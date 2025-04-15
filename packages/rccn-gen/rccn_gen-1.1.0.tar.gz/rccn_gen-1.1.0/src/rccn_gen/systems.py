from yamcs.pymdb import System, Subsystem, Command, Container, AndExpression, EqExpression
import shutil
import difflib
import datetime
from caseconverter import *
from importlib.resources import files
from .utils import *

class Application(Subsystem):
    """
    A PUS application.
    """
    def __init__(
        self,
        system: System,
        name: str,
        apid: int,
        vcid: int = 0,
        export_file_path = '.',
        snapshot_file_path = './.rccn_snapshots',
        diff_file_path = './.rccn_diffs',
        snapshots = True,
        *args,
        **kwargs
    ):
        super().__init__(system=system, name=name, *args, **kwargs)

        self.apid = apid
        self.vcid = vcid
        system._subsystems_by_name[name] = self
        self.export_file_path = export_file_path
        self.snapshot_file_path = snapshot_file_path
        self.snapshot_generated_file_path = os.path.join(snapshot_file_path, 'auto_generated')
        self.diff_file_path = diff_file_path
        self.text_modules_path = files('rccn_gen').joinpath('text_modules')
        print(self.text_modules_path)
        self.text_modules_main_path = os.path.join(self.text_modules_path, 'main')
        print(self.text_modules_main_path)
        self.snapshots = snapshots
        self.keep_snapshots = 10
    
    def add_service(self, service):
        if not isinstance(service, Service):
            raise TypeError('Service '+service.name+' is not a RCCNCommand.')
        service.add_to_application(self)
    
    def file_paths(self):
        paths = {
            'main': os.path.join(self.export_file_path, 'rccn_usr_'+snakecase(self.name), 'src', 'main.rs'),
            'main_generated_snapshot': os.path.join(self.snapshot_file_path, 'generated', 'rccn_usr_'+snakecase(self.name), 'src', 'main.rs'),
            'main_user_snapshot': os.path.join(self.user_snapshot_path(), 'rccn_usr_'+snakecase(self.name), 'src', 'main.rs'),
            'main_diff': os.path.join(self.diff_file_path, 'rccn_usr_'+snakecase(self.name), 'src', 'main.diff'),
            'main_template': os.path.join(self.text_modules_main_path, 'main.txt'),
            'cargo_toml': os.path.join(self.export_file_path, 'rccn_usr_'+snakecase(self.name), 'Cargo.toml'),
            'cargo_toml_template': os.path.join(self.text_modules_path, 'cargo_toml', 'cargo.txt'),
        }
        return paths

    def user_snapshot_path(self):
        return os.path.join(self.snapshot_file_path, 'user', datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S"))

    def services(self):
        return [subsystem for subsystem in self.subsystems if isinstance(subsystem, Service)]

    def create_rccn_directories(self):
        app_src_dir = os.path.join(self.export_file_path, 'rccn_usr_'+snakecase(self.name), 'src')
        if not os.path.exists(app_src_dir):
            os.makedirs(app_src_dir)
        for service in self.services():
            service_dir = os.path.join(app_src_dir, snakecase(service.name))
            if not os.path.exists(service_dir):
                os.makedirs(service_dir)

    def generate_rccn_main_file(self):
        # Create main.diff file
        if os.path.exists(self.file_paths()['main']) and os.path.exists(self.file_paths()['main_generated_snapshot']):
            os.makedirs(os.path.dirname(self.file_paths()['main_diff']), exist_ok=True)
            self.generate_diff_file('main', 'main_generated_snapshot', 'main_diff')
        # Create snapshot of main.rs with user changes if instructed
        if self.snapshots and os.path.exists(self.file_paths()['main']):
            self.generate_snapshot('main', 'main_user_snapshot')
        # Generate main.rs file
        with open(self.file_paths()['main_template'], 'r') as file:
            main_template_text = file.read()
        with open(self.file_paths()['main'], 'w') as file:
            new_main_text = self.find_and_replace_keywords(main_template_text)
            file.write("".join(new_main_text))
        # Create snapshot of newly generated main.rs if instructed
        if self.snapshots:
            self.generate_snapshot('main', 'main_generated_snapshot')
        # Rebase main.diff on main.rs if instructed
        if self.rebase_changes and os.path.exists(self.file_paths()['main_diff']):
            os.system('patch '+self.file_paths()['main']+' <  '+self.file_paths()['main_diff'])
    
    def find_and_replace_keywords(self, text):
        # Call keyword replacement for all associated services (Later, there needs to be checking to account for user changes to the generated files)
        for service in self.services():
            text = service.find_and_replace_keywords(text, self.text_modules_main_path)
        # Find and replace service variable keywords
        var_translation = {
            '<<VAR_APID>>':str(self.apid),
            '<<VAR_VCID>>':str(self.vcid),
            '<<VAR_APP_NAME_SCASE>>':snakecase(self.name),
        }
        var_keywords = get_var_keywords(text)
        for var_keyword in var_keywords:
            if var_keyword in var_translation.keys():
                text = text.replace(var_keyword, var_translation[var_keyword])
            else:
                raise KeyError('Keyword '+var_keyword+' is not in translation dictionary.')
        text = delete_all_keywords(text)
        return text 
    
    def generate_rccn_code(self, rebase_changes=True, check=True, export_file_path='.'):
        self.export_file_path = export_file_path
        if check:
            self.check_user_input()
        self.rebase_changes = rebase_changes
        self.create_rccn_directories()
        self.generate_rccn_main_file()
        self.generate_rccn_main_file()
        if not os.path.exists(self.file_paths()['cargo_toml']):
            self.generate_cargo_toml_file()
        for service in self.services():
            service.export_file_path = self.export_file_path
            service.generate_rccn_service_file()
            if not os.path.exists(service.file_paths()['mod']):
                service.generate_mod_file()
            service.generate_telemetry_file()
            service.generate_rccn_command_file(os.path.join(self.export_file_path, 'rccn_usr_'+snakecase(self.name), 'src'), os.path.join(self.text_modules_path, 'command'))
        self.delete_old_snapshots()

    def generate_snapshot(self, current_file_reference, snapshot_file_reference):
        os.makedirs(os.path.dirname(self.file_paths()[snapshot_file_reference]), exist_ok=True)
        shutil.copyfile(self.file_paths()[current_file_reference], self.file_paths()[snapshot_file_reference])
    
    def generate_diff_file(self, current_file_reference, snapshot_file_reference, diff_file_reference):
        with open(self.file_paths()[current_file_reference], 'r') as current_file:
            current_text = current_file.readlines()
        with open(self.file_paths()[snapshot_file_reference], 'r') as snapshot_file:
            snapshot_text = snapshot_file.readlines()
        diff = difflib.unified_diff(snapshot_text, current_text, fromfile='snapshot', tofile='current')
        diff_text = ''.join(diff)
        current_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(self.file_paths()[diff_file_reference], 'w') as diff_file:
            diff_file.write(diff_text)
    
    def delete_old_snapshots(self):
        if os.path.exists(os.path.join(self.snapshot_file_path, 'user')):
            user_snapshots_path = os.path.join(self.snapshot_file_path, 'user')
            snapshots = [os.path.join(user_snapshots_path, d) for d in os.listdir(user_snapshots_path) if os.path.isdir(os.path.join(user_snapshots_path, d))]
            snapshots.sort(key=os.path.getctime)
            while len(snapshots) > self.keep_snapshots:
                shutil.rmtree(snapshots.pop(0))
    
    def check_user_input(self):
        # Check if all services have unique names
        service_names = [service.name for service in self.services()]
        if len(service_names) != len(set(service_names)):
            raise ValueError('All services must have unique names.')
        
        # Check if all services have unique service_ids
        service_ids = [service.service_id for service in self.services()]
        if len(service_ids) != len(set(service_ids)):
            raise ValueError('All services must have unique service_ids.')
        
        # Check if all commands have unique names
        command_names = []
        for service in self.services():
            command_names += [command.name for command in service.rccn_commands()]
        if len(command_names) != len(set(command_names)):
            raise ValueError('All commands must have unique names.')
        
        # Check if all commands have unique subtypes
        command_subtypes = []
        for service in self.services():
            command_subtypes += [command.assignments['subtype'] for command in service.rccn_commands()]
        if len(command_subtypes) != len(set(command_subtypes)):
            raise ValueError('All commands must have unique subtypes.')
        
    def generate_cargo_toml_file(self):
        with open(self.file_paths()['cargo_toml_template'], 'r') as file:
            cargo_toml_template_text = file.read()
        with open(self.file_paths()['cargo_toml'], 'w') as file:
            file.write(cargo_toml_template_text)


class Service(Subsystem):
    def __init__(
        self,
        name: str,
        service_id: int,
        *args,
        **kwargs
    ):
        self.init_args = args
        self.init_kwargs = kwargs
        self.init_args = args
        self.init_kwargs = kwargs
        self.name = name
        self.service_id = service_id
        self.text_modules_path = files('rccn_gen').joinpath('text_modules')
        self.text_modules_service_path = os.path.join(self.text_modules_path, 'service')
        self.text_modules_command_path = os.path.join(self.text_modules_path, 'command')
        self.text_modules_telemetry_path = os.path.join(self.text_modules_path, 'telemetry')
        if 'system' in kwargs and isinstance(kwargs['system'], Application):
            self.add_to_application(kwargs['system'])
    
    def add_to_application(self, application):
        if 'system' in self.init_kwargs and isinstance(self.init_kwargs['system'], Application):
            super().__init__(
                name=self.name,
                *self.init_args, **self.init_kwargs
            )
        else:
            super().__init__(
                system=application,
                name=self.name,
                *self.init_args, **self.init_kwargs
            )
        self.export_file_path = self.system.export_file_path
        self.snapshot_file_path = self.system.snapshot_file_path
        self.snapshots = self.system.snapshots
        self.diff_file_path = self.system.diff_file_path
    
    def add_container(self, container):
        if not isinstance(container, RCCNContainer):
            raise TypeError('Container '+container.name+' is not a RCCNContainer.')
        container.add_to_service(self)
    
    def add_command(self, command):
        if not isinstance(command, RCCNCommand):
            raise TypeError('Command '+command.name+' is not a RCCNCommand.')
        command.add_to_service(self)
    
    def file_paths(self):
        paths = {
            'service': os.path.join(self.export_file_path, 'rccn_usr_'+snakecase(self.system.name), 'src', snakecase(self.name), 'service.rs'),
            'service_generated_snapshot': os.path.join(self.snapshot_file_path, 'generated', 'rccn_usr_'+snakecase(self.system.name), 'src', snakecase(self.name), 'service.rs'),
            'service_user_snapshot': os.path.join(self.snapshot_file_path, 'user', datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S"), 'rccn_usr_'+snakecase(self.system.name), 'src', snakecase(self.name), 'service.rs'),
            'service_diff': os.path.join(self.diff_file_path, 'rccn_usr_'+snakecase(self.system.name), 'src', snakecase(self.name), 'service.diff'),
            'service_template': os.path.join(self.text_modules_service_path, 'service.txt'),
            'command': os.path.join(self.export_file_path, 'rccn_usr_'+snakecase(self.system.name), 'src', snakecase(self.name), 'command.rs'),
            'command_generated_snapshot': os.path.join(self.snapshot_file_path, 'generated', 'rccn_usr_'+snakecase(self.system.name), 'src', snakecase(self.name), 'command.rs'),
            'command_user_snapshot': os.path.join(self.snapshot_file_path, 'user', datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S"), 'rccn_usr_'+snakecase(self.system.name), 'src', snakecase(self.name), 'command.rs'),
            'command_diff': os.path.join(self.diff_file_path, 'rccn_usr_'+snakecase(self.system.name), 'src', snakecase(self.name), 'command.diff'),
            'command_template': os.path.join(self.text_modules_command_path, 'command.txt'),
            'mod': os.path.join(self.export_file_path, 'rccn_usr_'+snakecase(self.system.name), 'src', snakecase(self.name), 'mod.rs'),
            'mod_template': os.path.join(self.text_modules_path, 'mod', 'mod.txt'),
            'telemetry': os.path.join(self.export_file_path, 'rccn_usr_'+snakecase(self.system.name), 'src', snakecase(self.name), 'telemetry.rs'),
            'telemetry_generated_snapshot': os.path.join(self.snapshot_file_path, 'generated', 'rccn_usr_'+snakecase(self.system.name), 'src', snakecase(self.name), 'telemetry.rs'),
            'telemetry_user_snapshot': os.path.join(self.snapshot_file_path, 'user', datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S"), 'rccn_usr_'+snakecase(self.system.name), 'src', snakecase(self.name), 'command.rs'),
            'telemetry_diff': os.path.join(self.diff_file_path, 'rccn_usr_'+snakecase(self.system.name), 'src', snakecase(self.name), 'telemetry.diff'),
            'telemetry_template': os.path.join(self.text_modules_telemetry_path, 'telemetry.txt'),
        } 
        return paths

    def rccn_commands(self):
        return [command for command in self.commands if isinstance(command, RCCNCommand) and command.name != 'base']

    def find_and_replace_keywords(self, text, text_modules_path):
        # Find and replace service module keywords
        service_module_keywords = get_service_module_keywords(text)
        for service_module_keyword in service_module_keywords:
            service_module_file_name = service_module_keyword.replace('>','').replace('<', '').lower() + '.txt'
            service_module_path = os.path.join(text_modules_path, service_module_file_name)
            if not os.path.exists(service_module_path):
                raise FileExistsError('Specified keyword '+service_module_keyword+' does not correspond to a text file.')
            
            with open(service_module_path, 'r') as file:
                module_text = file.read()
            replacement_text = (self.find_and_replace_keywords(module_text, text_modules_path) + '\n')
            text = insert_before_with_indentation(text, service_module_keyword, replacement_text)
        
        for command in self.rccn_commands():
            text = command.find_and_replace_keywords(text, text_modules_path)
        
        # Find and replace service variable keywords
        var_keywords = get_var_keywords(text)
        service_var_translation = {
            '<<VAR_SERVICE_NAME>>': lambda: snakecase(self.name),
            '<<VAR_SERVICE_ID>>': lambda: str(self.service_id),
            '<<VAR_SERVICE_NAME_UCASE>>': lambda: pascalcase(self.name),
            '<<VAR_SERVICE_TELEMETRY>>': lambda: self.generate_rust_telemetry_definition(),
        }
        for var_keyword in var_keywords:
            if var_keyword in service_var_translation.keys():
                text = replace_with_indentation(text, var_keyword, service_var_translation[var_keyword]())
        
        # Delete all command module keywords
        text = delete_all_command_module_keywords(text)

        return text
    
    def generate_rccn_service_file(self):
        # Create service.diff file
        if os.path.exists(self.file_paths()['service']) and os.path.exists(self.file_paths()['service_generated_snapshot']):
            os.makedirs(os.path.dirname(self.file_paths()['service_diff']), exist_ok=True)
            self.generate_diff_file('service', 'service_generated_snapshot', 'service_diff')
        # Create snapshot of service.rs with user changes if instructed
        if self.snapshots and os.path.exists(self.file_paths()['service']):
            self.generate_snapshot('service', 'service_user_snapshot')
        # Generate service.rs file
        with open(self.file_paths()['service_template'], 'r') as file:
            service_template_file_text = file.read()
        with open(self.file_paths()['service'], 'w') as file:
            file.write(self.find_and_replace_keywords(service_template_file_text, self.text_modules_service_path))
        # Create snapshot of service.rs if instructed
        if self.snapshots:
            self.generate_snapshot('service', 'service_generated_snapshot')
        # Rebase main.diff on main.rs if instructed
        if self.system.rebase_changes and os.path.exists(self.file_paths()['service_diff']):
            os.system('patch '+self.file_paths()['service']+' <  '+self.file_paths()['service_diff'])
    
    def generate_rccn_command_file(self, export_file_dir='.', text_modules_path='./text_modules/command'):
        # Create command.diff file
        if os.path.exists(self.file_paths()['command']) and os.path.exists(self.file_paths()['command_generated_snapshot']):
            os.makedirs(os.path.dirname(self.file_paths()['command_diff']), exist_ok=True)
            self.generate_diff_file('command', 'command_generated_snapshot', 'command_diff')
        # Create snapshot of command.rs with user changes if instructed
        if self.snapshots and os.path.exists(self.file_paths()['command']):
            self.generate_snapshot('command', 'command_user_snapshot')
        # Generate command.rs file
        if len(self.rccn_commands()) == 0:
            print('RCCN-Information: Service \''+self.name+'\' has no commands other than base command. Generation of command.rs file will be skipped.')
            return
        command_file_path = self.file_paths()['command_template']
        with open(command_file_path, 'r') as file:
            command_file_text = file.read()
        command_export_file_path = os.path.join(export_file_dir, snakecase(self.name), 'command.rs')
        with open(command_export_file_path, 'w') as file:
            file.write(self.find_and_replace_keywords(command_file_text, text_modules_path))
        # Create snapshot of command.rs if instructed
        if self.snapshots:
            self.generate_snapshot('command', 'command_generated_snapshot')
        # Rebase command.diff on command.rs if instructed
        if self.system.rebase_changes and os.path.exists(self.file_paths()['command_diff']):
            os.system('patch '+self.file_paths()['command']+' <  '+self.file_paths()['command_diff'])
    
    def generate_snapshot(self, current_file_reference, snapshot_file_reference):
        os.makedirs(os.path.dirname(self.file_paths()[snapshot_file_reference]), exist_ok=True)
        shutil.copyfile(self.file_paths()[current_file_reference], self.file_paths()[snapshot_file_reference])
        
    def generate_diff_file(self, current_file_reference, snapshot_file_reference, diff_file_reference):
        with open(self.file_paths()[current_file_reference], 'r') as current_file:
            current_text = current_file.readlines()
        with open(self.file_paths()[snapshot_file_reference], 'r') as snapshot_file:
            snapshot_text = snapshot_file.readlines()
        diff = difflib.unified_diff(snapshot_text, current_text, fromfile='snapshot', tofile='current')
        diff_text = ''.join(diff)
        with open(self.file_paths()[diff_file_reference], 'w') as diff_file:
            diff_file.write(diff_text)
    
    def generate_mod_file(self):
        with open(self.file_paths()['mod_template'], 'r') as file:
            mod_template_text = file.read()
        with open(self.file_paths()['mod'], 'w') as file:
            file.write(mod_template_text)
    
    def generate_telemetry_file(self):
        # Create telemetry.diff file
        if os.path.exists(self.file_paths()['telemetry']) and os.path.exists(self.file_paths()['telemetry_generated_snapshot']):
            os.makedirs(os.path.dirname(self.file_paths()['telemetry_diff']), exist_ok=True)
            self.generate_diff_file('telemetry', 'telemetry_generated_snapshot', 'telemetry_diff')
        # Create snapshot of telemetry.rs with user changes if instructed
        if self.snapshots and os.path.exists(self.file_paths()['telemetry']):
            self.generate_snapshot('telemetry', 'telemetry_user_snapshot')
        # Generate telemetry.rs file
        with open(self.file_paths()['telemetry_template'], 'r') as file:
            telemetry_template_file_text = file.read()
        with open(self.file_paths()['telemetry'], 'w') as file:
            file.write(self.find_and_replace_keywords(telemetry_template_file_text, self.text_modules_telemetry_path))
        # Create snapshot of telemetry.rs if instructed
        if self.snapshots:
            self.generate_snapshot('telemetry', 'telemetry_generated_snapshot')
        # Rebase main.diff on main.rs if instructed
        if self.system.rebase_changes and os.path.exists(self.file_paths()['telemetry_diff']):
            os.system('patch '+self.file_paths()['telemetry']+' <  '+self.file_paths()['telemetry_diff'])
    
    def generate_rust_telemetry_definition(self):
        telemetry_definition_text = ''
        for container in self.containers:
            if not isinstance(container, RCCNContainer):
                container.__class__ = RCCNContainer
            telemetry_definition_text += container.generate_rccn_telemetry()
        return telemetry_definition_text


class RCCNCommand(Command):
    def __init__(self, *args, **kwargs):
        self.init_args = args
        self.init_kwargs = kwargs
        if 'system' in kwargs and isinstance(kwargs['system'], Service):
            self.add_to_service(kwargs['system'])
        elif 'base' in kwargs and (isinstance(kwargs['base'], Command) or isinstance(kwargs['base'], RCCNCommand)):
            self.add_to_service(kwargs['base'].system)

    def add_to_service(self, service):
        if not 'base' in self.init_kwargs and not any(command.name == 'base' for command in service.commands):
            print("RCCN-Information: Command \'"+self.init_kwargs['name']+"\' doesn\'t have a base argument and no base command was found in service \'"+service.name+"\'.\nStandard base command will be used with system = \'"+service.name+"\' and type = "+str(service.service_id)+".")
            self.init_kwargs['base'] = Command(
                system=service, 
                name='base',
                abstract=True,
                base='/PUS/pus-tc',
                assignments={'type': service.service_id}
            )
        elif not 'base' in self.init_kwargs and any(command.name == 'base' for command in service.commands):
            print("RCCN-Information: Command \'"+self.init_kwargs['name']+"\' doesn\'t have a \'base\' argument. Existing base command for service \'"+service.name+"\' will be used.")
            self.init_kwargs['base'] = next(command for command in service.commands if command.name == 'base')
        if 'system' in self.init_kwargs and isinstance(self.init_kwargs['system'], Service):
            super().__init__(*self.init_args, **self.init_kwargs)
        else:
            super().__init__(system=service, *self.init_args, **self.init_kwargs)
        self.assignments['apid'] = self.system.system.apid
        self.struct_name = self.name + 'Args'

    
    def find_and_replace_keywords(self, text, text_modules_path):
        # Find and replace command module keywords
        command_module_keywords = get_command_module_keywords(text)
        for command_module_keyword in command_module_keywords:
            command_module_file_name = command_module_keyword.replace('>','').replace('<', '').lower() + '.txt'
            command_module_path = os.path.join(text_modules_path, command_module_file_name)
            if not os.path.exists(command_module_path):
                raise FileExistsError('Specified keyword '+command_module_keyword+' does not correspond to a text file.')
            
            with open(command_module_path, 'r') as file:
                module_text = file.read()
            replacement_text = (self.find_and_replace_keywords(module_text, text_modules_path) + '\n')
            text = insert_before_with_indentation(text, command_module_keyword, replacement_text)

        # Find and replace command variable keywords
        command_var_keywords = get_var_keywords(text)
        command_var_translation = {
            '<<VAR_COMMAND_NAME_UCASE>>': lambda: pascalcase(self.name),
            '<<VAR_COMMAND_NAME>>': lambda: self.name,
            '<<VAR_COMMAND_STRUCT_NAME>>': lambda: self.struct_name,
            '<<VAR_COMMAND_SUBTYPE>>': lambda: str(self.assignments['subtype']),
            '<<VAR_COMMAND_STRUCT>>': lambda: self.struct_definition(),
            '<<VAR_SHORT_DESCRIPTION>>': lambda: "\n/// " + self.short_description if self.short_description is not None else "",
        }
        for command_var_keyword in command_var_keywords:
            if command_var_keyword in command_var_translation.keys():
                text = replace_with_indentation(text, command_var_keyword, command_var_translation[command_var_keyword]())
        return text
    
    def check_user_input(self):
        if self.assignments['subtype'] == None and self.name != 'base':
            raise ValueError('Command '+self.name+' does not have a subtype assigned to it.')
    
    def user_snapshot_path(self):
        return os.path.join(self.snapshot_file_path, 'user', datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S"))

    def struct_definition(self):
        struct_definition_text = ""
        if len(self.arguments) == 0:
            return ''
        if hasattr(self, 'long_description') and self.long_description is not None:
            struct_definition_text += "/// "+str(self.long_description)+"\n"
        struct_definition_text += "#[derive(BitStruct, Debug, PartialEq)]\npub struct "+pascalcase(self.struct_name)+" {\n"
        ins = ""
        append = ""
        for argument in self.arguments:
            arg_def = rust_type_definition(argument)
            ins += arg_def[0]
            append += arg_def[1]
        struct_definition_text += ins
        struct_definition_text += "}\n"
        struct_definition_text += append
        return struct_definition_text

class RCCNContainer(Container):
    def __init__(self, base="/PUS/pus-tm", subtype = None, *args, **kwargs):
        self.base = base
        self.subtype = subtype
        self.init_args = args
        self.init_kwargs = kwargs
        self.init_kwargs['base'] = base
        self.name = kwargs['name']
        if 'system' in kwargs and isinstance(kwargs['system'], Service):
            self.add_to_service(kwargs['system'])

    def add_to_service(self, service):
        self.type = service.service_id
        condition_type = None
        condition_subtype = None
        if 'condition' in self.init_kwargs:
            for eq_expression in self.init_kwargs['condition'].expressions:
                if eq_expression.ref == self.base+'/type':
                    condition_type = eq_expression.value
                if eq_expression.ref == self.base+'/subtype':
                    condition_subtype = eq_expression.value
        if condition_type is not None and condition_type != self.type:
            print('RCCN-Warning: Container '+self.name+' has a user-defined type of '+str(eq_expression.value)+', which does\'nt match the service ID. User-defined type will be used.')
            self.type = condition_type
        if condition_subtype is not None and self.subtype is not None and condition_subtype != self.subtype:
            print('RCCN-Warning: Container '+self.name+' has an ambiguous user-defined subtype. \'subtype\' argument should match the \'condition\' argument.')
        elif condition_subtype is not None:
            self.subtype = condition_subtype
        elif self.subtype is not None and not 'condition' in self.init_kwargs:
            self.init_kwargs['condition'] = AndExpression(
                EqExpression(self.base+'/type', self.type),
                EqExpression(self.base+'/subtype', self.subtype)
                )
        else:
            raise ValueError('RCCN-Error: Container '+self.name+' has no \'condition\' argument and condition could not be created due to a missing \'subtype\' argument.')

        if 'system' in self.init_kwargs and isinstance(self.init_kwargs['system'], Service):
            super().__init__(*self.init_args, **self.init_kwargs)
        else:
            super().__init__(system=service, *self.init_args, **self.init_kwargs)

    def generate_rccn_telemetry(self):
        rccn_telemetry_text = ""
        if hasattr(self, 'short_description') and self.short_description is not None:
            rccn_telemetry_text += "/// "+str(self.short_description)+"\n"
        rccn_telemetry_text += "#[derive(ServiceTelemetry, BitStruct, Debug)]\n"
        if hasattr(self, 'subtype') and self.subtype is not None:
            rccn_telemetry_text += "#[subtype("+str(self.subtype)+")]\n"
        rccn_telemetry_text += "pub struct " + self.name + " {\n"
        insert, append = ["",""]
        for parameter_entry in self.entries:
            par_def = rust_type_definition(parameter_entry.parameter)
            insert += par_def[0]
            append += par_def[1]
        rccn_telemetry_text += insert
        rccn_telemetry_text += "}\n\n"
        rccn_telemetry_text += append        
        return rccn_telemetry_text
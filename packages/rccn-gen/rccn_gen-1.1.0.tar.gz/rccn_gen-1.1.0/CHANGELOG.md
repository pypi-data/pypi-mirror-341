# CHANGE LOG

## [1.1.0] - 2025-04-14
- Added derive statements to the rust container structs in the telemetry.rs file.
- Inherit subtype of a container from the `condition` argument, if given, or from the new (optional) `subtype` argument. If only the latter is given, condition is created from that. Subtype is included in the derive statements.
- Added missing `use anyhow::Result` import and bug fixes in `main.rs` file. 
- Added new dependencies in `cargo.toml` file.
- Changed names of command structs to differentiate between trait names and struct names. 
- Include bit number statement in enum declaration.
- The `tc` parameter in the service.rs file is now mutable.
- `System` of a command is obtained from the base command, if no system argument is given.
- Added support for long and short descriptions of commands, arguments and supported telemetry parameters.
- Bug fixes.
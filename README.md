# Minecraft World Pre-generator

**Version**: 1.0.0-dev

Pre-generate your Minecraft worlds to reduce lag, especially suitable for UHC.

## Start Generating

The following dependencies must be installed on your system:

 - [Python3](https://www.python.org/downloads/)
 
 Simply pipe `generator.py` into your Minecraft server:
 
  - `path/to/generator.py | java -Xms512M -Xmx2048M -jar path/to/server.jar nogui`
  
 Look at the [CLI](#command-line-interface) for further options.

## Compatible Minecraft Versions

Following are the Minecraft versions which have been checked to be compatible with this script. Missing versions may still be compatible. Please submit a pull request if you have tested a missing version.

 - Minecraft Java Edition 1.14
   - Vanilla Server - `"js1.14"`

## Command-line Interface

Syntax: `$PYTHON3 generator.py [args]`

Replace `$PYTHON3` with your Python3 binary, often `python` or `python3` will do.

Arguments:

 - `-d` or `--default`
   - Uses default values instead of user input for applicable options
 - `-s <stress>` or `--stress <stress>`
   - Sets how much stress to put on the server
   - Ranges from `1` to `10`
   - Default value: user input or `5` if `-d` option is set

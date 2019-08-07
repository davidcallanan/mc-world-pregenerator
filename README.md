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

 - `-t` or `--target`
   - Changes the target Minecraft server version
   - See [Compatible Minecraft Versions](#compatible-minecraft-versions)
   - Default value: `js1.14`
 - `-x <chunk-x>` or `--origin-x <chunk-x>`
   - Sets the x origin
	 - Default value: `0`
 - `-z <chunk-z>` or `--origin-z <chunk-z>`
   - Sets the z origin
	 - Default value: `0`
 - `-w <chunks>` or `--width <chunks>`
   - Sets the number of chunks for the width
	 - Default value: `64`
 - `-l <chunks>` or `--length <chunks>`
   - Sets the number of chunks for the length
	 - Default value: `64`
 - `-s <chunks>` or `--segment-size <chunks>`
   - Sets number of chunks to generate in each segment
	 - Rounds down to the nearest square
	 - If this number is too high:
     - the server may fall behind and chunks may be skipped
	   - the server may run out of RAM and crash
	 - Min value: `1`
	 - Max value: `256`
	 - Default value: `64`
 - `-T <time>` or `--segment-time <time>`
   - Sets the time interval in seconds to generate each segment
	 - If this number is too low there may be similar consequences to a high segment size
	 - Min value: `1`
	 - Max value: `16`
	 - Default value: `8`
 - `-d <time>` or `--delay <time>`
   - Sets the delay in seconds before pre-generating the world
	 - This is useful on Windows where there's no fifo files
 - `-k` or `--keep-loaded`
   - Keeps chunks loaded after generation
	 - Eats up a lot of RAM

#!/usr/bin/env python3

# Copyright (c) 2019 David Callanan
# See `LICENSE` file for license details

#######################################
# IMPORTS
#######################################

import sys
import math
import time
import argparse

#######################################
# WORLD PREGENERATOR
#######################################

def iter_pregeneration_commands(x1, z1, x2, z2, delay_interval):
	if x1 > x2: x1, x2 = x2, x1
	if z1 > z2: z1, z2 = z2, z1
	xdiff = x2 - x1
	zdiff = z2 - z1
	predicted_seconds = int(delay_interval * xdiff * zdiff)
	predicted_minutes = int(predicted_seconds / 60)

	time.sleep(delay_interval / 2)
	yield 'tellraw @a ["",{"text":"World pre-generation has started!","color":"gold","hoverEvent":{"action":"show_text","value":{"text":"","extra":[{"text":"This will take at minimum ' + str(predicted_seconds) + ' seconds!","color":"light_purple"}]}}},{"text":"github.com/davidcallanan/mc-world-pregenerator","color":"yellow","underlined":true,"clickEvent":{"action":"open_url","value":"https://www.github.com/davidcallanan/mc-loot-randomizer"},"hoverEvent":{"action":"show_text","value":{"text":"","extra":[{"text":"Generator source code","color":"green"}]}}},{"text":"This will take at minimum ' + str(predicted_minutes) + ' minutes","color":"light_purple","underlined":false}]\n'
	
	for x in range(x1, x2 + 1):
		time.sleep(delay_interval / 2)
		yield f"/say [World generation] {round((x - x1) / (xdiff + 1) * 100, 1)}% complete\n"

		for z in range(z1, z2 + 1):
			time.sleep(delay_interval / 2)
			yield f"/forceload add {x} {z}\n"
			time.sleep(delay_interval / 2)
			#yield f"/forceload remove {x} {z}\n"
	
	time.sleep(delay_interval / 2)
	yield f"/say [World generation] 100% complete\n"
	time.sleep(delay_interval / 2)
	yield 'tellraw @a ["",{"text":"World pre-generation has completed!","color":"gold"},{"text":"github.com/davidcallanan/mc-world-pregenerator","color":"yellow","underlined":true,"clickEvent":{"action":"open_url","value":"https://www.github.com/davidcallanan/mc-loot-randomizer"},"hoverEvent":{"action":"show_text","value":{"text":"","extra":[{"text":"Generator source code","color":"green"}]}}}]\n'

#######################################
# COMMAND-LINE INTERFACE
#######################################

# Default values

default_target = 'js1.14'
default_stress = 5
default_origin_x = 0
default_origin_z = 0
default_width = 64
default_length = 64

# Parse arguments

parser = argparse.ArgumentParser(description='World pregenerator\nPipe the output of this script into your server')
parser.add_argument('-t', '--target', default=default_target, help='target minecraft version')
parser.add_argument('-s', '--stress', type=int, default=default_stress, help='stress level on server')
parser.add_argument('-x', '--origin-x', type=int, default=default_origin_x, help='x origin in chunks')
parser.add_argument('-z', '--origin-z', type=int, default=default_origin_z, help='z origin in chunks')
parser.add_argument('-w', '--width', type=int, default=default_width, help='width in chunks')
parser.add_argument('-l', '--length', type=int, default=default_length, help='length in chunks')
args = parser.parse_args()

# Get values

x1 = args.origin_x - math.ceil(args.width / 2)
z1 = args.origin_z - math.ceil(args.length / 2)
x2 = args.origin_x + math.ceil(args.width / 2)
z2 = args.origin_z + math.ceil(args.length / 2)
delay_interval = 1.4 ** (10 - args.stress) / 20

# Output pregeneration commands

for cmd in iter_pregeneration_commands(x1, z1, x2, z2, delay_interval):
	sys.stdout.write(cmd)

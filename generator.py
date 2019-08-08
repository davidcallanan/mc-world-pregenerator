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

def note_pregeneration_begin(predicted_seconds):
	predicted_minutes = math.floor(predicted_seconds / 60)
	if predicted_minutes > 0: minute_text = f"{predicted_minutes} minutes"
	else: minute_text = f"{predicted_seconds} seconds"
	return '/tellraw @a ["",{"text":"World pre-generation has started!\n","color":"gold","hoverEvent":{"action":"show_text","value":{"text":"","extra":[{"text":"This will take at minimum ' + str(predicted_seconds) + ' seconds!","color":"light_purple"}]}}},{"text":"github.com/davidcallanan/mc-world-pregenerator","color":"yellow","underlined":true,"clickEvent":{"action":"open_url","value":"https://www.github.com/davidcallanan/mc-world-pregenerator"},"hoverEvent":{"action":"show_text","value":{"text":"","extra":[{"text":"Generator source code","color":"green"}]}}},{"text":"This will take at minimum ' + str(minute_text) + '","color":"light_purple","underlined":false}]'

def note_pregeneration_finish():
	return 'tellraw @a ["",{"text":"World pre-generation has completed!\n","color":"gold"},{"text":"github.com/davidcallanan/mc-world-pregenerator","color":"yellow","underlined":true,"clickEvent":{"action":"open_url","value":"https://www.github.com/davidcallanan/mc-loot-randomizer"},"hoverEvent":{"action":"show_text","value":{"text":"","extra":[{"text":"Generator source code","color":"green"}]}}}]'

def note_progress(progress):
	return f"/say [World generation] {round(progress * 100, 1)}% complete"

def load_section(x1, z1, x2, z2):
	return f"/forceload add {x1 * 16} {z1 * 16} {x2 * 16} {z2 * 16}"

def unload_section(x1, z1, x2, z2):
	return f"/forceload remove {x1 * 16} {z1 * 16} {x2 * 16} {z2 * 16}"

def save_all(should_flush=False):
	if should_flush:
		return f"/save-all flush"
	return f"/save-all"

def iter_pregeneration_commands(width, length, xoffset, zoffset, segment_size, segment_time, should_keep_loaded):
	segment_width = math.floor(math.sqrt(segment_size))
	segment_size = segment_width ** 2
	total_chunks = width * length
	num_segments = math.floor(total_chunks / segment_size)
	chunks_processed = 0
	predicted_seconds = segment_time * num_segments

	time.sleep(segment_time)
	yield note_pregeneration_begin(predicted_seconds)
	yield save_all(should_flush=True)
	time.sleep(segment_time)
	
	for i in range(math.ceil(width / segment_width)):
		base_x1 = i * segment_width
		base_x2 = min(base_x1 + segment_width - 1, width)
		x1 = base_x1 + xoffset
		x2 = base_x2 + xoffset

		for j in range(math.ceil(length / segment_width)):
			base_z1 = j * segment_width
			base_z2 = min(base_z1 + segment_width - 1, length)
			z1 = base_z1 + zoffset
			z2 = base_z2 + zoffset

			yield load_section(x1, z1, x2, z2)
			yield note_progress(chunks_processed / total_chunks)
			time.sleep(segment_time)
			if not should_keep_loaded:
				# yield save_all(should_flush=True)
				yield unload_section(x1, z1, x2, z2)
			chunks_processed += (x2 - x1 + 1) * (z2 - z1 + 1)

	time.sleep(segment_time)
	yield note_progress(1)
	yield note_pregeneration_finish()

#######################################
# COMMAND-LINE INTERFACE
#######################################

# Default values

default_target = 'js1.14'
default_origin_x = 0
default_origin_z = 0
default_width = 64
default_length = 64
default_segment_size = 64
default_segment_time = 8
default_delay = 0
min_segment_size = 1
max_segment_size = 256
min_segment_time = 0.5
max_segment_time = 16

# Parse arguments

parser = argparse.ArgumentParser(description='World pregenerator\nPipe the output of this script into your server')
parser.add_argument('-t', '--target', default=default_target, help='target minecraft version')
parser.add_argument('-x', '--center-x', type=int, default=default_origin_x, help='x center in chunks')
parser.add_argument('-z', '--center-z', type=int, default=default_origin_z, help='z center in chunks')
parser.add_argument('-w', '--width', type=int, default=default_width, help='width in chunks')
parser.add_argument('-l', '--length', type=int, default=default_length, help='length in chunks')
parser.add_argument('-s', '--segment-size', type=int, default=default_segment_size, help='segment size in chunks')
parser.add_argument('-T', '--segment-time', type=float, default=default_segment_time, help='segment time interval in seconds')
parser.add_argument('-d', '--delay', type=float, default=default_delay, help='delay in seconds before generation')
parser.add_argument('-k', '--keep-loaded', action='store_true', help='keep chunks loaded after generation')
args = parser.parse_args()

# Get values

width = args.width
length = args.length
xoffset = args.center_x - math.ceil(width / 2)
zoffset = args.center_z - math.ceil(length / 2)
segment_size = min(max(args.segment_size, min_segment_size), max_segment_size)
segment_time = min(max(args.segment_time, min_segment_time), max_segment_time)
delay = args.delay
should_keep_loaded = args.keep_loaded

# Delay

time.sleep(delay)

# Output pregeneration commands

for cmd in iter_pregeneration_commands(width, length, xoffset, zoffset, segment_size, segment_time, should_keep_loaded):
	sys.stdout.write(cmd + "\n")
	sys.stdout.flush()

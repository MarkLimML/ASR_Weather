#! /usr/bin/env python3
import os
import wave

for file_name in os.listdir("waves_weather/"):
	with wave.open(file_name, "r") as wave_file:
		frame_rate = wave_file.getframerate()
		print(file_name, frame_rate)
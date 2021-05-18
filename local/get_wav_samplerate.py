#!/usr/bin/env python3
import os
import wave
import contextlib

for file_name in os.listdir("waves_weather/"):
	if("disaster" in file_name):
		with contextlib.closing(wave.open("waves_weather/"+file_name,'rb')) as wave_file:
			frame_rate = wave_file.getframerate()
			num_channels = int(wave_file.getnchannels())
			print(file_name, frame_rate, num_channels)
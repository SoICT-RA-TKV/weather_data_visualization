import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
from collections import namedtuple
from datetime import datetime, timedelta
import random
import math
from airbox_data import *
from rxpower_data import *
from darksky_data import *
from openweathermap_data import *
from wunderground_data import *
from wunderground_condition_data import *
import os

# Danh sach file input
airbox_files = os.listdir('airbox/')
rxpower_files = os.listdir('rxpower/')
darksky_files = os.listdir('darksky/')
openweathermap_files = os.listdir('openweathermap/')
wunderground_files = os.listdir('wunderground/')

def main():
	plot_signals = []
	plot_condition_signal = []
	rxpower_data(plot_signals, rxpower_files)
	airbox_data(plot_signals, airbox_files)
	darksky_data(plot_signals, darksky_files)
	openweathermap_data(plot_signals, openweathermap_files)
	wunderground_data(plot_signals, wunderground_files)
	# wunderground_condition_data(plot_condition_signal, wunderground_files)
	# Tach mang du lieu theo ngay
	# min_time = datetime.max
	# max_time = datetime.min
	# for signal in plot_signals:
	# 	min_time = min(min_time, signal['x'][0])
	# 	max_time = max(max_time, signal['x'][-1])
	# min_time += timedelta(hours = -min_time.hour, minutes = -min_time.minute,
	# 	seconds = -min_time.second, microseconds = -min_time.microsecond)
	# if (max_time.hour > 0) or (max_time.minute > 0) or (max_time.second > 0) or (max_time.microsecond > 0):
	# 	max_time += timedelta(days = 1, hours = -max_time.hour, minutes = -max_time.minute,
	# 		seconds = -max_time.second, microseconds = -max_time.microsecond)
	# i_time = min_time
	# while i_time < max_time:
	# 	data_plot(plot_signals, plot_condition_signal, i_time)
	# 	i_time += timedelta(days = 1)

# Ve do thi
def data_plot(plot_signals, plot_condition_signal, date):
	date_str = date.strftime("%Y-%m-%d")
	print("Plotting data:", date_str)
	fig, ax = plt.subplots(figsize = (16, 9))

	x = []
	y = []
	# color = ['r', 'g', 'b', 'y']
	color = [2, 3, 4, 5]
	for i in range(48):
		x.append(date + timedelta(minutes = i * 30))
		y.append(color[random.randint(0, 3)])
	# Y, X = np.meshgrid(y, x)
	# print(Y)
	# im = ax.imshow(Y)
	# x = np.arange(0, 48, 0.1)
	# ax.plot(x, np.sin(x))
	print(y)
	ax.plot(x, y, kind = 'bar')
	# plt.show()

	# fig, ax = plt.subplots(figsize = (16, 9))

	save = False
	def find(dates, date):
		first = 0
		while (first < len(dates)) and (dates[first] - date < timedelta()):
			first += 1
		last = first
		tmp_date = date + timedelta(days = 1)
		while (last < len(dates)) and (dates[last] - tmp_date < timedelta()):
			last += 1
		return first, last
	first = 0
	last = 0
	for signal in plot_signals:
		first, last = find(signal['x'], date)
		if first >= last:
			continue
		if not save:
			save = True
		if 'style' in signal:
			ax.plot(signal['x'][first:last], signal['y'][first:last], signal['style'], label = signal['name'])
			# ax.plot([(i - first) / (last - first) * 48 for i in range(first, last)], signal['y'][first:last], signal['style'], label = signal['name'])
		else:
			ax.plot(signal['x'][first:last], signal['y'][first:last], label = signal['name'])
			# ax.plot([(i - first) / (last - first) * 48 for i in range(first, last)], signal['y'][first:last], signal['style'])


	if save:
		# ax.legend()
		plt.rcParams.update({'font.size': 6, 'figure.figsize': (16, 9)})
		plt.title('Weather and Signal Data ' + date_str)
		# plt.savefig('plot/esp/plot_' + date_str + '.eps', format='eps')
		# plt.savefig('plot/png/plot_' + date_str + '.png', format='png')
		plt.show()
		# plt.close()

if __name__ == '__main__':
	main()
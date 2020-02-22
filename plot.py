import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
from collections import namedtuple
from datetime import datetime, timedelta
from airbox_data import *
from rxpower_data import *
from darksky_data import *
from openweathermap_data import *
from wunderground_data import *
import os

# Danh sach file input
airbox_files = os.listdir('airbox/')
rxpower_files = os.listdir('rxpower/')
darksky_files = os.listdir('darksky/')
openweathermap_files = os.listdir('openweathermap/')
wunderground_files = os.listdir('wunderground/')

def main():
	plot_signals = []
	airbox_data(plot_signals, airbox_files)
	darksky_data(plot_signals, darksky_files)
	openweathermap_data(plot_signals, openweathermap_files)
	wunderground_data(plot_signals, wunderground_files)
	rxpower_data(plot_signals, rxpower_files)
	# Tach mang du lieu theo ngay
	min_time = datetime.max
	max_time = datetime.min
	for signal in plot_signals:
		min_time = min(min_time, signal['x'][0])
		max_time = max(max_time, signal['x'][-1])
	min_time += timedelta(hours = -min_time.hour, minutes = -min_time.minute,
		seconds = -min_time.second, microseconds = -min_time.microsecond)
	if (max_time.hour > 0) or (max_time.minute > 0) or (max_time.second > 0) or (max_time.microsecond > 0):
		max_time += timedelta(days = 1, hours = -max_time.hour, minutes = -max_time.minute,
			seconds = -max_time.second, microseconds = -max_time.microsecond)
	i_time = min_time
	while i_time < max_time:
		data_plot(plot_signals, i_time)
		i_time += timedelta(days = 1)

# Ve do thi
def data_plot(plot_signals, date):
	date_str = date.strftime("%Y-%m-%d")
	print("Plotting data:", date_str)
	ax = 0
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
	for signal in plot_signals:
		first, last = find(signal['x'], date)
		if first >= last:
			continue
		if not save:
			fig, ax = plt.subplots(figsize = (16, 9))
			save = True
		ax.plot(signal['x'][first:last], signal['y'][first:last], label = signal['name'])
	if save:
		ax.legend()
		plt.rcParams.update({'font.size': 6, 'figure.figsize': (16, 9)})
		plt.title('Weather and Signal Data ' + date_str)
		plt.savefig('plot/esp/plot_' + date_str + '.eps', format='eps')
		plt.savefig('plot/png/plot_' + date_str + '.png', format='png')
		plt.close()
		# plt.show()

if __name__ == '__main__':
	main()
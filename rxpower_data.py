import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
from collections import namedtuple
from datetime import datetime, timedelta

NaN = np.NaN

# Xu ly du lieu RXPower
def rxpower_data(plot_signals, rxpower_files):
	print("Preprocessing rxpower data")
	rxpower_files.sort()
	rxpower_data = dict({
		'Time': [],
		'Power': []
		})
	for rxpower_file in rxpower_files:
		file = open('rxpower/' + rxpower_file, 'r')
		while True:
			tmp_data = file.readline()
			if tmp_data == None:
				break
			if tmp_data.find('***') >= 0 or tmp_data.find('CONFIG:') >= 0:
				continue
			tmp_data = tmp_data.split(',')
			if len(tmp_data) < 4:
				break
			datetime_string = tmp_data[0] + ' ' + tmp_data[1]
			tmp_datetime = datetime.strptime(datetime_string, '%m/%d/%Y %H:%M:%S')
			if (len(rxpower_data['Time']) > 0) and (tmp_datetime <= rxpower_data['Time'][-1]):
				continue
			rxpower_data['Time'].append(tmp_datetime)
			rxpower_data['Power'].append(float(tmp_data[2]))

	# Them du lieu RXPower vao danh sach ve do thi
	plot_signals.append(
		{'name': 'RXPower',
		'x': np.array(rxpower_data['Time']),
		'y': np.array(rxpower_data['Power'])
		})
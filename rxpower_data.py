import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
from collections import namedtuple
from datetime import datetime, timedelta
from utils import *

NaN = np.NaN

# Xu ly du lieu RXPower
def rxpower_data(plot_signals, rxpower_files):
	print("Preprocessing rxpower data")
	rxpower_data = dict({
		'Time': [],
		'Power': []
		})
	tmp_rxpower_data = dict()
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
			tmp_rxpower_data[tmp_datetime.timestamp()] = float(tmp_data[2])

	rxpower_data['Time'] = sorted(list(tmp_rxpower_data))
	for i in range(len(rxpower_data['Time'])):
		rxpower_data['Power'].append(tmp_rxpower_data[rxpower_data['Time'][i]])
		rxpower_data['Time'][i] = datetime.fromtimestamp(rxpower_data['Time'][i])
	rxpower_data['Power'] = normalize(rxpower_data['Power'], 0, 40)

	# Them du lieu RXPower vao danh sach ve do thi
	plot_signals.append(
		{'name': 'RXPower (0 - 40)',
		'style': 'c-',
		'x': np.array(rxpower_data['Time']),
		'y': np.array(rxpower_data['Power'])
		})
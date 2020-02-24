import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
from collections import namedtuple
from datetime import datetime, timedelta
from utils import *

NaN = np.NaN

# Xu ly du lieu wunderground
def wunderground_data(plot_signals, wunderground_files):
	print("Preprocessing wunderground data")
	wunderground_data_fields = ['Time', 'Wunderground_Temperature', 'Wunderground_DewPoint', 'Wunderground_Humidity', 'Wunderground_Wind',
		'Wunderground_WindSpeed', 'Wunderground_WindGust', 'Wunderground_Pressure',
		'Wunderground_Condition', 'Wunderground_Visibility']
	wunderground_data_fields_plot_mask = [1, 0, 0, 0, 0, 0, 0, 0, 0, 1]
	wunderground_data = dict()
	tmp_wunderground_data = dict()

	for wunderground_file in wunderground_files:
		file = open('./wunderground/' + wunderground_file, 'r')
		file.readline()
		while True:
			data = file.readline()
			if data == None:
				break
			data = data.replace(',', '').split('\t')
			if len(data) < len(wunderground_data_fields):
				break
			datetime_string = wunderground_file.replace('.txt', ' ') + data[0]
			data[0] = datetime.strptime(datetime_string, '%Y-%m-%d %H:%M')
			is_no_signal = True
			for i in range(1, len(wunderground_data_fields)):
				try:
					data[i] = float(data[i])
				except:
					data[i] = NaN
				if data[i] != 0:
					is_no_signal = False
			if is_no_signal:
				for i in range(1, len(wunderground_data_fields)):
					data[i] = NaN
			tmp_datetime = data[0].timestamp()
			tmp_wunderground_data[tmp_datetime] = dict()
			for i in range(1, len(wunderground_data_fields)):
				if wunderground_data_fields[i] == 0:
					continue
				tmp_wunderground_data[tmp_datetime][wunderground_data_fields[i]] = data[i]

	wunderground_data = dict()
	wunderground_data['Time'] = sorted(list(tmp_wunderground_data))
	for j in range(1, len(wunderground_data_fields)):
		if wunderground_data_fields_plot_mask[j] == 0:
			continue
		wunderground_data[wunderground_data_fields[j]] = []
		for i in range(len(wunderground_data['Time'])):
			wunderground_data[wunderground_data_fields[j]].append(tmp_wunderground_data[wunderground_data['Time'][i]][wunderground_data_fields[j]])
	for i in range(len(wunderground_data['Time'])):
		wunderground_data['Time'][i] = datetime.fromtimestamp(wunderground_data['Time'][i])

	wunderground_data['Wunderground_Visibility'] = [i * 1609.344 for i in wunderground_data['Wunderground_Visibility']]
	wunderground_data['Wunderground_Visibility'] = normalize(wunderground_data['Wunderground_Visibility'], 0, 10000)

	# Them du lieu wunderground vao danh sach ve do thi
	for i in range(1, len(wunderground_data_fields)):
		if wunderground_data_fields_plot_mask[i] == 1:
			plot_signals.append(
				{'name': wunderground_data_fields[i] + ' 0 - 10000(m)',
				'style': 'go-',
				'x': np.array(wunderground_data[wunderground_data_fields[0]]),
				'y': np.array(wunderground_data[wunderground_data_fields[i]])
				})
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
from collections import namedtuple
from datetime import datetime, timedelta

NaN = np.NaN

# Xu ly du lieu wunderground
def wunderground_data(plot_signals, wunderground_files):
	print("Preprocessing wunderground data")
	wunderground_data_fields = ['Time', 'Wunderground_Temperature', 'Wunderground_DewPoint', 'Wunderground_Humidity', 'Wunderground_Wind',
		'Wunderground_WindSpeed', 'Wunderground_WindGust', 'Wunderground_Pressure',
		'Wunderground_Condition', 'Wunderground_Visibility']
	wunderground_data_fields_plot_mask = [1, 1, 1, 1, 0, 0, 0, 0, 0, 1]
	wunderground_files.sort()
	wunderground_data = dict()
	for wunderground_data_field in wunderground_data_fields:
		wunderground_data[wunderground_data_field] = []

	for wunderground_file in wunderground_files:
		file = open('./wunderground/' + wunderground_file, 'r')
		file.readline().replace('\n', '')
		while True:
			data = file.readline().replace('\n', '')
			if data == None:
				break
			data = data.replace(',', '').split('\t')[:-1]
			if len(data) < len(wunderground_data_fields):
				break
			datetime_string = wunderground_file.replace('.txt', ' ') + data[0]
			data[0] = datetime.strptime(datetime_string, '%Y-%m-%d %H:%M')
			if (len(wunderground_data['Time']) > 0) and (data[0] <= wunderground_data['Time'][-1]):
				continue
			is_no_signal = True
			for i in range(1, len(data)):
				if wunderground_data_fields_plot_mask[i] == 0:
					continue
				data[i] = float(data[i])
				if data[i] > 0:
					is_no_signal = False
			if is_no_signal:
				for i in range(1, len(data)):
					data[i] = NaN
			for i in range(len(data)):
				wunderground_data[wunderground_data_fields[i]].append(data[i])

	# Them du lieu wunderground vao danh sach ve do thi
	for i in range(1, len(wunderground_data_fields)):
		if wunderground_data_fields_plot_mask[i] == 1:
			plot_signals.append(
				{'name': wunderground_data_fields[i],
				'x': np.array(wunderground_data[wunderground_data_fields[0]]),
				'y': np.array(wunderground_data[wunderground_data_fields[i]])
				})
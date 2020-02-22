import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
from collections import namedtuple
from datetime import datetime, timedelta

NaN = np.NaN

# Xu ly du lieu darksky
def darksky_data(plot_signals, darksky_files):
	print("Preprocessing darksky data")
	darksky_data_fields = ['Time', 'Darksky_Summary', 'Darksky_Icon', 'Darksky_PrecipIntensity', 'Darksky_PrecipProbability',
		'Darksky_PrecipType', 'Darksky_Temperature', 'Darksky_ApparentTemperature',
		'Darksky_DewPoint', 'Darksky_Humidity', 'Darksky_Pressure',
		'Darksky_WinSpeed', 'Darksky_WindGust', 'Darksky_WindBearing',
		'Darksky_CloudCover', 'Darksky_UVIndex', 'Darksky_Visibility', 'Darksky_Ozone']
	darksky_data_fields_plot_mask = [1, 0, 0, 1, 1, 0, 1, 0, 1, 1, 0, 0, 0, 0, 1, 0, 1, 0]
	darksky_files.sort()
	darksky_data = dict()
	for darksky_data_field in darksky_data_fields:
		darksky_data[darksky_data_field] = []

	for darksky_file in darksky_files:
		file = open('./darksky/' + darksky_file, 'r')
		file.readline()
		while True:
			data = file.readline()
			if data == None:
				break
			data = data.replace(',', '').split('\t')
			if len(data) < len(darksky_data_fields):
				break
			datetime_string = darksky_file.replace('.txt', ' ') + data[0]
			data[0] = datetime.strptime(datetime_string, '%Y-%m-%d %H:%M')
			if (len(darksky_data['Time']) > 0) and (data[0] <= darksky_data['Time'][-1]):
				continue
			is_no_signal = True
			for i in range(1, len(data)):
				if darksky_data_fields_plot_mask[i] == 0:
					continue
				data[i] = float(data[i])
				if data[i] > 0:
					is_no_signal = False
			if is_no_signal:
				for i in range(1, len(data)):
					data[i] = NaN
			for i in range(len(data)):
				darksky_data[darksky_data_fields[i]].append(data[i])

	# Them du lieu darksky vao danh sach ve do thi
	for i in range(1, len(darksky_data_fields)):
		if darksky_data_fields_plot_mask[i] == 1:
			plot_signals.append(
				{'name': darksky_data_fields[i],
				'x': np.array(darksky_data[darksky_data_fields[0]]),
				'y': np.array(darksky_data[darksky_data_fields[i]])
				})
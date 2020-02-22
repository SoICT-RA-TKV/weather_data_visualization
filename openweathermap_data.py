import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
from collections import namedtuple
from datetime import datetime, timedelta

NaN = np.NaN

# Xu ly du lieu openweathermap
def openweathermap_data(plot_signals, openweathermap_files):
	print("Preprocessing openweathermap data")
	openweathermap_data_fields = ['Time', 'OpenWeatherMap_Main', 'OpenWeatherMap_Description', 'OpenWeatherMap_Temperature', 'OpenWeatherMap_Pressure',
		'OpenWeatherMap_Humidity', 'OpenWeatherMap_Visibility', 'OpenWeatherMap_WindSpeed',
		'OpenWeatherMap_WindDeg', 'OpenWeatherMap_Clouds']
	openweathermap_data_fields_plot_mask = [1, 0, 0, 1, 0, 1, 1, 0, 0, 1]
	openweathermap_files.sort()
	openweathermap_data = dict()
	for openweathermap_data_field in openweathermap_data_fields:
		openweathermap_data[openweathermap_data_field] = []

	for openweathermap_file in openweathermap_files:
		file = open('./openweathermap/' + openweathermap_file, 'r')
		file.readline().replace('\n', '')
		while True:
			data = file.readline().replace('\n', '')
			if data == None:
				break
			data = data.replace(',', '').split('\t')[:-1]
			if len(data) < len(openweathermap_data_fields):
				break
			datetime_string = openweathermap_file.replace('.txt', ' ') + data[0]
			data[0] = datetime.strptime(datetime_string, '%Y-%m-%d %H:%M')
			if (len(openweathermap_data['Time']) > 0) and (data[0] <= openweathermap_data['Time'][-1]):
				continue
			is_no_signal = True
			for i in range(1, len(data)):
				if openweathermap_data_fields_plot_mask[i] == 0:
					continue
				data[i] = float(data[i])
				if data[i] > 0:
					is_no_signal = False
			if is_no_signal:
				for i in range(1, len(data)):
					data[i] = NaN
			for i in range(len(data)):
				openweathermap_data[openweathermap_data_fields[i]].append(data[i])

	# Them du lieu openweathermap vao danh sach ve do thi
	for i in range(1, len(openweathermap_data_fields)):
		if openweathermap_data_fields_plot_mask[i] == 1:
			plot_signals.append(
				{'name': openweathermap_data_fields[i],
				'x': np.array(openweathermap_data[openweathermap_data_fields[0]]),
				'y': np.array(openweathermap_data[openweathermap_data_fields[i]])
				})
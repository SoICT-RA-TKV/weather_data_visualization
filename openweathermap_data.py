import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
from collections import namedtuple
from datetime import datetime, timedelta
from utils import *

NaN = np.NaN

# Xu ly du lieu openweathermap
def openweathermap_data(plot_signals, openweathermap_files):
	print("Preprocessing openweathermap data")
	openweathermap_data_fields = ['Time', 'OpenWeatherMap_Main', 'OpenWeatherMap_Description',
		'OpenWeatherMap_Temperature', 'OpenWeatherMap_Pressure',
		'OpenWeatherMap_Humidity', 'OpenWeatherMap_Visibility', 'OpenWeatherMap_WindSpeed',
		'OpenWeatherMap_WindDeg', 'OpenWeatherMap_Clouds']
	openweathermap_data_fields_plot_mask = [1, 0, 0, 1, 0, 1, 1, 0, 0, 0]
	openweathermap_data = dict()
	tmp_openweathermap_data = dict()

	for openweathermap_file in openweathermap_files:
		file = open('./openweathermap/' + openweathermap_file, 'r')
		file.readline()
		while True:
			data = file.readline()
			if data == None:
				break
			data = data.replace(',', '').split('\t')
			if len(data) < len(openweathermap_data_fields):
				break
			datetime_string = openweathermap_file.replace('.txt', ' ') + data[0]
			data[0] = datetime.strptime(datetime_string, '%Y-%m-%d %H:%M')
			is_no_signal = True
			for i in range(1, len(openweathermap_data_fields)):
				try:
					data[i] = float(data[i])
				except:
					data[i] = NaN
				if data[i] != 0:
					is_no_signal = False
			if is_no_signal:
				for i in range(1, len(openweathermap_data_fields)):
					data[i] = NaN
			tmp_datetime = data[0].timestamp()
			tmp_openweathermap_data[tmp_datetime] = dict()
			for i in range(1, len(openweathermap_data_fields)):
				if openweathermap_data_fields[i] == 0:
					continue
				tmp_openweathermap_data[tmp_datetime][openweathermap_data_fields[i]] = data[i]

	openweathermap_data = dict()
	openweathermap_data['Time'] = sorted(list(tmp_openweathermap_data))
	for j in range(1, len(openweathermap_data_fields)):
		if openweathermap_data_fields_plot_mask[j] == 0:
			continue
		openweathermap_data[openweathermap_data_fields[j]] = []
		for i in range(len(openweathermap_data['Time'])):
			openweathermap_data[openweathermap_data_fields[j]].append(tmp_openweathermap_data[openweathermap_data['Time'][i]][openweathermap_data_fields[j]])
	for i in range(len(openweathermap_data['Time'])):
		openweathermap_data['Time'][i] = datetime.fromtimestamp(openweathermap_data['Time'][i])

	openweathermap_data['OpenWeatherMap_Temperature'] = [i - 273.15 for i in openweathermap_data['OpenWeatherMap_Temperature']]
	openweathermap_data['OpenWeatherMap_Temperature'] = normalize(openweathermap_data['OpenWeatherMap_Temperature'], 0, 50)
	openweathermap_data['OpenWeatherMap_Humidity'] = normalize(openweathermap_data['OpenWeatherMap_Humidity'], 0, 100)
	openweathermap_data['OpenWeatherMap_Visibility'] = normalize(openweathermap_data['OpenWeatherMap_Visibility'], 0, 10000)

	style = {'OpenWeatherMap_Temperature': 'm', 'OpenWeatherMap_Humidity': 'y', 'OpenWeatherMap_Visibility': 'k'}
	norm = {'OpenWeatherMap_Temperature': ' 0 - 50', 'OpenWeatherMap_Humidity': ' 0% - 100%', 'OpenWeatherMap_Visibility': ' 0 - 10000(m)'}

	# Them du lieu openweathermap vao danh sach ve do thi
	for i in range(1, len(openweathermap_data_fields)):
		if openweathermap_data_fields_plot_mask[i] == 1:
			plot_signals.append(
				{'name': openweathermap_data_fields[i] + norm[openweathermap_data_fields[i]],
				'style': style[openweathermap_data_fields[i]],
				'x': np.array(openweathermap_data[openweathermap_data_fields[0]]),
				'y': np.array(openweathermap_data[openweathermap_data_fields[i]])
				})
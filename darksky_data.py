import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
from collections import namedtuple
from datetime import datetime, timedelta
from utils import *

NaN = np.NaN

# Xu ly du lieu darksky
def darksky_data(plot_signals, darksky_files):
	print("Preprocessing darksky data")
	darksky_data_fields = ['Time', 'Darksky_Summary', 'Darksky_Icon', 'Darksky_PrecipIntensity', 'Darksky_PrecipProbability',
		'Darksky_PrecipType', 'Darksky_Temperature', 'Darksky_ApparentTemperature',
		'Darksky_DewPoint', 'Darksky_Humidity', 'Darksky_Pressure',
		'Darksky_WinSpeed', 'Darksky_WindGust', 'Darksky_WindBearing',
		'Darksky_CloudCover', 'Darksky_UVIndex', 'Darksky_Visibility', 'Darksky_Ozone']
	darksky_data_fields_plot_mask = [1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
	darksky_data = dict()
	tmp_darksky_data = dict()

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
			is_no_signal = True
			for i in range(1, len(darksky_data_fields)):
				try:
					data[i] = float(data[i])
				except:
					data[i] = NaN
				if data[i] != 0:
					is_no_signal = False
			if is_no_signal:
				for i in range(1, len(data)):
					data[i] = NaN
			tmp_datetime = data[0].timestamp()
			tmp_darksky_data[tmp_datetime] = dict()
			for i in range(1, len(darksky_data_fields)):
				if darksky_data_fields[i] == 0:
					continue
				tmp_darksky_data[tmp_datetime][darksky_data_fields[i]] = data[i]

	darksky_data['Time'] = sorted(list(tmp_darksky_data))
	for j in range(1, len(darksky_data_fields)):
		if darksky_data_fields_plot_mask[j] == 0:
			continue
		darksky_data[darksky_data_fields[j]] = []
		for i in range(len(darksky_data['Time'])):
			darksky_data[darksky_data_fields[j]].append(tmp_darksky_data[darksky_data['Time'][i]][darksky_data_fields[j]])
	for i in range(len(darksky_data['Time'])):
		darksky_data['Time'][i] = datetime.fromtimestamp(darksky_data['Time'][i])

	darksky_data['Darksky_PrecipIntensity'] = [i * 1000 for i in darksky_data['Darksky_PrecipIntensity']]
	darksky_data['Darksky_PrecipIntensity'] = normalize(darksky_data['Darksky_PrecipIntensity'], 0, 50)

	# Them du lieu darksky vao danh sach ve do thi
	for i in range(1, len(darksky_data_fields)):
		if darksky_data_fields_plot_mask[i] == 1:
			plot_signals.append(
				{'name': darksky_data_fields[i] + ' 0-50(mm/h)',
				'style': 'b-',
				'x': np.array(darksky_data[darksky_data_fields[0]]),
				'y': np.array(darksky_data[darksky_data_fields[i]])
				})
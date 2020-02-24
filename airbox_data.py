import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
from collections import namedtuple
from datetime import datetime, timedelta
from utils import *

NaN = np.NaN

# Xu ly du lieu airbox
def airbox_data(plot_signals, airbox_files):
	print("Preprocessing airbox data")
	airbox_data_fields = ['Time', 'Airbox_PM1', 'Airbox_PM25', 'Airbox_PM10', 'Airbox_Temperature', 'Airbox_Humidity']
	airbox_data_fields_plot_mask = [1, 1, 1, 1, 1, 0]
	airbox_data = dict()
	tmp_airbox_data = dict()

	for airbox_file in airbox_files:
		file = open('./airbox/' + airbox_file, 'r')
		file.readline()
		while True:
			data = file.readline()
			if data == None:
				break
			data = data.replace(',', '').split('\t')
			if len(data) < len(airbox_data_fields):
				break
			datetime_string = airbox_file.replace('.txt', ' ') + data[0]
			data[0] = datetime.strptime(datetime_string, '%Y-%m-%d %H:%M')
			is_no_signal = True
			for i in range(1, len(airbox_data_fields)):
				try:
					data[i] = float(data[i])
				except:
					data[i] = NaN
				if data[i] != 0:
					is_no_signal = False
			if is_no_signal:
				for i in range(1, len(airbox_data_fields)):
					data[i] = NaN
			tmp_datetime = data[0].timestamp()
			tmp_airbox_data[tmp_datetime] = dict()
			for i in range(1, len(airbox_data_fields)):
				if airbox_data_fields[i] == 0:
					continue
				tmp_airbox_data[tmp_datetime][airbox_data_fields[i]] = data[i]

	airbox_data = dict()
	airbox_data['Time'] = sorted(list(tmp_airbox_data))
	for j in range(1, len(airbox_data_fields)):
		if airbox_data_fields_plot_mask[j] == 0:
			continue
		airbox_data[airbox_data_fields[j]] = []
		for i in range(len(airbox_data['Time'])):
			airbox_data[airbox_data_fields[j]].append(tmp_airbox_data[airbox_data['Time'][i]][airbox_data_fields[j]])
	for i in range(len(airbox_data['Time'])):
		airbox_data['Time'][i] = datetime.fromtimestamp(airbox_data['Time'][i])

	for i in range(1, 4):
		airbox_data[airbox_data_fields[i]] = normalize(airbox_data[airbox_data_fields[i]], 0, 300)
	airbox_data['Airbox_Temperature'] = normalize(airbox_data['Airbox_Temperature'], 0, 50)

	style = {'Airbox_PM1': 'y--', 'Airbox_PM25': 'g--', 'Airbox_PM10': 'b--', 'Airbox_Temperature': 'r--'}
	norm = {'Airbox_PM1': ' 0-300', 'Airbox_PM25': ' 0-300', 'Airbox_PM10': ' 0-300', 'Airbox_Temperature': ' 0-50'}

	# Them du lieu airbox vao danh sach ve do thi
	for i in range(1, len(airbox_data_fields)):
		if airbox_data_fields_plot_mask[i] == 1:
			plot_signals.append(
				{'name': airbox_data_fields[i] + norm[airbox_data_fields[i]],
				'style': style[airbox_data_fields[i]],
				'x': np.array(airbox_data[airbox_data_fields[0]]),
				'y': np.array(airbox_data[airbox_data_fields[i]])
				})
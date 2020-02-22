import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
from collections import namedtuple
from datetime import datetime, timedelta

NaN = np.NaN

# Xu ly du lieu airbox
def airbox_data(plot_signals, airbox_files):
	print("Preprocessing airbox data")
	airbox_data_fields = ['Time', 'Airbox_PM1', 'Airbox_PM25', 'Airbox_PM10', 'Airbox_Temperature', 'Airbox_Humidity']
	airbox_data_fields_plot_mask = [1, 1, 1, 1, 1, 1]
	airbox_files.sort()
	airbox_data = dict()
	for airbox_data_field in airbox_data_fields:
		airbox_data[airbox_data_field] = []

	for airbox_file in airbox_files:
		file = open('airbox/' + airbox_file, 'r')
		file.readline()
		while True:
			data = file.readline()
			if data == None:
				break
			data = data.replace(',', '').split()
			if len(data) < len(airbox_data_fields):
				break
			datetime_string = airbox_file.replace('.txt', ' ') + data[0]
			data[0] = datetime.strptime(datetime_string, '%Y-%m-%d %H:%M')
			if (len(airbox_data['Time']) > 0) and (data[0] <= airbox_data['Time'][-1]):
				continue
			is_no_signal = True
			for i in range(1, len(data)):
				if airbox_data_fields_plot_mask[i] == 0:
					continue
				try:
					data[i] = float(data[i])
				except:
					data[i] = NaN
				if data[i] > 0:
					is_no_signal = False
			if is_no_signal:
				for i in range(1, len(data)):
					data[i] = NaN
			for i in range(len(data)):
				airbox_data[airbox_data_fields[i]].append(data[i])

	# Them du lieu airbox vao danh sach ve do thi
	for i in range(1, len(airbox_data_fields)):
		if airbox_data_fields_plot_mask[i] == 1:
			plot_signals.append(
				{'name': airbox_data_fields[i],
				'x': np.array(airbox_data[airbox_data_fields[0]]),
				'y': np.array(airbox_data[airbox_data_fields[i]])
				})
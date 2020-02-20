import matplotlib.pyplot as plt
import numpy as np
from collections import namedtuple
from datetime import datetime

# Danh sach file input
airbox_files = ['2020-02-17.txt']
rxpower_files = ['rx614b_1.log', 'rx614b_2.log', 'rx614b_3.log', 'rx614b_4.log', 'rx614b_5.log', 'rx614b_6.log',
'rx614b_7.log', 'rx614b_8.log', 'rx614b_9.log']

def main():
	plot_signals = []
	airbox_data(plot_signals)
	rxpower_data(plot_signals)
	# Ve do thi
	fig, ax = plt.subplots()
	for signal in plot_signals:
		ax.plot(signal['x'], signal['y'], label = signal['name'])
	ax.legend()
	plt.title('PM data')
	plt.savefig('plot.eps', format='eps')
	plt.show()

NaN = np.NaN

# Xu ly du lieu airbox
def airbox_data(plot_signals):
	airbox_data_fields = ['Time', 'PM1', 'PM25', 'PM10', 'Temperature', 'Humidity']
	airbox_data_fields_plot_mask = [1, 1, 1, 1, 1, 1]
	airbox_files.sort()
	airbox_data = dict()
	for airbox_data_field in airbox_data_fields:
		airbox_data[airbox_data_field] = []

	for airbox_file in airbox_files:
		file = open(airbox_file, 'r')
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
				data[i] = float(data[i])
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

# Xu ly du lieu RXPower
def rxpower_data(plot_signals):
	rxpower_files.sort()
	rxpower_data = dict({
		'Time': [],
		'Power': []
		})
	for rxpower_file in rxpower_files:
		file = open(rxpower_file, 'r')
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

if __name__ == '__main__':
	main()
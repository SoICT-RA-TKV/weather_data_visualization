import numpy as np
import matplotlib as mpl
from matplotlib import pyplot as plt
# import pandas as pd
import pymongo
import json
from datetime import datetime, timedelta
from utils import *


def main():
	first_date_string = "2020-02-28 00:00"
	last_date_string = "2020-02-29 00:00"
	first = datetime.strptime(first_date_string, '%Y-%m-%d %H:%M')
	last = datetime.strptime(last_date_string, '%Y-%m-%d %H:%M')

	mongo_client = pymongo.MongoClient("mongodb://sv2.teambit.tech:27017/")
	weather_db = mongo_client['weather']

	plot_signals = json.loads(open('plot.json').read())

	while (first < last):
		plot(first, first + timedelta(days = 1), plot_signals, weather_db)
		first += timedelta(days = 1)

def plot(first, last, plot_signals, weather_db):
	print("Plotting", first.strftime("%Y-%m-%d"), "data")
	# fig, (ax, bx) = plt.subplots(2, figsize = (16, 9), sharex = True)
	fig = plt.figure(figsize = (16, 9))
	ax = fig.add_axes([0.1, 0.4, 0.6, 0.5])
	bx = fig.add_axes([0.1, 0.1, 0.6, 0.2])

	for signal in plot_signals:
		try:
			signal["kwarg"]["label"] = signal["field"] + ' ' + signal["minValue"] + "-" + signal["maxValue"]
		except:
			pass
		tmp_data = weather_db[signal["collection"]].find({"Time": {"$gte": first, "$lt": last}})
		data = []
		for i in tmp_data:
			data.append(i)
		data.sort(key = time_key)
		time = []
		value = []
		for i in range(len(data)):
			time.append(data[i]["Time"])
			value.append(data[i][signal["field"]])
		if (signal["field"] == "OpenWeatherMap_Temperature"):
			for i in range(len(value)):
				value[i] -= 273.15
		value = normalize(value, signal['minValue'], signal['maxValue'])
		if (signal["kwarg"]["label"] == "Wunderground_Condition"):
			continue
		ax.plot(time, value, **signal["kwarg"])

	tmp_data = weather_db["openweathermap"].find({"Time": {"$gte": first, "$lt": last}})
	data = []
	for i in tmp_data:
		data.append(i)
	data.sort(key = time_key)
	time = []
	value = []
	for i in range(len(data)):
		time.append(data[i]["Time"])
		value.append(data[i]["OpenWeatherMap_Description"])
	bx.plot(time, value, label = "OpenWeatherMap_Description")

	ax.legend(bbox_to_anchor = (1, 1))
	bx.legend(bbox_to_anchor = (1, 1))
	# plt.savefig('plot/esp/plot_' + first_date_string.replace(' ', '_') + '.eps', format='eps')
	# plt.savefig('plot/png/plot_' + first.strftime("%Y-%m-%d") + '.png', format='png')
	# plt.rcParams.update({'font.size': 6, 'figure.figsize': (16, 9)})
	plt.title('Weather and Signal Data ' + first.strftime("%Y-%m-%d"))
	mng = plt.get_current_fig_manager()
	# print(type(mng))
	mng.resize(*mng.window.maxsize())
	mng.full_screen_toggle()
	plt.show()

def time_key(obj):
	return obj['Time']

if __name__ == '__main__':
	main()
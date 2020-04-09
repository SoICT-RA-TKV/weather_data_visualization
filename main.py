import numpy as np
import matplotlib as mpl
import matplotlib.patches as mpatches
from matplotlib import pyplot as plt
# import pandas as pd
import pymongo
import json
from datetime import datetime, timedelta
from utils import *
from dotenv import load_dotenv
import os


def main():
	first_date_string = "2020-04-02 00:00"
	last_date_string = "2020-04-04 00:00"
	first = datetime.strptime(first_date_string, '%Y-%m-%d %H:%M')
	last = datetime.strptime(last_date_string, '%Y-%m-%d %H:%M')

	load_dotenv()
	mongo_uri = os.getenv("URI")
	mongo_client = pymongo.MongoClient(mongo_uri)
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
	ax.set_ylim([-0.1, 1.1])
	bx = fig.add_axes([0.1, 0.1, 0.6, 0.2])
	bx.set_ylim([0, 20])

	for signal in plot_signals:
		try:
			signal["kwarg"]["label"] = signal["field"] + ' ' + str(signal["minValue"]) + "-" + str(signal["maxValue"])
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
			if (value[-1] == 0) and (len(value) > 1):
				value[-1] = value[-2]
		if (signal["field"] == "OpenWeatherMap_Temperature"):
			for i in range(len(value)):
				value[i] -= 273.15
		value = normalize(value, signal['minValue'], signal['maxValue'])
		if (signal["field"] == "Wunderground_Condition"):
			continue
		ax.plot(time, value, **signal["kwarg"])

	# Plot condition
	des = json.loads(open('weather_types.json').read())
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
	time = np.array(time)
	value = np.array(value)
	value_id = []
	value_color = dict()
	value_des = dict()
	for v in value:
		v = v.replace(' ', '').replace('_', '')
		value_id.append(des[v]["id"])
		value_color[des[v]["id"]] = des[v]["color"]
		value_des[des[v]["id"]] = v
	value_id = np.array(value_id)
	color_lengend = []
	for i in range(len(des)):
		if i not in value_color:
			continue
		bx.fill_between(time, 0, 20, where = value_id == [i]*len(value_id), color = value_color[i])
		color_lengend.append(mpatches.Patch(color = value_color[i], label = value_des[i]))

	plt.rcParams.update({'legend.loc': 'best'})
	ax.legend(bbox_to_anchor = (1, 1))
	bx.legend(handles = color_lengend, bbox_to_anchor = (1.3, 1))
	plt.savefig('plot/esp/plot_' + first.strftime("%Y-%m-%d") + '.eps', format='eps')
	plt.savefig('plot/png/plot_' + first.strftime("%Y-%m-%d") + '.png', format='png')
	# plt.rcParams.update({'font.size': 6, 'figure.figsize': (16, 9)})
	plt.title('Weather and Signal Data ' + first.strftime("%Y-%m-%d"))
	# mng = plt.get_current_fig_manager()
	# print(type(mng))
	# mng.resize(*mng.window.maxsize())
	# mng.full_screen_toggle()
	# plt.show()

def time_key(obj):
	return obj['Time']

if __name__ == '__main__':
	main()
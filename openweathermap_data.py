import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
from collections import namedtuple
from datetime import datetime, timedelta
from utils import *
import pymongo
import json
import os

mongo_client = pymongo.MongoClient("mongodb://sv2.teambit.tech:27017/")
weather_db = mongo_client['weather']
openweathermap_col = weather_db['openweathermap']

NaN = np.NaN

# Xu ly du lieu openweathermap
def openweathermap_data(openweathermap_files):
	print("Preprocessing openweathermap data")
	openweathermap_data_fields = ['Time', 'OpenWeatherMap_Main', 'OpenWeatherMap_Description',
		'OpenWeatherMap_Temperature', 'OpenWeatherMap_Pressure',
		'OpenWeatherMap_Humidity', 'OpenWeatherMap_Visibility', 'OpenWeatherMap_WindSpeed',
		'OpenWeatherMap_WindDeg', 'OpenWeatherMap_Clouds']

	openweathermap_data = []

	for openweathermap_file in openweathermap_files:
		print(openweathermap_file)
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
					data[i] = data[i]
				if data[i] != 0:
					is_no_signal = False
			if is_no_signal:
				for i in range(1, len(openweathermap_data_fields)):
					data[i] = NaN
			tmp_data = dict()
			for i in range(len(openweathermap_data_fields)):
				tmp_data[openweathermap_data_fields[i]] = data[i]
			openweathermap_col.update_one({'Time': data[0]}, {'$set': tmp_data}, upsert = True)
			# print(tmp_data)
			# print(openweathermap_col.find_one({'Time': data[0]}))


if __name__ == '__main__':
	openweathermap_data(os.listdir('openweathermap/'))
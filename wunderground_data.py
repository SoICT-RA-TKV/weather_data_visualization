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
wunderground_col = weather_db['wunderground']

NaN = np.NaN

# Xu ly du lieu wunderground
def wunderground_data(wunderground_files):
	print("Preprocessing wunderground data")
	wunderground_data_fields = ['Time', 'Wunderground_Temperature', 'Wunderground_DewPoint', 'Wunderground_Humidity', 'Wunderground_Wind',
		'Wunderground_WindSpeed', 'Wunderground_WindGust', 'Wunderground_Pressure',
		'Wunderground_Condition', 'Wunderground_Visibility']

	wunderground_data = []

	for wunderground_file in wunderground_files:
		print(wunderground_file)
		file = open('./wunderground/' + wunderground_file, 'r')
		file.readline()
		while True:
			data = file.readline()
			if data == None:
				break
			data = data.replace(',', '').split('\t')
			if len(data) < len(wunderground_data_fields):
				break
			datetime_string = wunderground_file.replace('.txt', ' ') + data[0]
			data[0] = datetime.strptime(datetime_string, '%Y-%m-%d %H:%M')
			is_no_signal = True
			for i in range(1, len(wunderground_data_fields)):
				try:
					data[i] = float(data[i])
				except:
					pass
				if data[i] != 0:
					is_no_signal = False
			if is_no_signal:
				for i in range(1, len(wunderground_data_fields)):
					data[i] = NaN
			tmp_data = dict()
			for i in range(len(wunderground_data_fields)):
				if wunderground_data_fields[i] == 'Wunderground_Condition':
					data[i] = data[i].split()[0]
				tmp_data[wunderground_data_fields[i]] = data[i]
			wunderground_col.update_one({'Time': data[0]}, {'$set': tmp_data}, upsert = True)
			# print(tmp_data)
			# print(wunderground_col.find_one({'Time': data[0]}))


if __name__ == '__main__':
	wunderground_data(os.listdir('wunderground/'))
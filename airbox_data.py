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
airbox_col = weather_db['airbox']

NaN = np.NaN

# Xu ly du lieu airbox
def airbox_data(airbox_files):
	print("Preprocessing airbox data")
	airbox_data_fields = ['Time', 'Airbox_PM1', 'Airbox_PM25', 'Airbox_PM10', 'Airbox_Temperature', 'Airbox_Humidity']

	airbox_data = []

	for airbox_file in airbox_files:
		print(airbox_file)
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
			tmp_data = dict()
			for i in range(len(airbox_data_fields)):
				tmp_data[airbox_data_fields[i]] = data[i]
			airbox_col.update_one({'Time': data[0]}, {'$set': tmp_data}, upsert = True)
			# print(tmp_data)
			# print(airbox_col.find_one({'Time': data[0]}))


if __name__ == '__main__':
	airbox_data(os.listdir('airbox/'))
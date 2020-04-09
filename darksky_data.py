import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
from collections import namedtuple
from datetime import datetime, timedelta
from utils import *
import pymongo
import json
import os
from dotenv import load_dotenv

load_dotenv()
mongo_uri = os.getenv("URI")
mongo_client = pymongo.MongoClient(mongo_uri)
weather_db = mongo_client['weather']
darksky_col = weather_db['darksky']

NaN = np.NaN

# Xu ly du lieu darksky
def darksky_data(darksky_files):
	print("Preprocessing darksky data")
	darksky_data_fields = ['Time', 'Darksky_Summary', 'Darksky_Icon', 'Darksky_PrecipIntensity', 'Darksky_PrecipProbability',
		'Darksky_PrecipType', 'Darksky_Temperature', 'Darksky_ApparentTemperature',
		'Darksky_DewPoint', 'Darksky_Humidity', 'Darksky_Pressure',
		'Darksky_WinSpeed', 'Darksky_WindGust', 'Darksky_WindBearing',
		'Darksky_CloudCover', 'Darksky_UVIndex', 'Darksky_Visibility', 'Darksky_Ozone']

	darksky_data = []

	for darksky_file in darksky_files:
		print(darksky_file)
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
					data[i] = data[i]
				if data[i] != 0:
					is_no_signal = False
			if is_no_signal:
				for i in range(1, len(darksky_data_fields)):
					data[i] = NaN
			tmp_data = dict()
			for i in range(len(darksky_data_fields)):
				tmp_data[darksky_data_fields[i]] = data[i]
			darksky_col.update_one({'Time': data[0]}, {'$set': tmp_data}, upsert = True)
			# print(tmp_data)
			# print(darksky_col.find_one({'Time': data[0]}))


if __name__ == '__main__':
	darksky_data(os.listdir('darksky/'))
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
rxpower_col = weather_db['rxpower']

NaN = np.NaN

# Xu ly du lieu rxpower
def rxpower_data(rxpower_files):
	print("Preprocessing rxpower data")
	rxpower_data_fields = ['Time', 'Power']

	rxpower_data = []
	loss = 0

	if rxpower_col.find_one({'Time': 'hihi'}) == None:
		print("Hello")

	for rxpower_file in rxpower_files:
		print(rxpower_file)
		file = open(rxpower_file, 'r')
		while True:
			data = file.readline()
			if data == None:
				break
			if (data.find("***") >= 0) or (data.find("CONFIG") >= 0):
				continue
			data = data.split(',')
			if len(data) < 4:
				break
			datetime_string = data[0] + ' ' + data[1]
			data[0] = datetime.strptime(datetime_string, '%m/%d/%Y %H:%M:%S')
			data[1] = float(data[2])
			tmp_data = dict()
			for i in range(len(rxpower_data_fields)):
				tmp_data[rxpower_data_fields[i]] = data[i]
			# rxpower_col.update_one({'Time': data[0]}, {'$set': tmp_data}, upsert = True)
			# print(tmp_data)
			# print(rxpower_col.find_one({'Time': data[0]}))
			if rxpower_col.find_one({'Time': data[0]}) == None:
				loss += 1
				print("Loss data:", tmp_data)
				rxpower_col.update_one({'Time': data[0]}, {'$set': tmp_data}, upsert = True)
	print(loss)


if __name__ == '__main__':
	rxpower_files = []
	rxpower_folders = ['rxpower/Collect20200224/', 'rxpower/Collect20200311/', 'rxpower/Collect20200320/']
	for folder in rxpower_folders:
		files = os.listdir(folder)
		for file in files:
			rxpower_files.append(folder + file)
	rxpower_data(rxpower_files)
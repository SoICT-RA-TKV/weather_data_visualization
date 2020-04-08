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
rxpower_col = weather_db['rxpower']

NaN = np.NaN

# Xu ly du lieu rxpower
def rxpower_data(rxpower_files):
	print("Preprocessing rxpower data")
	rxpower_data_fields = ['Time', 'Power']

	rxpower_data = []
	loss = 0

	done = []
	try:
		f = open('rxpower_done.txt', 'r')
		done = f.read().split('\n')
		f.close()
	except:
		pass

	for rxpower_file in rxpower_files:
		f = open('rxpower_done.txt', 'a')
		if rxpower_file in done:
			continue
		print(rxpower_file)
		file = open(rxpower_file, 'r')
		existed = 0
		new = 0
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
			if rxpower_col.find_one({'Time': data[0]}) == None:
				new += 1
				rxpower_col.update_one({'Time': data[0]}, {'$set': tmp_data}, upsert = True)
				print("New " + str(new) + ": ", {'Time': data[0]}, {'$set': tmp_data})
			else:
				existed += 1
				print("Exsited " + str(existed) + ": ", {'Time': data[0]}, {'$set': tmp_data})
		f.write(rxpower_file + '\n')
		f.close()


if __name__ == '__main__':
	rxpower_files = []
	rxpower_folders = []
	rxpower_children = os.listdir('rxpower')
	for c in rxpower_children:
		tmp_path = 'rxpower/' + c + '/'
		if os.path.isdir(tmp_path):
			rxpower_folders.append(tmp_path)
	print(rxpower_folders)
	for folder in rxpower_folders:
		files = os.listdir(folder)
		for file in files:
			rxpower_files.append(folder + file)
	rxpower_data(rxpower_files)
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

def main():
	processor = import_json
	rxpower_files = list_files('rxpower')
	processor(rxpower_files)

def list_files(folder):
	rxpower_files = []
	rxpower_folders = []
	rxpower_children = os.listdir(folder)
	for c in rxpower_children:
		tmp_path = folder + '/' + c + '/'
		if os.path.isdir(tmp_path):
			rxpower_folders.append(tmp_path)
	print(rxpower_folders)
	for folder in rxpower_folders:
		files = os.listdir(folder)
		for file in files:
			rxpower_files.append(folder + file)
	return rxpower_files

def load_env():
	load_dotenv()
	mongo_uri = os.getenv("URI")
	mongo_client = pymongo.MongoClient(mongo_uri)
	weather_db = mongo_client['weather']
	rxpower_col = weather_db['rxpower']
	return rxpower_col

def upload_from_log(rxpower_files):
	rxpower_col = load_env()
	NaN = np.NaN

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

def count(rxpower_files):
	print("Preprocessing rxpower data")

	time = set()
	for rxpower_file in rxpower_files:
		if not rxpower_file.endswith('.log'):
			continue
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
			time.add(int(data[0].timestamp()))
	print(len(time))

def import_json(rxpower_files):
	print("Preprocessing rxpower data")

	for rxpower_file in rxpower_files:
		if not rxpower_file.endswith('.json'):
			continue
		print(rxpower_file)
		# mongoimport rx614b_9.json -d weather -c rxpower --upsert
		cmd = "mongoimport --mode=merge -d weather -c rxpower %s" % rxpower_file
		print(cmd)
		os.system(cmd)

def log_to_json(rxpower_files):
	print("Preprocessing rxpower data")

	for rxpower_file in rxpower_files:
		if not rxpower_file.endswith('.log'):
			continue
		print(rxpower_file)
		file = open(rxpower_file, 'r')
		jsonfile = open(rxpower_file.split('.')[0] + '.json', 'w')
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
			tmp_data = {"Time": {"$date": {"$numberLong": str(1000 * int(data[0].timestamp()))}}, "Power": {"$numberDouble": str(data[1])}}
			jsonfile.write(json.dumps(tmp_data) + '\n')
		file.close()
		jsonfile.close()

if __name__ == '__main__':
	main()
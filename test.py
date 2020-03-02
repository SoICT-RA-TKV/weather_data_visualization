import pymongo
import numpy as np

mongo_client = pymongo.MongoClient("mongodb://sv2.teambit.tech:27017/")
weather_db = mongo_client['weather']
collection = weather_db['openweathermap']

description = set()
main = set()

print("Collecting document")
data = collection.find()

print("Filtering document")
for d in data:
	if type(d['OpenWeatherMap_Main']) == str:
		main.add(d['OpenWeatherMap_Main'].replace(' ', ''))
	else:
		main.add('No_Info')
	if type(d['OpenWeatherMap_Description']) == str:
		description.add(d['OpenWeatherMap_Description'].replace(' ', ''))
	else:
		description.add('No_Info')

print(len(description))
print(description)

print(len(main))
print(main)
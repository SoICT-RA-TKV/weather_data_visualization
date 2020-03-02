import numpy as np

def normalize(data, min_value, max_value, min_norm=0, max_norm=1):
	try:
		range_value = max_value - min_value
	except:
		return data
	range_norm = max_norm - min_norm
	k = range_norm / range_value
	for i in range(len(data)):
		if data[i] == np.NaN:
			continue
		try:
			data[i] = min_norm + (data[i] - min_value) * k
		except:
			pass
	return data
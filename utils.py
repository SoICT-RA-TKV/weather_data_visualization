import numpy as np

def normalize(data, min_value, max_value, min_norm=0, max_norm=1):
	range_value = max_value - min_value
	range_norm = max_norm - min_norm
	k = range_norm / range_value
	for i in range(len(data)):
		if data[i] == np.NaN:
			continue
		data[i] = min_norm + (data[i] - min_value) * k
	return data
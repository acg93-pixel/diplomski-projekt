import numpy as np
import time
from config import  conf
import os
import cv2

data = np.load('/home/ceja/Documents/projekt/stats/stats.npy')
stats = {}
stats['mean_size'] = np.mean(data)
stats['max_size'] = np.max(data)
stats['min_size'] = np.min(data)

print(stats['mean_size'])
print(stats['max_size'])
print(stats['min_size'])
print data


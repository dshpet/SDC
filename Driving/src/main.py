#!/usr/bin/env python 

'''
Main processing logic. 
Incorporates machine learning and computer vision in a free manner.

Run through Anaconda python distrib on Windows 10

OpenCV
https://stackoverflow.com/questions/23119413/how-do-i-install-python-opencv-through-conda
'''

import numpy as np
import cv2
from PIL import ImageGrab

def screen_record():
	while True:
		# 800x600 window
		printscreen = np.array(ImageGrab.grab(bbox=(0, 40, 800, 640)))

		cv2.imshow('window', cv2.cvtColor(printscreen, cv2.COLOR_BGR2RGB))

		if cv2.waitKey(25) & 0xFF == ord('q'):
			cv2.destroyAllWindows()
			break

screen_record()
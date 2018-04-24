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

def process_image(_image):
  processed_image = cv2.cvtColor(_image, cv2.COLOR_BGR2GRAY)
  processed_image = cv2.Canny(processed_image, threshold1 = 200, threshold2 = 300)

  return processed_image


def main():
  while True:
    # 800x600 window
    screen = np.array(ImageGrab.grab(bbox=(0, 40, 800, 640)))
    processed_screen = process_image(screen)

    cv2.imshow('window', processed_screen)
    #cv2.imshow('window', cv2.cvtColor(screen, cv2.COLOR_BGR2RGB))

    if cv2.waitKey(25) & 0xFF == ord('q'):
      cv2.destroyAllWindows()
      break

main()
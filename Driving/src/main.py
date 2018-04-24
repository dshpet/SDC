#!/usr/bin/env python 

'''
Main processing logic. 
Incorporates machine learning and computer vision in a free manner.

Run through Anaconda python distrib on Windows 10

OpenCV
https://stackoverflow.com/questions/23119413/how-do-i-install-python-opencv-through-conda

pyautogui (not the latest version as a lot of packages change)
https://anaconda.org/conda-forge/pyautogui
'''

import numpy as np
import cv2
import time
from PIL import ImageGrab
import inputsimulator as input

# todo use it on other simulators with direct input processing
# terminal takes the input
# from inputsimulator import PressKey, W, A, S, D

def process_image(_image):
  processed_image = cv2.cvtColor(_image, cv2.COLOR_BGR2GRAY)
  processed_image = cv2.Canny(processed_image, threshold1 = 200, threshold2 = 300)

  return processed_image

def main():
  while True:
    # todo change
    input.PressKeyIndirect('w') 

    # 800x600 window
    screen = np.array(ImageGrab.grab(bbox=(0, 40, 800, 640)))
    processed_screen = process_image(screen)

    cv2.imshow('SDC_driver', processed_screen)
    #cv2.imshow('SDC_driver', cv2.cvtColor(screen, cv2.COLOR_BGR2RGB))

    if cv2.waitKey(25) & 0xFF == ord('q'):
      cv2.destroyAllWindows()
      break

main()
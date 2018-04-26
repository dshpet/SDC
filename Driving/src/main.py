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
# from inputsimulator import ReleaseKey, PressKey, W, A, S, D


def get_road_lanes(_image, _lines):
  # sometimes crashes
  if _lines is None:
    return

  # if this fails, go with some default line
  try:  
    # finds the maximum y value for a lane marker 
    # (since we cannot assume the horizon will always be at the same point.)
    ys = []  
    for i in _lines:
      for ii in i:
        ys += [ii[1], ii[3]]

    min_y = min(ys)
    max_y = 600
    new_lines = []
    line_dict = {}
  
    for idx, i in enumerate(_lines):
      for xyxy in i:
        # These four lines:
        # modified from http://stackoverflow.com/questions/21565994/method-to-return-the-equation-of-a-straight-line-given-two-points
        # Used to calculate the definition of a line, given two sets of coords.
        x_coords = (xyxy[0], xyxy[2])
        y_coords = (xyxy[1], xyxy[3])
        A = vstack([x_coords, ones(len(x_coords))]).T
        m, b = lstsq(A, y_coords)[0]
  
        # Calculating our new, and improved, xs
        x1 = (min_y - b) / m
        x2 = (max_y - b) / m
  
        line_dict[idx] = [m, b, [int(x1), min_y, int(x2), max_y]]
        new_lines.append([int(x1), min_y, int(x2), max_y])
  
    final_lanes = {}
  
    for idx in line_dict:
      final_lanes_copy = final_lanes.copy()
      m = line_dict[idx][0]
      b = line_dict[idx][1]
      line = line_dict[idx][2]
      
      if len(final_lanes) == 0:
        final_lanes[m] = [ [m, b, line] ]
          
      else:
        found_copy = False
  
        for other_ms in final_lanes_copy:
          if not found_copy:
            if abs(other_ms * 1.2) > abs(m) > abs(other_ms * 0.8):
              if abs(final_lanes_copy[other_ms][0][1] * 1.2) > abs(b) > abs(final_lanes_copy[other_ms][0][1] * 0.8):
                final_lanes[other_ms].append([m, b, line])
                found_copy = True
                break
            else:
              final_lanes[m] = [ [m, b, line] ]
  
    line_counter = {}
  
    for lanes in final_lanes:
      line_counter[lanes] = len(final_lanes[lanes])
  
    top_lanes = sorted(line_counter.items(), key = lambda item: item[1])[::-1][:2]
  
    lane1_id = top_lanes[0][0]
    lane2_id = top_lanes[1][0]
  
    def average_lane(_lane_data):
      x1s = []
      y1s = []
      x2s = []
      y2s = []

      for data in _lane_data:
        x1s.append(data[2][0])
        y1s.append(data[2][1])
        x2s.append(data[2][2])
        y2s.append(data[2][3])

      return int(mean(x1s)), int(mean(y1s)), int(mean(x2s)), int(mean(y2s)) 
  
    l1_x1, l1_y1, l1_x2, l1_y2 = average_lane(final_lanes[lane1_id])
    l2_x1, l2_y1, l2_x2, l2_y2 = average_lane(final_lanes[lane2_id])
  
    return [l1_x1, l1_y1, l1_x2, l1_y2], [l2_x1, l2_y1, l2_x2, l2_y2]

  except Exception as e:
    print(str(e))

def roi(_image, _vertices):
  mask = np.zeros_like(_image)
  cv2.fillPoly(mask, _vertices, 255)

  masked = cv2.bitwise_and(_image, mask)
  
  return masked

def process_image(_image):
  original_image = _image

  processed_image = cv2.cvtColor(_image, cv2.COLOR_BGR2GRAY)
  processed_image = cv2.GaussianBlur(processed_image, (5, 5), 0)
  processed_image = cv2.Canny(processed_image, threshold1 = 200, threshold2 = 300)

  # only bottom part of the image (road)
  vertices = np.array(
      [
        [ 10, 500],
        [ 10, 300],
        [300, 200],
        [500, 200],
        [800, 300],
        [800, 500],
      ], 
      np.int32
    )  
  processed_image = roi(processed_image, [vertices])

  # http://docs.opencv.org/3.0-beta/doc/py_tutorials/py_imgproc/py_houghlines/py_houghlines.html
  # edges, rho, theta, threshold, min length, max gap
  lines = cv2.HoughLinesP(processed_image, 1, np.pi / 180, 180, 20, 15)
  try:
    l1, l2 = get_road_lanes(original_image, lines)

    color     = [0, 255, 0]
    thickness = 30
    cv2.line(original_image, (l1[0], l1[1]), (l1[2], l1[3]), color, thickness)
    cv2.line(original_image, (l2[0], l2[1]), (l2[2], l2[3]), color, thickness)

  except Exception as e:
    print(str(e))
    pass

  try:
    for coords in lines:
      coords = coords[0]
      try:
        color     = [0, 255, 0]
        thickness = 30
        cv2.line(processed_image, (coords[0], coords[1]), (coords[2], coords[3]), color, thickness)

      except Exception as e:
        print(str(e))
  
  except Exception as e:
    pass

  return processed_image, original_image

def main():
  while True:
    # todo change
    # input.PressKeyIndirect('w') 

    # 800x600 window
    screen = np.array(ImageGrab.grab(bbox=(0, 40, 800, 640)))
    processed_screen, original_screen = process_image(screen)

    cv2.imshow('SDC_driver', processed_screen)
    #cv2.imshow('SDC_driver', cv2.cvtColor(screen, cv2.COLOR_BGR2RGB))

    if cv2.waitKey(25) & 0xFF == ord('q'):
      cv2.destroyAllWindows()
      break

main()
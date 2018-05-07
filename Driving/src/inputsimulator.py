#!/usr/bin/env python 

'''
Input simulation to surpass Direct input method needed for some simulators
[Windows only]

Useful sources
http://stackoverflow.com/questions/14489013/simulate-python-keypresses-for-controlling-a-game
http://www.gamespp.com/directx/directInputKeyboardScanCodes.html

pyautogui (not the latest version as a lot of packages change)
https://anaconda.org/conda-forge/pyautogui
'''

import ctypes
import pyautogui
import time

SendInput = ctypes.windll.user32.SendInput

# todo use proper keycodes
W = 0x11
A = 0x1E
S = 0x1F
D = 0x20

#
# C struct redefinitions 
#

PUL = ctypes.POINTER(ctypes.c_ulong)

class KeyBdInput(ctypes.Structure):
  _fields_ = [
      ("wVk",         ctypes.c_ushort),
      ("wScan",       ctypes.c_ushort),
      ("dwFlags",     ctypes.c_ulong ),
      ("time",        ctypes.c_ulong ),
      ("dwExtraInfo", PUL            )
    ]

class HardwareInput(ctypes.Structure):
  _fields_ = [
      ("uMsg",    ctypes.c_ulong ),
      ("wParamL", ctypes.c_short ),
      ("wParamH", ctypes.c_ushort)
    ]

class MouseInput(ctypes.Structure):
  _fields_ = [
      ("dx",          ctypes.c_long ),
      ("dy",          ctypes.c_long ),
      ("mouseData",   ctypes.c_ulong),
      ("dwFlags",     ctypes.c_ulong),
      ("time",        ctypes.c_ulong),
      ("dwExtraInfo", PUL           )
    ]

class Input_I(ctypes.Union):
  _fields_ = [
      ("ki", KeyBdInput   ),
      ("mi", MouseInput   ),
      ("hi", HardwareInput)
    ]

class Input(ctypes.Structure):
  _fields_ = [
      ("type", ctypes.c_ulong),
      ("ii",   Input_I       )
    ]

#
# Interface
#

def PressKey(_hexKeyCode):
  extra  = ctypes.c_ulong(0)
  ii_    = Input_I()
  ii_.ki = KeyBdInput(0, _hexKeyCode, 0x0008, 0, ctypes.pointer(extra))
  x      = Input(ctypes.c_ulong(1), ii_)

  ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

def ReleaseKey(_hexKeyCode):
  extra  = ctypes.c_ulong(0)
  ii_    = Input_I()
  ii_.ki = KeyBdInput(0, _hexKeyCode, 0x0008 | 0x0002, 0, ctypes.pointer(extra))
  x      = Input(ctypes.c_ulong(1), ii_)

  ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

def PressKeyIndirect(_key):
  pyautogui.keyDown(_key)

def ReleaseKeyIndirect(_key):
  pyautogui.keyUp(_key)

#
# High level abstract input
#

def straight():
    PressKey(W)
    ReleaseKey(A)
    ReleaseKey(D)

def left():
    PressKey(A)
    ReleaseKey(W)
    ReleaseKey(D)
    ReleaseKey(A)

def right():
    PressKey(D)
    ReleaseKey(A)
    ReleaseKey(W)
    ReleaseKey(D)

def slow_ya_roll():
    ReleaseKey(W)
    ReleaseKey(A)
    ReleaseKey(D)
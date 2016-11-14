import os
import sys
import subprocess

def function():
    functionReturn = os.system('matlab.exe -nodesktop -nosplash -r C:/Users/undergradSTUDENT_1/Documents/aces/matlab/driver/beach_nourishment.m')
    #return functionReturn

def start():
    call = function()
    string = "This is the 'start' function calling matlab"
    return string

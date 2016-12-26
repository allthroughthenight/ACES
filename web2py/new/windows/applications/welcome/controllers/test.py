import os
import sys
import subprocess

def function():
    functionReturn = "function call"
    return functionReturn

def hello():
    call = function()
    string = "This is the 'hello' function plus the " + call
    return string

import os
import sys
import subprocess

def listing():
    ls = os.system("ls")
    return ls

def hello():
    directory = listing()
    return "This is the 'main' call with the directory listing: %i" % directory

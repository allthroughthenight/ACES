import os
import sys
import subprocess

def hello():
    directory = os.system("ls")
    return "The directory listing is %i" % directory

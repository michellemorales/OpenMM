#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

Created on Thurs Oct 05 07:36:55 2017

@author: michellemorales
"""

#!/usr/bin/python
import sys
import os
from Tkinter import *
import FeatureExtract
import json
import tkMessageBox


def run():
    global pars
    ibm_pass = str(pars["IBM_PASSWORD"])
    ibm_un = str(pars["IBM_USERNAME"])
    openface = str(pars["OPENFACE"])
    # TODO:perform video analysis
    print "Running OpenFace..."
    FeatureExtract.extract_visual("/Users/morales/GitHub/OpenMM/examples/FerrisBuellerClip.mp4", openface)
    # Perform audio analysis
    print "Running Covarep..."
    # FeatureExtract.extract_audio("/Users/morales/GitHub/OpenMM/examples/")
    # Perform speech-to-text
    print "Running speech-to-text..."
    FeatureExtract.ibm_speech2text("/Users/morales/GitHub/OpenMM/examples/FerrisBuellerClip.wav", 'en-US', ibm_un , ibm_pass)
    # Perform linguistic analysis
    # Output prediction


# Get config parameters
config = "/Users/morales/Desktop/config.json"
json_file = open(config, "r").read()
pars = json.loads(json_file)
# Make pars global

win = Tk()
win.title("OpenMM")
L = Label(win, text="Please choose a video:")
B = Button(win,text="Run OpenMM", command= run)
L.pack()
B.pack(padx=50, pady=50)
win.mainloop()


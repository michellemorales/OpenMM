#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

Created on Thurs Oct 05 07:36:55 2017

@author: michellemorales
"""

#!/usr/bin/python
import sys
import os
import Tkinter
import FeatureExtract
import tkMessageBox
top=Tkinter.Tk()
top.title("OpenMM")

def run():


B=Tkinter.Button(top,text="Run OpenMM",command= helloCallBack)
B.pack()
top.mainloop()
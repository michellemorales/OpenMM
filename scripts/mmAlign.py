#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 30 07:36:55 2017

@author: michellemorales
"""

import sys

sys.path.insert(0, '~/GitHub/OpenMM/gentle')

import align


def force_align(audio, text):
    """Align audio and transcript using gentle"""
    align(audio, text)


audio, text = sys.argv[1:]
force_align(audio, text)
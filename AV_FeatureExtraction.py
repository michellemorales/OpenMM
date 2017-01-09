#Michelle Morales
#Dissertation Work 2017

#This script can be used to perform AV (audiovisual) feature extraction using the OpenFace and COVAREP repos

### OpenFace ###
#Feature extraction with OpenFace
#ToDo
#function that takes video as input
#creates new csv for output
#runs feature extraction: OpenFace/bin/FeatureExtraction -f /path/to/mov -of /path/to/.csv

#Extract audio (wav) from video - ffmpeg -i Example.mov -vn -acodec pcm_s16le -ar 44100 -ac 2 Example.wav

### COVAREP ###
#Feature extraction with covarep
#ToDo
#figure out how to call matlab functions in python
#function that takes audio as input and creates csv and writes features to
#covarep/feature_extraction/COVAREP_feature_extraction.m


### Dependencies ###
# OpenFace
# ffmpeg
# Covarep

import sys, os, subprocess

def extract_visual(video, csv):
    #Extracts visual features using OpenFace, requires the OpenFace () repo to be installed
    pathOpenFace =''
    print 'Launching OpenFace to extract visual features... \n\n\n\n\n'
    command = '/Users/morales/GitHub/OpenFace/bin/FeatureExtraction -f %s -of %s'%(video, csv)
    subprocess.call(command, shell=True)
    print 'DONE! Visual features saved to %s' %csv

def video2audio(video):
    #Converts video to audio using ffmpeg, requires ffmpeg to be installed
    wav = video.replace('.mov','.wav')
    command = 'ffmpeg -i %s -vn -acodec pcm_s16le -ar 44100 -ac 2 %s'%(video, wav)
    subprocess.call(command, shell=True)
    print 'DONE! Video converted to audio file: %s'%wav

def extract_audio(audio, csv):
    #Extracts audio features using COVAREP, requires the Covarep repo ()

# extract_visual('/Users/morales/Desktop/Example.mov','/Users/morales/Desktop/test.csv')
# video2audio('/Users/morales/Desktop/Example.mov')

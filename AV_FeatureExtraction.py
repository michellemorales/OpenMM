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
#/Applications/MATLAB_R2016a.app/bin/matlab -nodisplay -nosplash -nodesktop -r "COVAREP_feature_extraction('/Users/morales/Desktop/');exit"


### Dependencies ###
# OpenFace
# ffmpeg
# Covarep
# Matlab

import sys, os, subprocess
import speech_recognition as sr

def extract_visual(video, csv):
    #Extracts visual features using OpenFace, requires the OpenFace () repo to be installed
    pathOpenFace =''
    newF = open(csv,'w')
    print 'Launching OpenFace to extract visual features... \n\n\n\n\n'
    command = '/Users/morales/GitHub/OpenFace/bin/FeatureExtraction -f %s -of %s'%(video, csv)
    subprocess.call(command, shell=True)
    print 'DONE! Visual features saved to %s' %csv

def video2audio(video):
    #Converts video to audio using ffmpeg, requires ffmpeg to be installed
    wav = video.replace('.mp4','.wav')
    command = 'ffmpeg -i %s -vn -acodec pcm_s16le -ar 44100 -ac 2 %s'%(video, wav)
    subprocess.call(command, shell=True)
    print 'DONE! Video converted to audio file: %s'%wav

def extract_audio(audio_dir):
    #covarep operates on directory of files
    #Extracts audio features using COVAREP, requires the Covarep repo and matlab
    command = '/Applications/MATLAB_R2016a.app/bin/matlab -nodisplay -nosplash -nodesktop -r '+ '"COVAREP_feature_extraction(%s);exit"'%("'"+audio_dir+"'")
    print command
    subprocess.call(command, shell=True)
    print 'DONE! Audio features saved to .mat file in %s directory.' %audio_dir

def speech2text(audio_file,lang):
    GOOGLE_SPEECH_RECOGNITION_API_KEY = 'AIzaSyCQNG-Jeageo_myq7MJTBzoxAdSq8oqASc'
    ### TODO: FIX THIS FUNCTION ###
    r = sr.Recognizer()
    with sr.AudioFile(audio_file) as source:
        audio = r.record(source)
    # recognize speech using Google Speech Recognition
    try:
    # for testing purposes, we're just using the default API key
    # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
    # instead of `r.recognize_google(audio)`
        print("Google Speech Recognition thinks you said " + r.recognize_google(audio, key=GOOGLE_SPEECH_RECOGNITION_API_KEY, language=lang))
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))

extract_visual('FerrisBuellerClip.mp4','FBTest.csv')
video2audio('FerrisBuellerClip.mp4')
extract_audio('/Users/morales/GitHub/Dissertation')
speech2text('FerrisBuellerClip.wav','en-US')

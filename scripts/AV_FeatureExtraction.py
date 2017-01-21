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
# Matlab

import sys, os, subprocess, ling_analysis
import speech_recognition as sr

def extract_visual(video):
    #Extracts visual features using OpenFace, requires the OpenFace () repo to be installed
    pathOpenFace =''
    csv = video.replace('.mp4','.csv')
    newF = open(csv,'w')
    print 'Launching OpenFace to extract visual features... \n\n\n\n\n'
    command = '/Users/morales/GitHub/OpenFace/bin/FeatureExtraction -f %s -of %s'%(video, csv)
    subprocess.call(command, shell=True)
    print 'DONE! Visual features saved to %s' %csv

def video2audio(video):
    #Converts video to audio using ffmpeg, requires ffmpeg to be installed
    wav = video.replace('.mp4','.wav')
    command = 'ffmpeg -i %s -acodec pcm_s16le -ac 1 -ar 16000 %s'%(video, wav)
    subprocess.call(command, shell=True)
    print 'DONE! Video converted to audio file: %s'%wav

def extract_audio(audio_dir):
    #covarep operates on directory of files
    #Extracts audio features using COVAREP, requires the Covarep repo and matlab
    command = '/Applications/MATLAB_R2016a.app/bin/matlab -nodisplay -nosplash -nodesktop -r '+ '"COVAREP_feature_extraction(%s);exit"'%("'"+audio_dir+"'")
    print command
    subprocess.call(command, shell=True)
    print 'DONE! Audio features saved to .mat file in %s directory.' %audio_dir

def google_speech2text(audio_file,lang):
    GOOGLE_SPEECH_RECOGNITION_API_KEY = 'AIzaSyCQNG-Jeageo_myq7MJTBzoxAdSq8oqASc'
    r = sr.Recognizer()
    with sr.AudioFile(audio_file) as source:
        audio = r.record(source)
    #Recognize speech using Google Speech Recognition
    try:
        print("Google Speech Recognition thinks you said " + r.recognize_google(audio, key=GOOGLE_SPEECH_RECOGNITION_API_KEY, language=lang))
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))

def speech2text(audio_file,lang):
    IBM_USERNAME = "28e8d133-29a7-477e-9544-d3ac977218ab"
    IBM_PASSWORD = "JPyxiE3a4ADK"
    r = sr.Recognizer()
    with sr.AudioFile(audio_file) as source:
        audio = r.record(source)
    #Recognize speech using IBM Speech to Text
    try:
        result = r.recognize_ibm(audio, username=IBM_USERNAME, password=IBM_PASSWORD, language='en-US') #show_all=True - returns json
        print(result)
    except sr.UnknownValueError:
        print("IBM Speech to Text could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from IBM Speech to Text service; {0}".format(e))


if __name__ == '__main__':
    extract_visual('../FerrisBuellerClip.mp4')
    video2audio('../FerrisBuellerClip.mp4')
    extract_audio('/Users/morales/GitHub/Dissertation')
    transcript = speech2text('../FerrisBuellerClip.wav','en-US')
    ling_analysis(transcript)

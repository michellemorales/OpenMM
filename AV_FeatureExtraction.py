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

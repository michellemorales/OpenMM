#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 30 07:36:55 2017

@author: michellemorales
"""

from collections import defaultdict
from nltk.tag import pos_tag
from nltk.tokenize import word_tokenize
from pydub import AudioSegment
import subprocess
import pandas
import json
import os
import LingAnalysis
import FeatureExtract
import numpy as np
from python_speech_features import mfcc
import scipy.io.wavfile as wav


def force_align(wav_file, text):
    """Align audio and transcript using gentle"""
    command = "python /Users/michellemorales/GitHub/gentle/align.py %s %s" % (wav_file, text)
    output = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE).stdout.read()
    return output


def trim_audio(start, end, wav_file, new_wav):
    newAudio = AudioSegment.from_wav(wav_file)
    newAudio = newAudio[start:end] # pydub works with milliseconds
    newAudio.export(new_wav, format="wav")


def get_mfccs(wav_file):
    (rate, sig) = wav.read(wav_file)
    mfcc_feat = mfcc(sig, rate)
    return mfcc_feat


def get_features(wav_file, text, csv_name):
    """
    :param text: a csv with interview data from DAIC
    """
    univ_tags = LingAnalysis.load_tags()
    df = pandas.read_csv(text, delimiter='\t')
    # df = df.iloc[:15]
    # Save audio features for each POS tag
    features = defaultdict(list)
    for row in df.iterrows():
        row = row[1]
        start, end, speaker, sent = row['start_time'], row['stop_time'], row['speaker'], row['value']
        if speaker == 'Participant':
            words = sent.split()
            if len(words) > 2:

                try:
                    # Create a temporary clip
                    trim_audio(start * 1000, end * 1000, wav_file,
                               "clip.wav")  # convert to millisec because pydub requries that
                    # Create a temporary transcript
                    with open('transcript.txt', 'w') as f:
                        f.write(sent)
                    sent_clip = 'clip.wav'
                    alignment = force_align(sent_clip, 'transcript.txt')
                    align_dict = json.loads(alignment)
                    # Get tags
                    tokens = word_tokenize(align_dict['transcript'])
                    tags = pos_tag(tokens, tagset='universal', lang='eng')
                    # Get covarep features for wav clip
                    FeatureExtract.extract_audio('.')
                    # Get features from covarep file
                    print sent
                    covarep = pandas.read_csv('clip_covarep.csv')
                    covarep.drop(covarep.columns[len(covarep.columns) - 1], axis=1, inplace=True)
                    covarep_header = covarep.columns
                    # print covarep_header
                    # print covarep
                    # print len(covarep_header)
                    # Create a dir to write wav clips to
                    # if not os.path.exists('wavs'):
                    #     os.makedirs('wavs')
                    for i, word_dict in enumerate(align_dict['words']):
                        start = word_dict['start']
                        end = word_dict['end']
                        word = word_dict["alignedWord"]
                        tag = tags[i][1]
                        start_frame, end_frame = int(start * 100), int(end*100)
                        frames = covarep.iloc[start_frame:end_frame]
                        # print word, tag, start_frame, end_frame
                        # print "Number of frames = ", len(frames)
                        # Add features from frame to dictionary

                        for row in frames.iterrows():
                            feats = row[1].values.tolist()
                            features[tag].append(feats) # Save features to tag
                    # Delete sentence related files
                    os.remove('clip.wav')
                    os.remove('transcript.txt')
                    os.remove('clip_covarep.csv')
                except (IOError, KeyError, IndexError) as e:
                    # If covarep features don't exist, we ignore sentence
                    # If gentle can't align sentence and audio we align
                    pass
    # Get average vector across all features per tag
    # If tag does not exist in transcript, assign an empty vector to tag
    combined_header = []
    header = sorted(univ_tags)

    for tag in header:
        for name in covarep_header:
            combine = tag+'_'+name
            combined_header.append(combine)
    avg_features = []

    for tag in header:
        if tag in features.keys():
            # Get average
            avg = np.mean(features[tag], axis=0)
            avg_features.append(avg)
        elif tag not in features.keys():
            # Assign an empty vector to tag
            empty_f =[0] * 74
            avg_features.append(empty_f)

    # Create new csv
    new_csv = open(csv_name,'w')
    new_csv.write(','.join(combined_header)+'\n')
    combine_features = []
    for f_list in avg_features:
        for f in f_list:
            combine_features.append(str(f))
    new_csv.write(','.join(combine_features))



#Michelle Morales
#Script performs linguistic analysis for languages other than English

from __future__ import division
from collections import defaultdict
from gensim.models import word2vec
import sys, re, pandas, numpy, os, subprocess, json, os.path

def bag_of_words(dir):
    files = [f for f in os.listdir(dir) if f.endswith('_transcript.json')]
    all_words = []
    for file_name in files:
        with open(os.path.join(dir,file_name)) as data_file:
            data = json.load(data_file)
        for utterance in data["results"]:
            if "alternatives" not in utterance: raise UnknownValueError()
            for hypothesis in utterance["alternatives"]:
                if "transcript" in hypothesis:
                    transcript = hypothesis["transcript"]
                    words = transcript.strip().split()
                    for w in words:
                        all_words.append(w)
    bag = []
    for w in all_words:
        count = all_words.count(w)
        if count > 9 and w not in bag:
            bag.append(w)
    bag = sorted(bag)
    return bag

def get_feats(file_name, bag):
    with open(os.path.join(dir,file_name)) as data_file:
        data = json.load(data_file)
    transcription = []
    for utterance in data["results"]:
        if "alternatives" not in utterance: raise UnknownValueError()
        for hypothesis in utterance["alternatives"]:
            if "transcript" in hypothesis:
                transcription.append(hypothesis["transcript"])

    openF = open(file_name.replace('_transcript.json','_ling.csv'),'w')
    header = ','.join(bag).encode('ascii','ignore')
    openF.write(header+'\n')
    feature_list = []
    for sentence in transcription:
        print sentence
        words = sentence.strip().split()
        word_count = len(words)
        feats = []
        if word_count > 0:
            for w in bag:
                count = words.count(w)
                feats.append(float(count)/word_count)
        else:
            feats = len(bag) * [0]
        features = ','.join([str(f) for f in feats]).encode('ascii','ignore')
        feature_list.append(features)
    for s in feature_list:
        openF.write(s+'\n')
    print 'Done processing non-english transcript. Linguistic features saved to file!'

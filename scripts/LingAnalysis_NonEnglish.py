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

def spanish_parse(transcript):
    os.chdir(r"/Users/morales/Github/models/syntaxnet")
    command = "echo '%s' | syntaxnet/models/parsey_universal/parse.sh /Users/morales/GitHub/models/Spanish" %transcript
    try:
        output = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE).stdout.read()
    except:
        output = False
    return output
def german_parse(transcript):
    os.chdir(r"/Users/morales/Github/models/syntaxnet")
    command = "echo '%s' | syntaxnet/models/parsey_universal/parse.sh /Users/morales/GitHub/models/German" %transcript
    try:
        output = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE).stdout.read()
    except:
        output = False
    return output
def dependency_distance(conll_df):
    """ Computes dependency distance for dependency tree. Based off of:
    Pakhomov, Serguei, et al. "Computerized assessment of syntactic complexity
    in Alzheimers disease: a case study of Iris Murdochs writing."
    Behavior research methods 43.1 (2011): 136-144."""
    ID = numpy.array([int(x) for x in conll_df['ID']])
    HEAD = numpy.array([int(x) for x in conll_df['HEAD']])
    diff = abs(ID-HEAD)
    total_distance = sum(diff)
    return total_distance
def load_tags():
    #Load universal POS tag set - http://universaldependencies.org/u/pos/all.html
    with open('/Users/morales/GitHub/OpenMM/data/UniversalPOSTagList.txt','r') as f:
        tags = [line.strip() for line in f.readlines()]
    return tags
def tag_count(df):
    tag_count = []
    tags = load_tags()
    for tag in sorted(tags):
        df_tags = df['UPOS'].values.tolist()
        count = df_tags.count(tag)
        tag_count.append(count)
    return tag_count
def get_feats(file_name, bag, lang):
    with open(os.path.join(dir,file_name)) as data_file:
        data = json.load(data_file)
    transcription = []
    for utterance in data["results"]:
        if "alternatives" not in utterance: raise UnknownValueError()
        for hypothesis in utterance["alternatives"]:
            if "transcript" in hypothesis:
                transcription.append(hypothesis["transcript"])

    openF = open(file_name.replace('_transcript.json','_ling.csv'),'w')
    bag_header = ','.join(bag).encode('ascii','ignore')
    syntax_header = 'word_count,avg_wordlen,levels,distance,univ_tag,%s' %(','.join(load_tags()))
    openF.write(bag_header+','+syntax_header+'\n')
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
            if lang =='German':
                conll = german_parse(sentence)
            elif lang == 'Spanish':
                conll = spanish_parse(sentence)
            if conll:
                conll_lines = conll.strip().split('\n')
                conll_table = [line.split('\t') for line in conll_lines]
                df = pandas.DataFrame(conll_table,columns=['ID','FORM','LEMMA','UPOS','XPOS','FEATS','HEAD','DEPREL','DEPS','MISC'])
                pos_feats = tag_count(df) #pos tag count
                univ_tag = len(set(df['UPOS'].values)) #unique number of pos tags
                distance = dependency_distance(df) #dependency distance
                heads = df['HEAD'].values
                levels = len(set(heads)) #tree depth
                avg_wordlen = sum([len(w) for w in words])/len(words) #average word length
                syntax_feats = [word_count, avg_wordlen,levels,distance,univ_tag] + pos_feats
            else:
                syntax_feats = 22 * [0]
        else:
            feats = len(bag) * [0]
        feats = feats + syntax_feats
        features = ','.join([str(f) for f in feats]).encode('ascii','ignore')
        feature_list.append(features)
    for s in feature_list:
        openF.write(s+'\n')
    print 'Done processing non-english transcript. Linguistic features saved to file!'

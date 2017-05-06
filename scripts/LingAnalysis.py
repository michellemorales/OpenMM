# Michelle Morales
# Script performs linguistic analysis for languages other than English

from __future__ import division
from collections import defaultdict
import sys, re, pandas, numpy, os, subprocess, json, os.path, string


def bag_of_words(dir):
    files = [f for f in os.listdir(dir) if f.endswith('_transcript.txt')]
    all_words = []
    for file_name in files:
        with open(os.path.join(dir, file_name), 'r') as data_file:
            transcription = data_file.readlines()
            # Remove punctuation and lower all characters
            for sentence in transcription:
                sentence = sentence.translate(None, string.punctuation)
                words = sentence.lower().strip().split()
                for w in words:
                    all_words.append(w)

    bag = []
    for w in all_words:
        count = all_words.count(w)
        if count > 1 and w not in bag:
            bag.append(w)
    bag = sorted(bag)
    return bag


def english_parse(transcript, parser_dir):
    os.chdir(r"%s" % parser_dir)
    command = "echo '%s' | syntaxnet/demo.sh" % transcript
    try:
        output = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE).stdout.read()
    except:
        output = False
    return output


def spanish_parse(transcript, parser_dir):
    os.chdir(r"%s" % parser_dir)
    command = "echo '%s' | syntaxnet/models/parsey_universal/parse.sh /Users/morales/GitHub/models/Spanish" % transcript
    try:
        output = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE).stdout.read()
    except:
        output = False
    return output


def german_parse(transcript, parser_dir):
    os.chdir(r"%s" % parser_dir)
    command = "echo '%s' | syntaxnet/models/parsey_universal/parse.sh /Users/morales/GitHub/models/German" % transcript
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
    diff = abs(ID - HEAD)
    total_distance = sum(diff)
    return total_distance


def load_tags():
    # Load universal POS tag set - http://universaldependencies.org/u/pos/all.html
    tags = "ADJ ADP ADV AUX CCONJ DET INTJ NOUN NUM PART PRON PROPN PUNCT SCONJ SYM VERB X".strip().split()
    print tags
    return tags


def tag_count(df):
    tag_count = []
    tags = load_tags()
    for tag in sorted(tags):
        df_tags = df['UPOS'].values.tolist()
        count = df_tags.count(tag)
        tag_count.append(count)
    return tag_count


def get_feats(file_name, bag, lang, parser_dir):
    with open(os.path.join(dir, file_name), 'r') as data_file:
        transcription = data_file.readlines()

    openF = open(file_name.replace('_transcript.txt', '_ling.csv'), 'w')
    bag_header = ','.join(bag).encode('ascii', 'ignore')
    print bag_header
    # ToDo : figure out what is wrong with the feature header, why isnt bag of words working?
    syntax_header = 'word_count,avg_wordlen,levels,distance,univ_tag,%s' % (','.join(load_tags()))
    header = bag_header + ',' + syntax_header + '\n'
    print header
    openF.write(header)
    feature_list = []
    for sentence in transcription:
        print sentence
        words = sentence.strip().split()
        word_count = len(words)
        feats = []
        if word_count > 0:
            for w in bag:
                count = words.count(w)
                feats.append(float(count) / word_count)
            if lang == 'german':
                conll = german_parse(sentence, parser_dir)
            elif lang == 'spanish':
                conll = spanish_parse(sentence, parser_dir)
            elif lang == 'english':
                conll = english_parse(sentence, parser_dir)
            if conll:
                conll_lines = conll.strip().split('\n')
                conll_table = [line.split('\t') for line in conll_lines]
                df = pandas.DataFrame(conll_table,
                                      columns=['ID', 'FORM', 'LEMMA', 'UPOS', 'XPOS', 'FEATS', 'HEAD', 'DEPREL', 'DEPS',
                                               'MISC'])
                pos_feats = tag_count(df)  # pos tag count
                univ_tag = len(set(df['UPOS'].values))  # unique number of pos tags
                distance = dependency_distance(df)  # dependency distance
                heads = df['HEAD'].values
                levels = len(set(heads))  # tree depth
                avg_wordlen = sum([len(w) for w in words]) / len(words)  # average word length
                syntax_feats = [word_count, avg_wordlen, levels, distance, univ_tag] + pos_feats
            else:
                syntax_feats = 22 * [0]
        else:
            feats = len(bag) * [0]
        feats = feats + syntax_feats
        features = ','.join([str(f) for f in feats]).encode('ascii', 'ignore')
        feature_list.append(features)
    for s in feature_list:
        openF.write(s + '\n')
    print 'Done processing non-english transcript. Linguistic features saved to file!'

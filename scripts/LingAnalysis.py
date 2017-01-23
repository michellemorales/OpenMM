#Michelle Morales
#Script performs linguistic analysis

Skip to content
This repository
Search
Pull requests
Issues
Gist
 @michellemorales
 Unwatch 2
  Unstar 2
 Fork 0 schererstefan/michelle Private
 Code  Issues 0  Pull requests 0  Projects 0  Wiki  Pulse  Graphs
Branch: master Find file Copy pathmichelle/scripts/feat_extract.py
51245a4  on Oct 3, 2016
 Michelle Morales made changes
0 contributors
RawBlameHistory     
436 lines (412 sloc)  18.2 KB
# Michelle Renee Morales
# This script can be used to extract a set of syntactic features.

# Arguments = text file containing dependency tree from Google's Parsey McParseface
# Features= [# of dependents, root,  ]

# Each parse try from Parsey comes in a CONLL format, details can be found: http://universaldependencies.org/docs/format.html
# The basic structure of each row the conll table is as follows

# ID: Word index, integer starting at 1 for each new sentence; may be a range for tokens with multiple words.
# FORM: Word form or punctuation symbol.
# LEMMA: Lemma or stem of word form.
# UPOSTAG: Universal part-of-speech tag drawn from our revised version of the Google universal POS tags.
# XPOSTAG: Language-specific part-of-speech tag; underscore if not available.
# FEATS: List of morphological features from the universal feature inventory or from a defined language-specific extension; underscore if not available.
# HEAD: Head of the current token, which is either a value of ID or zero (0).
# DEPREL: Universal Stanford dependency relation to the HEAD (root iff HEAD = 0) or a defined language-specific subtype of one.
# DEPS: List of secondary dependencies (head-deprel pairs).
# MISC: Any other annotation.
# Note: Parsey doesn't give output for every item, some columns may always be blank

# from nltk.corpus import sentiwordnet as swn
from __future__ import division
from collections import defaultdict
from gensim.models import word2vec
import sys, re, pandas, numpy

# ARGUMENTS: [sentences] [new features file] [path to labels]
file = sys.argv[1] #conll sentences
# outF = sys.argv[2] #new file to write features to
# path = sys.argv[3] #csv file with labels TODO: remove this? instead just print out participant ID

def import_labels(label,path):
    """Imports labels- must designate below which label you want"""
    labels = {}
    IDs = []
    if label == 'depression_value':
        i = 4
    elif label == 'depression':
        i = 3
    elif label == 'PTSD_value':
        i = 2
    elif label == 'PTSD':
        i = 1
    # # load the CSV file as a numpy matrix
    dataset = numpy.loadtxt(path, delimiter=",")
    for row in dataset:
        ID, PTSD, PTSD_value, depression, depression_value = row
        labels[ID] = row[i]
        IDs.append(ID)
    return labels, IDs #TODO: remove this?

### SYNTAX FEATURES ###
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
def embedding_distance(conll_df,word2vec_model):
    """ Computes cosine similarity between word2vec embeddings for each dependency relation.
    Returns summed total of all distances."""
    # Load pre-trained word2vec model
    cos_sim = []
    for i, word in enumerate(conll_df['FORM']):
        head = conll_df.at[i,'HEAD']
        head_index = conll_df.loc[conll_df['ID']==head].index.tolist()
        if head_index != []:
            head_word = conll_df.at[head_index[0],'FORM']
            try:
                d = abs(model.similarity(word,head_word))
                cos_sim.append(d)
            except:
                d = 0
    total_sim = sum(cos_sim)
    return total_sim
def upsampling(tree_list,path):
    """ Function used to upsample data of depressed participants."""
    upsampled = defaultdict(list)
    labels, label_list = import_labels('depression',path)
    negative = [L.strip() for L in open('data/negative-words.txt','r').readlines()]
    for T in tree_list:
        lines = T.split('\n')
        ID = lines[0].split()[-1]
        label = labels[int(ID)]
        conll_table = [line.split('\t') for line in lines[1:-2]]
        df = pandas.DataFrame(conll_table,columns=['ID','FORM','LEMMA','UPOS','XPOS','FEATS','HEAD','DEPREL','DEPS','MISC'])
        words = df['FORM'].values
        neg = ''
        if len(words) > 2 and len(words) < 30:
            if label == 1: #upsample depressed participants
                for x in xrange(12):
                    upsampled[ID].append(T)
            else:
                upsampled[ID].append(T)
    return upsampled
def load_tags():
    with open('PennTreebankTagList.txt','r') as f:
        tags = [line.strip().split()[1] for line in f.readlines()]
    return tags

### SEMANTIC FEATURES ###
def get_word2vecs(model, words):
    features = []
    for w in words:
        try:
            vec = model[w]
            l = [str(x) for x in vec.tolist()]
            s = ' '.join(l)
        except:
            l = [str(x) for x in ([0]*100)]
            s = ' '.join(l)
        features.append(s)
    features = ','.join(features)
    return features
def average_word2vecs(model,words):
    features = []
    if len(words) != 0:
        for w in words:
            try:
                vec = numpy.array(model[w])
            except:
                vec = [x for x in ([0]*100)] #word doesn't exist in model
            features.append(numpy.array(vec))
        avg_vector = numpy.average(numpy.array(features),axis=0).tolist()
    else:
        avg_vector = [x for x in ([0]*100)]
    return avg_vector
def sum_word2vecs(model,words):
    features = []
    if len(words) != 0:
        for w in words:
            try:
                vec = numpy.array(model[w])
            except:
                vec = [x for x in ([0]*100)] #word doesn't exist in model
            features.append(numpy.array(vec))
        sum_vector = numpy.sum(numpy.array(features),axis=0).tolist()
    else:
        sum_vector = [x for x in ([0]*100)]
    return sum_vector
def stats(tree_list,labels,IDs):
    """Calculates stats on the data."""
    sent_length = []
    word_length = []
    none = 0
    minimal = 0
    mild = 0
    moderate = 0
    severe = 0
    print 'Number of participants:', len(set(labels.keys()))
    for i, T in enumerate(tree_list):
        lines = T.split('\n')
        ID = IDs[i]
        if ID !=  362.0:
            score = labels[ID]
            # print score
            if score < 5:
                none += 1
            elif score > 4 and score < 10:
                minimal += 1
            elif score > 9 and score < 15:
                mild += 1
            elif score > 14 and score < 20:
                moderate += 1
            elif score > 19:
                severe += 1
            conll_table = [line.split('\t') for line in lines[1:-2]] #convert conll table to pandas data frame for easier processing
            df = pandas.DataFrame(conll_table,columns=['ID','FORM','LEMMA','UPOS','XPOS','FEATS','HEAD','DEPREL','DEPS','MISC'])
            words = df['FORM'].values
            sent_len = len(words)
            if sent_len > 0:
                avg_w = numpy.mean(numpy.array([len(w) for w in words]))
            else:
                avg_w = 0
            sent_length.append(sent_len)
            word_length.append(avg_w)
    print 'Average sentence length: ', numpy.mean(numpy.array(sent_length))
    print 'Average word length: ', numpy.mean(numpy.array(word_length))
    print 'Total Depressed sentences, i.e. score > 10 = %s, Total non-depressed = %s \n Breakdown by level: None = %s, Minimal=%s, Mild=%s, Moderate=%s, Severe=%s' %(mild+moderate+severe,none+minimal, none, minimal, mild, moderate, severe)
    none = 0
    minimal = 0
    mild = 0
    moderate = 0
    severe = 0
    for I in set(IDs):
        score = labels[I]
        if score < 5:
            none += 1
        elif score > 4 and score < 10:
            minimal += 1
        elif score > 9 and score < 15:
            mild += 1
        elif score > 14 and score < 20:
            moderate += 1
        elif score > 19:
            severe += 1
    print 'Total Depressed participants, i.e. score > 10 = %s, Total non-depressed = %s \n Breakdown by level: None = %s, Minimal=%s, Mild=%s, Moderate=%s, Severe=%s' %(mild+moderate+severe,none+minimal, none, minimal, mild, moderate, severe)
    ptsd = 0
    none = 0
    print 'Total Participants:', len(labels.keys())
    for participant in labels.keys():
        score = labels[participant]
        if score == 0.0:
            none += 1
        elif score ==1.0:
            ptsd += 1
    print 'PTSD=%s, None=%s' %(ptsd,none)
    ptsd_sents = 0
    non_sents = 0
    for i, T in enumerate(trees):
        lines = T.split('\n')
        ID = IDs[i]
        label = labels[ID]
        if label == 0.0:
            non_sents+=1
        elif label == 1.0:
            ptsd_sents +=1
    print 'PTSD sents=%s, Non sents=%s'%(ptsd_sents,non_sents)
def liwc(words):
    """ Get features using LIWC 2015. categories in total."""
    categories = []
    liwcD = {}
    liwc_file = '/home/michelle/ICT/data/liwc/LIWC2015_English.dic'
    read = open(liwc_file,'r').readlines()
    header = read[1:77]
    for line in header:
        category_name = line.strip().split()[1]
        categories.append(category_name)

    liwc_words = read[88:]
    for line in liwc_words:
        items = line.strip().split('\t')
        word = items[0].replace('(','').replace(')','')
        cats = items[1:]
        liwcD[word] = cats

    total_words = len(words)
    line = ' '.join(words)
    feats = defaultdict(int)
    for word in sorted(liwcD.keys()): #first 9 words are emojis with special characters TODO: treat them separately
        cats = liwcD[word]
        if '*' in word:
            pattern = re.compile(' %s'%word.replace('*',''))
        else:
            pattern = re.compile(' %s '%word)
        matches = [(m.start(0), m.end(0)) for m in re.finditer(pattern, line)]
        if matches != []:
            for C in cats:
                feats[int(C)]+=len(matches)
        else:
            for C in cats:
                feats[int(C)] += 0
    if total_words != 0:
        liwc_features = [(float(feats[key])/total_words) for key in sorted(feats)]
    else:
        liwc_features = ','.join([0]*73)
    return liwc_features
def get_context(trees):
    d = defaultdict(list)
    new_trees = []
    for i, T in enumerate(trees):
        lines = T.split('\n')
        if len(lines) > 2:
            ID = lines[0].strip().split()[-1]
            d[ID].append(T)
    for ID in sorted(d.keys()):
        mid = int(len(d[ID])/2)
        for T in d[ID][mid:]:
            new_trees.append(T)
    return new_trees

with open(file,'r') as f: #opens CONLL data file of parse trees
    data = f.read()


pattern = re.compile(r'^\<TREE\>.*?\<\/TREE\>',re.DOTALL|re.MULTILINE) # Use the <TREE> Tags to find each distinct parse
trees = pattern.findall(data)
context = 'context_'
syntaxF = open(('%s.%ssyntax'%(file,context)).replace('conll','features'),'w')
semanticsF = open(('%s.%ssemantics'%(file,context)).replace('conll','features'),'w')
liwcF = open(('%s.%sliwc'%(file,context)).replace('conll','features'),'w')
combinedF = open(('%s.%sall'%(file,context)).replace('conll','features'),'w')
combinedF_liwc = open(('%s.%sall+liwc'%(file,context)).replace('conll','features'),'w')
# vec = []
# for i in range(100):
#     vec.append('word%s'%i)
# part1 = 'root_deps,levels,u_tag,x_tag,avg_wordlen,numb_words,dep_dist'
# part2 = ','.join(vec)
# part3 = ",".join([x.strip().replace('\t','').replace(' ','_') for x in header])
# print 'ID,Sentence,%s,%s,coherence,%s'%(part1,part2,part3)

# new_file = open(outF,'w')
# tags = load_tags()
# tag_header = sorted(tags) + ['average_wordLen','numb_words']+['ID']
# # ['word_%s'%i for i in range(100)]
# feature_header = ','.join(['avg_word_%s'%i for i in range(100)] + ['dep_count', 'root_dep_count', 'depth_levels', 'unique_utags', 'unique_xtags', 'cc_count', 'total_dist', 'total_sim'] + tag_header)
# new_file.write(feature_header+'\n')

model = word2vec.Word2Vec.load('/home/michelle/ICT/fisher-vectors-100dim-check20iter') # TODO: change word2vec model to Fisher# Load word2vec model only once
# tags = load_tags() #load pos tag list
# print 'Done loading word2vec model..'
remove_NaNs = [319,342,668,669,931]
trees = get_context(trees)
if type(trees) == list: #i.e. - no upsampling has occurred
    for i, T in enumerate(trees):
        lines = T.split('\n')
        ID = lines[0].strip().split()[-1] #first line contains meta info, including data index and participant ID
        if int(ID) not in remove_NaNs and len(T.split('\n')) > 2:
            conll_table = [line.split('\t') for line in lines[1:-2]] # convert conll table to pandas data frame for easier processing
            df = pandas.DataFrame(conll_table,columns=['ID','FORM','LEMMA','UPOS','XPOS','FEATS','HEAD','DEPREL','DEPS','MISC'])
            words = df['FORM'].values #get words
            roles = df['DEPREL'].values
            if len(words) != 0 and len(words) > 3 and len(words) < 30: # ONLY IF NSubj is included!
                # vectors = get_word2vecs(model,words) #use if we want sequences
                avg_vector = average_word2vecs(model,words)
                root_index = df.loc[df['DEPREL']=='ROOT'].index.tolist() # Find root word
                if root_index != []:
                        r = df.at[root_index[0],'FORM']
                        root_id = df.at[root_index[0],'ID']
                        root_children = df.loc[df['HEAD']==root_id]
                        root_deps = len(root_children) #root's direct children
                        try:
                            vec = numpy.array(model[r])
                        except:
                            vec = numpy.array([0]*100)
                else:
                    roots_id = 0
                    root_children = 0


                #Calculates syntactic dependency distance using conll tree
                dep_dist = dependency_distance(df)

                #Calculates semantic coherence using cosine similarity measures between head/dependent relations
                coherence = embedding_distance(df, model)

                #Get number of parents/children/depth of tree
                heads = df['HEAD'].values
                levels = len(set(heads)) #TODO:figure out what to name this, could also be number of relations
                # Get the number of unique POS tags (coarse and fine)
                u_tags = df['UPOS'].values
                x_tags = df['XPOS'].values
                u_tag = len(set(u_tags))
                x_tag = len(set(x_tags))

                #Get frequency of each POS tag
                tag_freq = []
                tags = load_tags()
                for tag in sorted(tags):
                    x_tags = df['XPOS'].values.tolist()
                    count = x_tags.count(tag)
                    tag_freq.append(count)

                #Calculate average word length and total number of words
                avg_wordlen = sum([len(w) for w in words])/len(words)
                numb_words = len(words)

                #Sentence
                sent = ' '.join(words)
                #LIWC features - p.s. liwc funciton already normalizes features
                liwc_features = ','.join([str(x) for x in liwc(words)])
                liwcF.write('%s,%s,%s\n'%(ID,sent,liwc_features))
                #Syntax features - TODO:NORMALIZE - done!
                syntax = [feat/len(words) for feat in [root_deps,levels,u_tag,x_tag,avg_wordlen,numb_words,dep_dist]]#Remove tag freq
                syntax_features = ','.join([str(feat) for feat in syntax])
                syntaxF.write('%s,%s,%s\n'%(ID,sent,syntax_features))
                #Semantic features
                semantics = coherence/len(words)
                avg_sent = ','.join([str(x) for x in avg_vector])
                semantics_features = '%s,%s'%(avg_sent,coherence)
                semanticsF.write('%s,%s,%s\n'%(ID,sent,semantics_features))
                #Combined features
                all_feats = '%s,%s,%s,%s\n'%(ID,sent,syntax_features,semantics_features)
                combinedF.write(all_feats)
                #Combined features+LIWC
                all_feats_liwc = '%s,%s,%s,%s,%s\n'%(ID,sent,syntax_features,semantics_features,liwc_features)
                combinedF_liwc.write(all_feats_liwc)
                print all_feats_liwc

#
# # print 'Done creating %s feature file.' %(outF)
#
# #     for ID in trees.keys():
# #         for T in trees[ID]:
# #             lines = T.split('\n')
# #         #first line contains meta info, including data index and participant ID
# #         # line_numb, ID = lines[0].split()[1:]
# #         # get labels
# #         # convert conll table to pandas data frame for easier processing
# #             conll_table = [line.split('\t') for line in lines[1:-2]]
# #
# #             df = pandas.DataFrame(conll_table,columns=['ID','FORM','LEMMA','UPOS','XPOS','FEATS','HEAD','DEPREL','DEPS','MISC'])
# #             # print df, '\n'
# #             # Find root word
# #             words = df['FORM'].values
# #             vectors = get_word2vecs(model,words)
# #             root_index = df.loc[df['DEPREL']=='ROOT'].index.tolist()
# #             if root_index != []:
# #                     r = df.at[root_index[0],'FORM']
# #                     root_id = df.at[root_index[0],'ID']
# #                     root_children = df.loc[df['HEAD']==root_id]
# #                     root_deps = len(root_children)
# #                     try:
# #                         vec = model[r]
# #                     except:
# #                         vec = numpy.array([0]*100)
# #             else:
# #                 roots_id = 0
# #                 root_children = 0
# #
# #             # Get number of dependencies
# #             dep_count = df.shape[0]
# #             dist = dependency_distance(df)
# #             cos = embedding_distance(df, model)
# #
# #             # Get number of parents/children/depth of tree
# #             heads = df['HEAD'].values
# #             levels = len(set(heads))
# #
# #             # Get the number of unique POS tags (coarse and fine)
# #             u_tags = df['UPOS'].values
# #             u_tag = len(set(u_tags))
# #             x_tag = len(set(df['XPOS'].values))
# #             cc =  u_tags.tolist().count('CONJ')
# #             # features = vec.tolist() + [dep_count, root_deps, levels, u_tag, x_tag, cc, dist, cos, ID]
# #             features = [dep_count, root_deps, levels, u_tag, x_tag, cc, dist, cos, ID]
# #             s = ','.join([str(f) for f in features])
# #             s = vectors + ',' + s
# #             new_file.write(s+'\n')
# #             print s





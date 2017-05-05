#Michelle Morales
#Script performs linguistic analysis

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

from __future__ import division
from collections import defaultdict
from gensim.models import word2vec
import sys, re, pandas, numpy, os, subprocess, json

### SYNTAX FEATURES ###
def parse(transcript):
    os.chdir(r"/Users/morales/Github/models/syntaxnet")
    command = "echo '%s' | syntaxnet/demo.sh" %transcript
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
    with open('/Users/morales/GitHub/OpenMM/data/PennTreebankTagList.txt','r') as f:
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
def get_liwc(transcript):
        """ Get features using LIWC 2015. categories in total."""
        categories = []
        liwcD = {}
        catsD = {}
        liwc_file = '/Users/morales/GitHub/OpenMM/data/LIWC2015_English.dic'
        read = open(liwc_file,'r').readlines()
        header = read[1:74]
        for line in header:
            items = line.strip().split()
            category_name = items[1]
            category_numb = items[0].strip()
            categories.append(category_name)

            catsD[int(category_numb)] = category_name
        liwc_words = read[88:] #ignore emojis
        for line in liwc_words:
            items = line.strip().split('\t')
            word = items[0].replace('(','').replace(')','')
            cats = items[1:]
            liwcD[word] = cats

        total_words = len(transcript.split())
        feats = defaultdict(int)
        for word in sorted(liwcD.keys()):
            cats = liwcD[word]
            if '*' in word:
                pattern = re.compile(' %s'%word.replace('*',''))
            else:
                pattern = re.compile(' %s '%word)
            matches = [(m.start(0), m.end(0)) for m in re.finditer(pattern, transcript)]
            if matches != []:
                for C in cats:
                    feats[int(C)]+=len(matches)
            else:
                for C in cats:
                    feats[int(C)] += 0
        if total_words != 0:
            liwc_features = [(float(feats[key])) for key in sorted(feats.keys())]
        else:
            liwc_features = ','.join(str(i) for i in [0]*len(categories))
        header = ','.join([catsD[cat] for cat in sorted(feats.keys())])
        return header, liwc_features

### RUN FEATURE EXTRACTION FUNCTIONS ###
def run(file_name):
    with open(file_name) as data_file:
        data = json.load(data_file)
    transcription = []
    for utterance in data["results"]:
        if "alternatives" not in utterance: raise UnknownValueError()
        for hypothesis in utterance["alternatives"]:
            if "transcript" in hypothesis:
                transcription.append(hypothesis["transcript"])

    model = word2vec.Word2Vec.load('/Users/morales/GitHub/OpenMM/data/fisher-vectors-100dim-check20iter')
    liwc_cats, liwc_feats = get_liwc(' ')
    tags = load_tags()
    openF = open(file_name.replace('_transcript.json','_ling.csv'),'w')
    header = '%s,word_count, avg_wordlen,levels,dep_dist,coherence, univ_tag, fine_tag,%s\n'%(liwc_cats,','.join(tags))
    openF.write(header)
    feature_list = []
    for sentence in transcription:
        print sentence
        words = sentence.strip().split()
        word_count = len(words)
        #Get semantic (LIWC) features
        liwc_cats, liwc_feats = get_liwc(sentence) #fix liwc script
        #Get syntactic features
        if word_count > 0:
            conll = parse(sentence)
            if conll:

                conll_lines = conll.strip().split('\n')
                conll_table = [line.split('\t') for line in conll_lines]
                df = pandas.DataFrame(conll_table,columns=['ID','FORM','LEMMA','UPOS','XPOS','FEATS','HEAD','DEPREL','DEPS','MISC'])

                #Get frequency of each POS tag
                tag_freq = []
                for tag in sorted(tags):
                    x_tags = df['XPOS'].values.tolist()
                    count = x_tags.count(tag)
                    tag_freq.append(count)

                #Calculates syntactic dependency distance using conll tree
                dep_dist = dependency_distance(df)

                #Calculates semantic coherence using cosine similarity measures between head/dependent relations
                coherence = embedding_distance(df, model)

                # Get the number of unique POS tags (coarse and fine)
                u_tags = df['UPOS'].values
                x_tags = df['XPOS'].values
                univ_tag = len(set(u_tags))
                fine_tag = len(set(x_tags))
                #Get number of parents/children/depth of tree
                heads = df['HEAD'].values
                levels = len(set(heads))
                avg_wordlen = sum([len(w) for w in words])/len(words)
                syntax_feats = [word_count, avg_wordlen,levels,dep_dist,coherence, univ_tag, fine_tag] + tag_freq
            else:
                 syntax_feats = 43 * [0]
        else:
            syntax_feats = 43 * [0]
        features = ','.join([str(f) for f in liwc_feats + syntax_feats])
        feature_list.append(features)
    for s in feature_list:
        openF.write(s+'\n')
    print 'Done processing transcript. Linguistic features saved to file!'

from flair.data import Sentence
from segtok.segmenter import split_single
from flair.models import SequenceTagger

import stanfordnlp

# TODO: generate the following syntax features - depth of tree, number of root dependents, number of unique universal POS tags, frequency of each POS tag, average word length, and a computed dependency distance measure.


# def pos_tagging(text):
#     """Tags text with part-of-speech tags using Flair model"""
#     pos_tagger = SequenceTagger.load('pos')
#     sentences = [Sentence(sent, use_tokenizer=True) for sent in split_single(text)]
#     pos_tagger.predict(sentences)
#     for s in sentences:
#         print(s.to_dict(tag_type='pos'))


# https://github.com/sebastianruder/NLP-progress/blob/master/english/dependency_parsing.md
# Info on universal dependencies - https://universaldependencies.org/
def stanford_tagger(text):
    nlp = stanfordnlp.Pipeline()
    doc = nlp(text)
    print(doc)
    print(doc.sentences[0].print_dependencies())
    doc.write_conll_to_file('syntax.csv')

stanford_tagger("Barack Obama was born in Hawaii.  He was elected president in 2008.")

def syntax_features():
    # freq of each POS tag
    # depth of tree
    # number of root dependents
    # number of unique universal pos tags

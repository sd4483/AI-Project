# -*- coding: utf-8 -*-
"""
Created on Wed May 30 13:03:11 2018

@author: sudhe
"""

import nltk
nltk.download('punkt')
from nltk.tokenize import word_tokenize

sentence = "I was extremely happy that my exams are over. I can now do crazy things like distinguishing \
between drive drives driving driver drivers driven and repeating myself with happy happy happy exams exams"

tokens = word_tokenize(sentence)

#stopwords
from nltk.corpus import stopwords
sw = stopwords.words('english')
sw = sw + ['john' + 'mary' + '$$%^']

Tokens = []
for token in tokens:
    if token not in sw:
        Tokens.append(token)

#stemming
from nltk.stem.porter import PorterStemmer
stemmer = PorterStemmer()

for token in tokens:
    tok = stemmer.stem(token)
    
#lemmatization
from nltk.stem import WordNetLemmatizer
nltk.download('wordnet')
lemmatizer = WordNetLemmatizer()

for token in tokens:
    tok = lemmatizer.lemmatize(token)
    
#parts of speech
from nltk import pos_tag
nltk.download('maxent_treebank_pos_tagger')
nltk.download('averaged_perceptron_tagger')
    
#converting to nltk text
from nltk.text import Text
t = Text(tokens)
t.count('I')
t.vocab()
t.plot()
import spacy 
import os 
import json 
import re

import unicodedata
from bs4 import BeautifulSoup
from textblob import TextBlob
from textblob import Word
from textblob.sentiments import NaiveBayesAnalyzer

from spacy.lang.en.stop_words import STOP_WORDS as stopwords

fpath=os.path.join(os.path.dirname(__file__),'data/contractions.json')
contractions=json.load(open(fpath))
nlp = spacy.load('en_core_web_sm')
#count the total number of words
def word_count(text):
    return len(text.split())

def char_count(x):
    pattern=r'\s'
    return len(re.sub(pattern,'',x))

def avg_word_len(x):
    return char_count(x)/word_count(x)

def stopword_count(x):
    temp=len([word for word in x.lower().split() if words in stopwords])
    return temp

def hashtags_count(x):
    return len(re.findall(r'#\w+',x))

def mentions_count(x):
    return len(re.findall(r'@\w+',x))

def numerics_count(x):
    return len(re.findall(r'\b\d+\b',x))

def upper_case_count(x):
    return len([word for word in x.split() if word.isupper()])


##PreProcessing and Text Cleaning

def to_lower_case(x):
    return x.lower()

def contraction_to_expansion(x):
    return " ".join([contractions.get(word.lower(),word) for word in x.split()])

def remove_emails(x):
    pattern =r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b'
    return re.sub(pattern,'',x)

def count_emails(x):
    pattern=r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b'
    return len(re.findall(pattern,x));

def remove_urls(x):
    pattern =r'http\S+|www\.\S+'
    return re.sub(pattern,'',x)

def count_urls(x):
    pattern =r'http\S+|www\.\S+'
    return re.findall(pattern,x)


def count_rt(x):
    pattern = r'\bRT @\w+'
    return len(re.findall(pattern, x))

def remove_rt(x):
    pattern = r'\bRT @\w+'
    return re.sub(pattern, '', x)

def remove_html_tags(x):
    return BeautifulSoup(x, 'lxml').get_text()

def remove_accented_chars(x):
    return unicodedata.normalize('NFKD', x).encode('ascii', 'ignore').decode('utf-8', 'ignore')

def remove_mentions(x):
    pattern = r'@\w+'
    return re.sub(pattern, '', x).strip()

def remove_special_chars(x):
    pattern = r'[^\w\s]'
    return re.sub(pattern, '', x)

def remove_repeated_chars(x):
    pattern = r'(.)\1+'
    return re.sub(pattern, r'\1\1', x)

def remove_stop_words(x):
    return ' '.join([word for word in x.split() if word not in stopwords])

def lemmatize_noun_verb(x):
    doc=nlp(x);
    tokens=[]
    for token in doc:
        if token.pos_ in ['NOUN','VERB']:
            tokens.append(token.lemma_)
        else:
            tokens.append(token.text)

    x=' '.join(token)
    pattern=r'\s\.'
    x=re.sub(pattern,'.',x)
    return x

def lemmatize(x):
    doc=nlp(x)
    return ' '.join([token.lemma_ for token in doc])

def remove_common_words(x,common_words):
    return ' '.join([word for word in x.split() if word not in common_words])

def remove_rare_words(x,rare_words):
    return ' '.join([word for word in x.split() if word not in rare_words])

def correct_spelling(x):
    words=[]
    for word in x.split():
        w=Word(word)
        words.append(w.correct())
    return ' '.join(words)

def get_noun_phrase(x):
    blob=TextBlob(x)
    noun_phrase=blob.noun_phrases

    return noun_phrase

def n_gram(x,n=2):
    return list(TextBlob(x),ngrams(n))


def singularize_words(x):
    blob = TextBlob(x)
    return ' '.join([word.singularize() if tag in ['NNS'] else word for word, tag in blob.tags])

def pluralize_words(x):
    blob = TextBlob(x)
    return ' '.join([word.pluralize() if tag in ['NN'] else word for word, tag in blob.tags])

def sentiment_analysis(x):
    return TextBlob(x, analyzer=NaiveBayesAnalyzer()).sentiment.classification


def detect_language(x):
    translator = Translator()
    return translator.detect(x).lang



        
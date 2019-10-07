"""
@author: DIP
@Copyright: Dipanjan Sarkar
"""

# # Import necessary dependencies
import spacy
import nltk
from nltk.tokenize.toktok import ToktokTokenizer
import re

from contractions import CONTRACTION_MAP
import unicodedata
#disable = ['ner', 'parser']
nlp = spacy.load('en_core_web_sm', parse = False, tag=False, entity=False)
nlp.max_length = 1500000 #or whatever value > 1000000, as long as you don't run out of RA
#nlp = spacy.load('en_core_web_sm')### for manisha's install of spacy, this works
tokenizer = ToktokTokenizer()
#stopword_list = nltk.corpus.stopwords.words('english')
stopword_list = list(spacy.lang.en.stop_words.STOP_WORDS)
stopword_list.extend(['lesson', 'illustration', 's', 'chapter', 'edition', 'print', 'sentence', 'illustrate', 'mrs', 'author', 'copy', 'XV','XI','XXI','II','XII','XXII','III','XIII','XXIII','IV','XIV','XXIV','V','XXV','VI','XVI','XXVI','VII','XVII','VIII','XVIII','IX','XIX','X','XX'])
#stopword_list.append()

# Removing accented characters
def remove_accented_chars(text):
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8', 'ignore')
    return text


# # Expanding Contractions
def expand_contractions(text, contraction_mapping=CONTRACTION_MAP):
    
    contractions_pattern = re.compile('({})'.format('|'.join(contraction_mapping.keys())), 
                                      flags=re.IGNORECASE|re.DOTALL)
    def expand_match(contraction):
        match = contraction.group(0)
        first_char = match[0]
        expanded_contraction = contraction_mapping.get(match) \
                                   if contraction_mapping.get(match) \
                                    else contraction_mapping.get(match.lower())                       
        expanded_contraction = first_char+expanded_contraction[1:]
        return expanded_contraction
        
    expanded_text = contractions_pattern.sub(expand_match, text)
    expanded_text = re.sub("'", "", expanded_text)
    return expanded_text


# # Removing Special Characters
def remove_special_characters(text):
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    return text


# # Lemmatizing text
def lemmatize_text(text):
    text = nlp(text, disable = ['ner', 'parser'])
    text = ' '.join([word.lemma_ if word.lemma_ != '-PRON-' else word.text for word in text])
    return text


# # Removing Stopwords
def remove_stopwords(text, is_lower_case=False):
    tokens = tokenizer.tokenize(text)
    tokens = [token.strip() for token in tokens]
    if is_lower_case:
        filtered_tokens = [token for token in tokens if token not in stopword_list]
    else:
        filtered_tokens = [token for token in tokens if token.lower() not in stopword_list]
    filtered_text = ' '.join(filtered_tokens)    
    return filtered_text


# # Normalize text corpus - tying it all together
def normalize_corpus(doc, contraction_expansion=True,
                     accented_char_removal=True, text_lower_case=True, 
                     text_lemmatization=True, special_char_removal=True, 
                     stopword_removal=True):
    
#    normalized_corpus = []

    if accented_char_removal:
        doc = remove_accented_chars(doc)
        
    if contraction_expansion:
        doc = expand_contractions(doc)
        
    if text_lower_case:
        doc = doc.lower()
        
    # remove extra newlines
    doc = re.sub(r'[\r|\n|\r\n]+', ' ',doc)
    # insert spaces between special characters to isolate them    
    special_char_pattern = re.compile(r'([{.(-)!}])')
    doc = special_char_pattern.sub(" \\1 ", doc)
    
    if text_lemmatization:
        doc = lemmatize_text(doc)
        
    if special_char_removal:
        doc = remove_special_characters(doc)  
        
    # remove extra whitespace
    doc = re.sub(' +', ' ', doc)
    
    if stopword_removal:
        doc = remove_stopwords(doc, is_lower_case=text_lower_case)
        
#        normalized_corpus.append(doc)
        
    return doc
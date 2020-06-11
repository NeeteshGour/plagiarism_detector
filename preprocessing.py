# -*- coding: utf-8 -*-
"""
Created on Thu Mar 12 11:18:59 2020

@author: neete
"""

import re

def text_preprocessing(input_str):
    #convert text to lower
    input_str = input_str.lower()
    
    
    # remove number
    input_str= re.sub(r'\d+', '', input_str)
    
    # remove punctions
    
    #print(result)
    punctuations = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
    no_punct = ""
    for char in input_str:
       if char not in punctuations:
           no_punct = no_punct + char
    input_str=no_punct
    
    #remove whitespace
    input_str = input_str.strip()
    
    
    #stop word removal
    from nltk.corpus import stopwords
    stop_words = set(stopwords.words('english'))
    from nltk.tokenize import word_tokenize
    tokens = word_tokenize(input_str)
    input_str = [i for i in tokens if not i in stop_words]
    
    
    #lemmatization
    
    
    from nltk.stem import WordNetLemmatizer
    from nltk.tokenize import word_tokenize
    lemmatizer=WordNetLemmatizer()
    final_str=[]
    for word in input_str:
        final_str.append(lemmatizer.lemmatize(word))
    final_str = " ".join(final_str)
    return final_str


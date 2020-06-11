# -*- coding: utf-8 -*-
"""
Created on Sun Mar  8 17:25:54 2020

@author: neete
"""

from googleapiclient.discovery import build
from werkzeug.utils import secure_filename
from textdistance import Levenshtein
from flask import Flask, render_template, request
app = Flask(__name__)



def getkey(value,dict_name):
    for x, y in dict_name.items():
        if y == value:
            return x


def preprocess(text):
    #remove \n and white spaces
    text=text[12:]
    text =text.strip()
    stri='...'
    text = text.split();
    text=(' '.join([i for i in text if i not in stri]));
    return text
    

def sentence_similarity(query,sen_dic):
    sim_matrix={}
    levenshtein = Levenshtein()
    for x,y in sen_dic.items():
        dist=levenshtein.distance(query,x)
        sim_matrix[x]=((1.0- dist/(max(len(query),len(x))))*100)
    return sim_matrix

def retrievd_max_sim_links(sen_sim_dict,response_files):
    values=[]
    values=list(sen_sim_dict.values())
    if max(values)>70:
        links=response_files[getkey(max(values),sen_sim_dict)]
    else:
        links="Not plagiarised"
    return links
    
        
    
def getResult(query):
    query=query[:220]
    try:
        response_files={}
#        print("working")
        api_key = "AIzaSyBzAe5nKWbekfVG5VqRlfVKpt1-kVAoBT8"
        cse_key = "002860180232229038790:rxs61eurz1n"
        
        resource = build("customsearch", 'v1', developerKey=api_key).cse()
        result = resource.list(q=query, cx=cse_key).execute()
        for _ in result['items']:
            response_files[preprocess(_['snippet'])]=_['link']
        if len(response_files)>1:
            links=retrievd_max_sim_links(sentence_similarity(preprocess(query),response_files),response_files)
            return links
        elif len(response_files)==1:
            return list(response_files.values())[0]
        else:
            return "NOT PLAGIARIZED"
    except :
        return "NO INTERNET CONNECTION"



	

if __name__ == '__main__':
   app.run(port=3000)

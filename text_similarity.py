# -*- coding: utf-8 -*-
"""
Created on Sat Mar 21 17:44:36 2020

@author: neete
"""
from textdistance import Levenshtein
def sentence_similarity(txt1,txt2):
    sim_matrix={}
    levenshtein = Levenshtein()
    dist=levenshtein.distance(txt1,txt2)
    sim_matrix=((1.0- dist/(max(len(txt1),len(txt2))))*100)
    return sim_matrix


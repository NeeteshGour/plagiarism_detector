# -*- coding: utf-8 -*-
"""
Created on Thu Mar 19 21:25:04 2020

@author: neete
"""
import os
import pycode_similar
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
pypath=os.path.join(BASE_DIR,'temp_py_file')
#file path to python source code files
path  = 'D:\ml dataset\RosettaCodeData-master\modifiedpython'

def processpyfiles():
    files = os.listdir(path)
    for pyfile in os.listdir(pypath):
        fp1 = open(pypath+'\\'+pyfile,encoding="utf8")
        txt = fp1.read()
        fp1.close()
    simi_matrix=list()
    code=[]

    
    for file in files:
        fp = open(path+'\\'+file,encoding="utf8")
        filetext= fp.read()
        code.append(filetext)
    print(code)
    #    for ft in filetext:
    #        code.append(ft)
    
    for file in code:
        try:
            simi_matrix.append(dict(pycode_similar.detect([str(txt),str(file)],diff_method=pycode_similar.UnifiedDiff)).get(1)[0].plagiarism_percent)
        except:
            return "SYNTAX ERROR IN FILE"
       
    if max(simi_matrix)>=.90:
        return "PLAGIARIZED"
    else:
        return "NOT PLAGIARIZED"
    


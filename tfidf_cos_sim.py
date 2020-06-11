# -*- coding: utf-8 -*-
from sklearn.feature_extraction.text import TfidfVectorizer
#import os
#import seaborn as sns
#import matplotlib.pyplot as plt
#import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

def findSimByTfCos(corpus):
    vectorizer = TfidfVectorizer(ngram_range=(2,3),min_df=2)
    docs       = vectorizer.fit_transform(corpus)
    print(docs.toarray().shape)
    docs1=docs.toarray()[:1]
    docs2=docs.toarray()[1:]
    print(" doc1 ",docs1.shape)
    print(" doc2 ",docs2.shape)
    cos_sim=cosine_similarity(docs2,docs1)
    print(" cos_sim ",cos_sim.shape)
    max_sim=max(cos_sim)
    i=0
    for _ in cos_sim:
        if max_sim==_:
            break
        i+=1
    return i


# print(vectorizer.get_feature_names())
# sns.distplot(docs.toarray()[0], rug=True,hist=False,bins=5)
# print(docs.toarray()[0].shape)
# for i in docs.toarray()[0:]:
#     print(count)
#     print(i)
#     count+=1


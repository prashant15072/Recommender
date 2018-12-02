#!/usr/bin/env python
# coding: utf-8

# In[ ]:
from __future__ import division
import sys
import numpy as np
import scipy as sp
import pandas as pd
from timeit import default_timer as timer
import matplotlib.pyplot as plt
from CoffeeFlick import coffeeFlick

#get_ipython().magic(u'matplotlib inline')
from os.path import basename

import seaborn as sns
sns.set_style('white')

from polara.recommender.data import RecommenderData, RecommenderDataPositive
from polara.recommender.models import SVDModel, CoffeeModel, NonPersonalized
from polara.evaluation import evaluation_engine as ee
from polara.evaluation.plotting import show_hits, show_hit_rates, show_precision_recall, show_ranking, show_relevance, show_ranking_positivity
from polara.tools.mymedialite.mmlwrapper import MyMediaLiteWrapper
from polara.tools.movielens import get_movielens_data, filter_short_head
from polara.tools.printing import print_frames

for ind in range(5):
    # In[2]:

    ml_file = "ml-1m.zip"
    if sys.platform == 'win32':
        lib_path = 'MyMediaLite-3.11/lib/mymedialite'
    else:
        lib_path = 'MyMediaLite-3.11/bin'
    data_folder = 'MyMediaLiteData'

    def get_file_name(filepath):
        return ''.join(basename(filepath).split('.')[:-1])


    # In[3]:

    ml_data = get_movielens_data(local_file=ml_file)
    movielens = RecommenderData(ml_data, 'userid', 'movieid', 'rating')
    movielens.name = get_file_name(ml_file)

    print type(ml_data)

    # In[4]:


    movielens.holdout_size = 1
    movielens.shuffle_data = True
    movielens.test_sample = None
    movielens.random_holdout = False
    movielens.permute_tops = True


    # In[5]:

    coffee = CoffeeModel(movielens)
    # print "coffee.mlrank"
    # print coffee.mlrank

    # In[6]:

    coffee.build()

    # In[7]:

    v, w = coffee._items_factors, coffee._feedback_factors

    # In[8]:

    rating_model = movielens
    # print "rating_model.index.feedback.T"
    # print rating_model.index.feedback.T

    # In[9]:

    pos_rating_idx = rating_model.index.feedback.set_index('old').loc[coffee.switch_positive, 'new']
    # print "pos_rating_idx"
    # print pos_rating_idx


    # In[ ]:

    hit_score = {}
    almost_score = {}
    fail_score = {}
    hidden_pos = {}
    rating_diff = {}

    num_users = rating_model.test.testset.userid.nunique()
    rating_model.test.testset.userid.unique()

    for user_id in rating_model.test.testset.userid.unique():
        #print user_id
        user_data = rating_model.test.testset.query('userid==@user_id')
        rating_data = rating_model.index.feedback.set_index('old').loc[user_data.rating.values, 'new'].values
        movies_data = user_data.movieid.values

        user_pref = sp.sparse.coo_matrix((np.ones_like(movies_data), (movies_data, rating_data)), shape = (v.shape[0], w.shape[0]))
        recs = v.dot((v.T.dot(user_pref.A).dot(w)).dot(w.T))

        hidden_movie = rating_model.test.evalset.query('userid==@user_id').movieid.iloc[0]
        hidden_rating = rating_model.test.evalset.query('userid==@user_id').rating.iloc[0]
        hidden_rating_idx = rating_model.index.feedback.query('old == @hidden_rating').new.iloc[0]

        predicted_rating_idx = recs[hidden_movie, :].argmax()

        if predicted_rating_idx == hidden_rating_idx:
            hit_score[user_id] = 1
        else:
            rating_diff[user_id] = hidden_rating_idx - predicted_rating_idx

            is_almost_top = ((predicted_rating_idx >= pos_rating_idx) and (hidden_rating_idx >= pos_rating_idx) or
                             (predicted_rating_idx <  pos_rating_idx) and (hidden_rating_idx <  pos_rating_idx))
            if is_almost_top:
                almost_score[user_id] = 1
            else:
                fail_score[user_id] = 1


    # # RMSE result

    # In[11]:

    # print "FOR FOLD " + str(ind+1) + ":"
    RMSE = np.sqrt(np.sum(rating_diff.values())/num_users)
    # print "RMSE"
    # print RMSE


    # In[12]:


    bingo = sum(hit_score.values())

    positive = sum(almost_score.values())

    #Print the data
    coffeeFlick().printPrediction()

# -*- coding: utf-8 -*-                                                                                                                                          
def filtering(tweets):
         ng_words=["https","http","RT",".","-"]
         for word in ng_words:
                 tweets=list(filter(lambda x:word not in x,tweets))
         return tweets

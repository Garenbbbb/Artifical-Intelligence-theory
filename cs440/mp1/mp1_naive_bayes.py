# naive_bayes.py
# ---------------
# Licensing Information:  You are free to use or extend this projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to the University of Illinois at Urbana-Champaign
#
# Created by Justin Lizama (jlizama2@illinois.edu) on 09/28/2018
from hashlib import pbkdf2_hmac
import numpy as np
import math
from tqdm import tqdm
from collections import Counter
import reader

"""
This is the main entry point for MP1. You should only modify code
within this file -- the unrevised staff files will be used for all other
files and classes when code is run, so be careful to not modify anything else.
"""




"""
  load_data calls the provided utility to load in the dataset.
  You can modify the default values for stemming and lowercase, to improve performance when
       we haven't passed in specific values for these parameters.
"""
 
def load_data(trainingdir, testdir, stemming=False, lowercase=False, silently=False):
    print(f"Stemming is {stemming}")
    print(f"Lowercase is {lowercase}")
    train_set, train_labels, dev_set, dev_labels = reader.load_dataset_main(trainingdir,testdir,stemming,lowercase,silently)
    return train_set, train_labels, dev_set, dev_labels


def create_word_maps_uni(X, y, max_size=None):
    """
    X: train sets
    y: train labels
    max_size: you can ignore this, we are not using it

    return two dictionaries: pos_vocab, neg_vocab
    pos_vocab:
        In data where labels are 1 
        keys: words 
        values: number of times the word appears
    neg_vocab:
        In data where labels are 0
        keys: words 
        values: number of times the word appears 
    """
    #print(len(X),'X')
    pos_vocab = []
    neg_vocab = []
    ##TODO:
    index = 0
    for email in X:
        for word in email:
            if y[index] == 1: # label is 1
                 pos_vocab.append(word)
            else: # label is 0 
                neg_vocab.append(word)
        index += 1

    pos_cnt = Counter()
    neg_cnt = Counter()   
    for word in pos_vocab:
        pos_cnt[word] += 1
    for word in neg_vocab:
        neg_cnt[word] += 1 

    return dict(pos_cnt), dict(neg_cnt)


def create_word_maps_bi(X, y, max_size=None):
    """
    X: train sets
    y: train labels
    max_size: you can ignore this, we are not using it

    return two dictionaries: pos_vocab, neg_vocab
    pos_vocab:
        In data where labels are 1 
        keys: pairs of words
        values: number of times the word pair appears
    neg_vocab:
        In data where labels are 0
        keys: words 
        values: number of times the word pair appears 
    """
    #print(len(X),'X')
    pos_vocab = []
    neg_vocab = []
    index = 0
    ##TODO:

    for email in X:
        pre_word = ''
        for word in email:
            if y[index] == 1:
                pos_vocab.append(word)
                if pre_word != '':
                    pos_vocab.append(pre_word + ' ' + word)
            else:
                neg_vocab.append(word)
                if pre_word != '':
                    neg_vocab.append(pre_word + ' ' + word)
            pre_word = word
        index += 1


    pos_cnt = Counter()
    neg_cnt = Counter()   
    for word in pos_vocab:
        pos_cnt[word] += 1
    for word in neg_vocab:
        neg_cnt[word] += 1

    return dict(pos_cnt), dict(neg_cnt)



# Keep this in the provided template
def print_paramter_vals(laplace,pos_prior):
    print(f"Unigram Laplace {laplace}")
    print(f"Positive prior {pos_prior}")


"""
You can modify the default values for the Laplace smoothing parameter and the prior for the positive label.
Notice that we may pass in specific values for these parameters during our testing.
"""

def naiveBayes(train_set, train_labels, dev_set, laplace=0.001, pos_prior=0.8, silently=False):
    '''
    Compute a naive Bayes unigram model from a training set; use it to estimate labels on a dev set.

    Inputs:
    train_set = a list of emails; each email is a list of words
    train_labels = a list of labels, one label per email; each label is 1 or 0
    dev_set = a list of emails
    laplace (scalar float) = the Laplace smoothing parameter to use in estimating unigram probs
    pos_prior (scalar float) = the prior probability of the label==1 class
    silently (binary) = if True, don't print anything during computations 

    Outputs:
    dev_labels = the most probable labels (1 or 0) for every email in the dev set
    '''
    #
    total_pos_word = 0
    total_neg_word = 0
    # Keep this in the provided template
    print_paramter_vals(laplace,pos_prior)
    #calculate the appreance of words
    pos_dict, neg_dict = create_word_maps_uni(train_set, train_labels, max_size=None)
    for num in pos_dict.values():
        total_pos_word += num
    for num in neg_dict.values():
        total_neg_word += num
    pos_len = len(pos_dict)
    neg_len = len(neg_dict)


    dev_labels = []
    for dev in dev_set:
        pos_pro = math.log(pos_prior)
        neg_pro = math.log(1 - pos_prior)
        for word in dev:
            exist_pos = 0
            exist_neg = 0
            if word in pos_dict.keys():
                pos_pro += math.log((pos_dict[word] + laplace)/(total_pos_word + laplace*(1+pos_len))) 
                exist_pos = 1
            if word in neg_dict.keys():
                neg_pro += math.log((neg_dict[word] + laplace)/(total_neg_word + laplace*(1+neg_len)))
                exist_neg = 1
            if exist_pos == 0:
                pos_pro += math.log(laplace/(total_pos_word + laplace*(1+pos_len)))
            if exist_neg == 0:
                neg_pro += math.log(laplace/(total_neg_word + laplace*(1+neg_len)))
        print(pos_pro,neg_pro)
        if pos_pro > neg_pro:
            dev_labels.append(1)
        else:
            dev_labels.append(0)
    #print(total_pos_word,total_neg_word,pos_len,neg_len)
    return dev_labels


# Keep this in the provided template
def print_paramter_vals_bigram(unigram_laplace,bigram_laplace,bigram_lambda,pos_prior):
    print(f"Unigram Laplace {unigram_laplace}")
    print(f"Bigram Laplace {bigram_laplace}")
    print(f"Bigram Lambda {bigram_lambda}")
    print(f"Positive prior {pos_prior}")


def bigramBayes(train_set, train_labels, dev_set, unigram_laplace=0.001, bigram_laplace=0.005, bigram_lambda=0.5,pos_prior=0.8,silently=False):
    '''
    Compute a unigram+bigram naive Bayes model; use it to estimate labels on a dev set.

    Inputs:
    train_set = a list of emails; each email is a list of words
    train_labels = a list of labels, one label per email; each label is 1 or 0
    dev_set = a list of emails
    unigram_laplace (scalar float) = the Laplace smoothing parameter to use in estimating unigram probs
    bigram_laplace (scalar float) = the Laplace smoothing parameter to use in estimating bigram probs
    bigram_lambda (scalar float) = interpolation weight for the bigram model
    pos_prior (scalar float) = the prior probability of the label==1 class
    silently (binary) = if True, don't print anything during computations 

    Outputs:
    dev_labels = the most probable labels (1 or 0) for every email in the dev set
    '''
    print_paramter_vals_bigram(unigram_laplace,bigram_laplace,bigram_lambda,pos_prior)

    max_vocab_size = None
    pos_dict_un, neg_dict_un = create_word_maps_uni(train_set, train_labels, max_size=None)
    pos_dict_bi, neg_dict_bi = create_word_maps_bi(train_set, train_labels, max_size=None)
    total_pos_word_un = 0
    total_neg_word_un = 0
    total_pos_word_bi = 0
    total_neg_word_bi = 0
    pos_len_un = len(pos_dict_un)
    neg_len_un = len(neg_dict_un)
    pos_len_bi = len(pos_dict_bi)
    neg_len_bi = len(neg_dict_bi)
    for num in pos_dict_un.values():
        total_pos_word_un += num
    for num in neg_dict_un.values():
        total_neg_word_un += num
    for num in pos_dict_bi.values():
        total_pos_word_bi += num
    for num in neg_dict_bi.values():
        total_neg_word_bi += num
    dev_label = []


    for email in dev_set:
        pro_pos_un = math.log(pos_prior)
        pro_neg_un = math.log(1 - pos_prior)
        pro_pos_bi = math.log(pos_prior)
        pro_neg_bi = math.log(1 - pos_prior)
        pre_word = ''
        for word in email:
            exist_pos = 0
            exist_neg = 0
            exist_bi_pos = 0
            exist_bi_neg = 0
            if word in pos_dict_un.keys():
                pro_pos_un += math.log((pos_dict_un[word] + unigram_laplace)/(total_pos_word_un + unigram_laplace*(1+pos_len_un))) 
                exist_pos = 1
            if word in neg_dict_un.keys():
                pro_neg_un += math.log((neg_dict_un[word] + unigram_laplace)/(total_neg_word_un + unigram_laplace*(1+neg_len_un)))   
                exist_neg = 1
            if exist_pos == 0:
                pro_pos_un += math.log(unigram_laplace/(total_pos_word_un + unigram_laplace*(1+pos_len_un)))
            if exist_neg == 0:
                pro_neg_un += math.log(unigram_laplace/(total_neg_word_un + unigram_laplace*(1+neg_len_un)))
            
            if pre_word != '':
                cur_word = pre_word + ' ' + word
                if cur_word in pos_dict_bi.keys():
                    pro_pos_bi += math.log((pos_dict_bi[cur_word]+bigram_laplace)/((total_pos_word_bi)+bigram_laplace*(1+pos_len_bi)))
                    exist_bi_pos = 1

                if cur_word in neg_dict_bi.keys():
                    pro_neg_bi += math.log((neg_dict_bi[cur_word]+bigram_laplace)/((total_neg_word_bi)+bigram_laplace*(1+neg_len_bi)))
                    exist_bi_neg = 1

                if exist_bi_pos == 0:
                    pro_pos_bi += math.log(bigram_laplace/((total_pos_word_bi)+bigram_laplace*(1+pos_len_bi)))
                if exist_bi_neg == 0:
                    pro_neg_bi += math.log(bigram_laplace/((total_neg_word_bi)+bigram_laplace*(1+neg_len_bi)))
            
            pre_word = word

        pos_tol = (1-bigram_lambda)*pro_pos_un+bigram_lambda*pro_pos_bi
        neg_tol = (1-bigram_lambda)*pro_neg_un + bigram_lambda*pro_neg_bi
        print(pos_tol, neg_tol)
        if pos_tol > neg_tol:
            dev_label.append(1)
        else:
            dev_label.append(0)    

    return dev_label
# mp4.py
# ---------------
# Licensing Information:  You are free to use or extend this projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to the University of Illinois at Urbana-Champaign
#
# Created Fall 2018: Margaret Fleck, Renxuan Wang, Tiantian Fang, Edward Huang (adapted from a U. Penn assignment)
# Modified Spring 2020: Jialu Li, Guannan Guo, and Kiran Ramnath
# Modified Fall 2020: Amnon Attali, Jatin Arora
# Modified Spring 2021 by Kiran Ramnath
"""
Part 1: Simple baseline that only uses word statistics to predict tags
"""

from unittest import result


def baseline(train, test):
    '''
    input:  training data (list of sentences, with tags on the words)
            test data (list of sentences, no tags on the words)
    output: list of sentences, each sentence is a list of (word,tag) pairs.
            E.g., [[(word1, tag1), (word2, tag2)], [(word3, tag3), (word4, tag4)]]
    ''' 
   
    
    output = {}
    tag_output = {}
    result = []
    temp = []
    for sentence in train:
        for i,cob in enumerate(sentence):
                if i == 0 or i == len(sentence) - 1:
                        continue
                if cob[1] in tag_output.keys():
                        tag_output[cob[1]] += 1
                else:
                        tag_output.update({cob[1]:1})

                if cob[0] in output.keys():
                        if cob[1] in output.get(cob[0]).keys():
                                output.get(cob[0])[cob[1]] += 1
                        else:
                                output.get(cob[0]).update({cob[1]:1})
                else:
                        output.update({cob[0]:{cob[1]:1}})

    for sentence in test:
        for i,word in enumerate(sentence):
                # if i == 0 or i == len(sentence) - 1:
                #         continue
                if word in output.keys():
                        temp.append((word,max(output.get(word), key=output.get(word).get)))
                else:
                        temp.append((word,max(tag_output, key=tag_output.get)))
        result.append(temp)
        temp = []
                
    return result

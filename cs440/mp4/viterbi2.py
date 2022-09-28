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
# Modified Spring 2021 by Kiran Ramnath (kiranr2@illinois.edu)

"""
Part 2: This is the simplest version of viterbi that doesn't do anything special for unseen words
but it should do better than the baseline at words with multiple tags (because now you're using context
to predict the tag).
"""
import math

def backtrace(tr, b_arr, sentence):
	output = [("START", "START")]
	max = -99999
	max_index = 0
	for index, i in enumerate(tr):
		if i[-1][0] > max:
			max = i[-1][0]
			max_index = index
	
	output.append((sentence[-2], tr[max_index][0][1]))
	for index in reversed(range(len(b_arr[0]))):
		if index == 0:
			continue
		#print(index)
		cur_index = b_arr[max_index][index]
		#print(cur_index)
		
		output.insert(1,(sentence[index], tr[cur_index][0][1]))
		max_index = cur_index
		#print(tr[cur_index][0][1])
	output.append(("END", "END"))

	return output

def viterbi_1(train, test):
	

	'''
	input:  training data (list of sentences, with tags on the words)
		   test data (list of sentences, no tags on the words)
	output: list of sentences with tags on the words
			E.g., [[(word1, tag1), (word2, tag2)], [(word3, tag3), (word4, tag4)]]
	'''
	result = []
	k = 0.0001
	tag_pari = {} 
	tag_count = {}
	word_tag_pair = {}
	word_count = {}
	pre_tag = ''

	words = set()
	tags = set()
	for sentence in train:
		for cob in sentence:
			word,tag = cob
			words.add(word)
			tags.add(tag)

	for sentence in train:
		for i, cob in enumerate(sentence):
			
			# word - tag pro 
			if cob[1] not in word_tag_pair.keys(): # if tag not in dict
				word_tag_pair.update({cob[1]: {cob[0] : 1}})
			else:
				if cob[0] not in word_tag_pair[cob[1]].keys(): # tag in word not
					word_tag_pair[cob[1]].update({cob[0] : 1})
				else:
					word_tag_pair[cob[1]][cob[0]] += 1 #both in
			
			if cob[1] not in word_count.keys():
				word_count.update({cob[1]:1}) #update tag count
			else:
				word_count[cob[1]] += 1 




			if i == 0:  # no tag-end pair
				pre_tag = cob[1]
				continue
			#tag - tag pro
			if pre_tag not in tag_pari.keys(): #if pre-tag not in dict
				tag_pari.update({pre_tag : {cob[1]:1}})
			else:
				if cob[1] not in tag_pari[pre_tag].keys(): # if cur-tag not in dict
					tag_pari[pre_tag].update({cob[1]:1})	
				else:
					tag_pari[pre_tag][cob[1]] += 1 #cur tag in dict +1

			if pre_tag not in tag_count.keys(): #count orrcurance of pretag
				tag_count.update({pre_tag: 1})
			else:
				tag_count[pre_tag] += 1	
			pre_tag = cob[1] #update pre_tag


	
	#Transition probabilities 
	for tag in tag_pari.keys():
		count = tag_count[tag]
		for tag_n in tag_pari[tag].keys():
			tag_pari[tag][tag_n] =  math.log((tag_pari[tag][tag_n] + k)/ (count + k*(1+len(tags))))



   #Emission probabilities
	for tag in word_tag_pair.keys():
		count = word_count[tag]
		for word in word_tag_pair[tag].keys():
			word_tag_pair[tag][word] = math.log((word_tag_pair[tag][word] + k) / (count + k*(1+ len(words)))) # how many words


	no_tag = math.log(k/(len(train)  + k*(1+ len(tags))))
	no_word = math.log(k/(len(train) +k*(1+ len(words))))
	ip = math.log(k/(len(train) + k*len(tags)))
	
	for index, sentence in enumerate(test):
		# if index != 6:
		# 	continue
		
		# print(sentence)
		Trellis = [[] for i in range(len(tags) -2)] #discard "start"
		max_index_arr = [ [] for i in range(len(tags) - 2)]
		

		first_tag = sentence[0]
		#Initial probabilities
		index = 0
		for key in tags: #set the initinal prob	
			if key in tag_pari["START"].keys():
				Trellis[index].append([tag_pari["START"][key],key])
				index += 1
			elif key != "END" and key != "START":
				Trellis[index].append([ip,key])
				index += 1
			else:
				continue


		for i , word in enumerate(sentence):
			if i == 0 or i == len(sentence)-1:
				continue
			for l in range(len(Trellis)): # row
				
				cur_tag = Trellis[l][i-1][1]
		
				max = -999999
				max_index = 0
				for m in range(len(Trellis)): #which pre row best
					tag_b = Trellis[m][0][1]
					#judge if word not exist  and tag-pair exist
					if word in word_tag_pair[cur_tag].keys():
						next = Trellis[m][i-1][0]+word_tag_pair[cur_tag][word]
					
					else:
						next = Trellis[m][i-1][0]+no_word
		
					#judge tag-pair exist
					if cur_tag in tag_pari[tag_b].keys():
						next += tag_pari[tag_b][cur_tag]
					else:
						next += no_tag
					if next > max:
						max = next
						max_index = m
					
					
				Trellis[l].append([max, cur_tag])
				max_index_arr[l].append(max_index)
				

		result.append(backtrace(Trellis, max_index_arr, sentence))
		
		

		
	return result
# loading files as a list
# Tokenizing and stemming 
# normalization of the text is yet to finish

import numpy as np
import nltk
import time 
import os
import re
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
import pickle
import sre_constants

def Scanning():
	from os import listdir
	from os.path import isfile, join, isdir, abspath
	path = join("C:\\","/home/chandu/IR-Codes/en_BDNews24/")
	directories = [join(path, dire) for dire in os.listdir(path) if isdir(join(path, dire))]
	directories = sorted(directories)
	# import pdb; pdb.set_trace()
	for dire in directories:
		files = [join(dire, f) for f in os.listdir(dire) if isfile(join(dire, f))]
		totalFiles.append(files)

	return totalFiles

#Tokenizing words
def Tokenizing(text):
	tokenized_doc = list()
	sent_text = nltk.sent_tokenize(text)
	for sentence in sent_text:
		tokenized_text = nltk.word_tokenize(sentence)
		# tagged = nltk.pos_tag(tokenized_text)
		tokenized_doc.append(tokenized_text)

	return tokenized_doc 

def RemoveStopWords(text):
	stop_words = set(stopwords.words('english'))
	filtered_sentence = [word for sent in text for word in sent if not word in stop_words and not word in Extra_characters]
	return filtered_sentence

def Stemming(_list_):
	ps = PorterStemmer()
	stemmed_text = [ps.stem(word) for word in _list_] 
	return stemmed_text

def updatingDictionaries(text, names, original_text):
	# import pdb; pdb.set_trace()
	for word in text:
		word = word.encode('ascii','ignore')
		try:
			pos = [(m.start(), m.end()) for m in re.finditer(word, original_text)]			
		except sre_constants.error:
			# print (word)
			print("!!! {} !!!".format(word))
		freq = len(pos)
		val = {'document':names,'frequency': freq, 'position':pos}
		if word in _dict_:
			_dict_[word].append(val)
		else:
			_dict_[word] = list()
			_dict_[word].append(val)

def ChangeKey(text_withoutStopWords, stemmed_text):
	i=0
	text_withoutStopWords = sorted(text_withoutStopWords)
	stemmed_text = sorted(stemmed_text)
	import pdb; pdb.set_trace()
	for i in range(len(stemmed_text)):
		_dict_[stemmed_text[i]]=_dict_.pop(text_withoutStopWords[i])
		i+=1

def Process():
	for files in totalFiles:
		for file in files:
			filename, dir_name = os.path.basename(file), os.path.basename(os.path.dirname(file)) 
			names = [filename, dir_name]
			f_object = open(file, "r")
			text = f_object.read()
			x = re.findall(r'<TEXT>(.*?)</TEXT>', text, re.DOTALL)
			original_text = "".join(x).replace('\n', '')
			original_text = original_text.lower()
			tokenized_doc = Tokenizing(original_text)
			# import pdb; pdb.set_trace()
			text_withoutStopWords = RemoveStopWords(tokenized_doc)
			# UpdatePos(text_withoutStopWords)
			updatingDictionaries(text_withoutStopWords, names, text.lower())
			stemmed_text = Stemming(text_withoutStopWords)
			# updatingDictionaries(stemmed_text, names, text)
			ChangeKey(text_withoutStopWords, stemmed_text)


def main():
	st = time.clock()
	global totalFiles
	totalFiles = list()
	Scanning()
	end = time.clock()
	print ("time taken in scanning: ", end-st)
	global _dict_
	_dict_ = {}

	global Extra_characters
	Extra_characters = ['(', ')','!', '@', '#', '$', '%', "''", '^', '&', '*', ',', '.', '~', '_', '-', '/', '""', ' ', '<', '>', '`', '=', '+', '?', '|', ':', ';', '``', '[', ']', '{', '}', ]
	st = time.clock()
	Process()
	end = time.clock()
	print ("time taken in creating dictionaries: ", end-st)
	
	# print ("dictionary: ", _dict_)
	with open('index.pickle', 'wb') as handle:
		pickle.dump(_dict_, handle, protocol=pickle.HIGHEST_PROTOCOL)

if __name__=="__main__":
	main()
import numpy as np
import pickle
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
from sets import Set
import time

def main():
	st = time.clock()
	with open('index.pickle', 'rb') as handle:
		_dict_ = pickle.load(handle)
	end = time.clock()
	print ("Time taken in loading pickle file:", end-st	)
	# import pdb; pdb.set_trace()
	string = input("Give query you want to search: ")
	string = string.lower()
	lt = string.split()
	#removing stop words
	stop_words = set(stopwords.words('english'))
	filtered_sentence = [word for word in lt if not word in stop_words]

	#Stemming
	ps = PorterStemmer()
	stemmed_text = [ps.stem(word) for word in filtered_sentence]

	_list_ = list()	
	for word in stemmed_text:
		word = word.encode('ascii','ignore')
		if word in _dict_:
			_list_.append(set(_dict_[word]))
	# import pdb; pdb.set_trace()
	

	if len(_list_)==0:
		print ("No Result Found")

	else:
		print("Similar words are found in the following files: ")
		intersection = set.intersection(*_list_)
		union = set.union(*_list_)
		if len(intersection) > 20:
			print(intersection[0:20])
			print("#----------------------------------------------------#")
			print (union[0:20])

		else:
			print(intersection)
			print("#----------------------------------------------------#")
			if len(union)>20:
				print(union[0:20])
			else:
				print(union)


if __name__=="__main__":
	main()
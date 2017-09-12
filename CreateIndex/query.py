import numpy as np
import pickle
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
from sets import Set
import time
import operator

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

	#
	_list_ = list()
	# _dict_ = sorted(_dict_.items(), key=operator.itemgetter(0))	
	for word in stemmed_text:
		word = word.encode('ascii','ignore')
		if word in _dict_:
			temp = _dict_[word]
			_list_.append(temp)

	# lt = list()
	# for item in _list_:
	# 	for d in item:
	# 		temp = sorted(d.items(), key=operator.itemgetter(0))
	# 		lt.append(temp)

	# import pdb; pdb.set_trace()
	

	if len(_list_)==0:
		print ("No Result Found")

	else:
		print("Similar words are found in the following files: ")
		print(_list_)
		# intersection = set.intersection(*set(lt))
		# union = set.union(*set(lt))
		# if len(intersection) > 20:
		# 	print("\n".join(intersection[0:20]))
		# 	print("#----------------------------------------------------#")
		# 	print ("\n".join(union[0:20]))

		# else:
		# 	print(intersection)
		# 	print("#----------------------------------------------------#")
		# 	if len(union)>20:
		# 		print("\n".join(union[0:20]))
		# 	else:
		# 		print("\n".join(union))


if __name__=="__main__":
	main()
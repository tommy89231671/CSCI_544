import sys
from collections import defaultdict
import json
word_dict=defaultdict()

tag_tag_tr_matrix={} #P(tag|previous_tag)
tag_tag_size_dict={}
tag_word_em_matrix={} #P(word|tag)
tag_word_size_dict={}


def read_txt(path):
	f=open(path,"r")
	# print(len(f.read().split('\n')))
	for sentence in f.read().split('\n'):
		# print(sentence)
		pre_tag="INIT"
		for word_and_tag in sentence.split(' '):
			tmp=word_and_tag.split('/')
			word="".join(tmp[:-1])
			tag=tmp[-1]
			if pre_tag in tag_tag_tr_matrix:
				if tag in tag_tag_tr_matrix[pre_tag]:
					tag_tag_tr_matrix[pre_tag][tag]+=1
				else:
					tag_tag_tr_matrix[pre_tag].update({tag:1})
			else:
				tag_tag_tr_matrix.update({pre_tag:{tag:1}})

			if tag in tag_word_em_matrix:
				if word in tag_word_em_matrix[tag]:
					tag_word_em_matrix[tag][word]+=1
				else:
					tag_word_em_matrix[tag].update({word:1})
			else:
				tag_word_em_matrix.update({tag:{word:1}})

			pre_tag=tag
	# print(len(tag_word_em_matrix),len(tag_tag_tr_matrix))
	# print(tag_tag_tr_matrix["INIT"])
	for key in tag_tag_tr_matrix:
		tag_tag_size_dict.update({key:sum(tag_tag_tr_matrix[key].values())})
	for key in tag_word_em_matrix:
		tag_word_size_dict.update({key:sum(tag_word_em_matrix[key].values())})
	# print(tag_word_size_dict)
	# print(tag_tag_size_dict)

	# print(word_dict)






if __name__ == "__main__":
	arg=sys.argv
	path=arg[1]
	read_txt(path)
	f=open("hmmmodel.txt","w")
	write_list=[tag_tag_tr_matrix,tag_tag_size_dict,tag_word_em_matrix,tag_word_size_dict]
	f.write(json.dumps(write_list, ensure_ascii=False))

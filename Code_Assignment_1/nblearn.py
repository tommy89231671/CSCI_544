import os,sys
import re
import math
import json

def read_document_to_dict(path,pos_neg_num,tru_dec_num,pos_neg_dict,tru_dec_dict):
    for dir in os.listdir(path):
        if dir[0]!=".":
            for subdir in os.listdir(path+"/"+dir):
                f=open(path+"/"+dir+"/"+subdir,"r")
                document=re.sub(r'[^\w]', ' ', f.read())

                for word in set(document.lower().split()):
                    pos_neg_num+=1
                    tru_dec_num+=1
                    total_word_set.add(word)
                    if word in pos_neg_dict:
                        pos_neg_dict[word]+=1
                    else:
                        pos_neg_dict.update({word:1})

                    if word in tru_dec_dict:
                        tru_dec_dict[word]+=1
                    else:
                        tru_dec_dict.update({word:1})
    return pos_neg_num,tru_dec_num,pos_neg_dict,tru_dec_dict

if __name__ == "__main__":
    arg=sys.argv
    root=arg[1]
    pos_dec_path = root+"/positive_polarity/deceptive_from_MTurk"
    pos_tru_path =  root+"/positive_polarity/truthful_from_TripAdvisor"

    neg_dec_path =  root+"/negative_polarity/deceptive_from_MTurk"
    neg_tru_path =  root+"/negative_polarity/truthful_from_Web"

    pos_word_dict={}
    neg_word_dict={}
    tru_word_dict={}
    dec_word_dict={}
    total_word_set=set()
    pos_word_num=0
    neg_word_num=0
    tru_word_num=0
    dec_word_num=0

    pos_word_num,tru_word_num,pos_word_dict,tru_word_dict=read_document_to_dict(pos_tru_path,pos_word_num,tru_word_num,pos_word_dict,tru_word_dict)
    pos_word_num,dec_word_num,pos_word_dict,dec_word_dict=read_document_to_dict(pos_dec_path,pos_word_num,dec_word_num,pos_word_dict,dec_word_dict)
    neg_word_num,tru_word_num,neg_word_dict,tru_word_dict=read_document_to_dict(neg_tru_path,neg_word_num,tru_word_num,neg_word_dict,tru_word_dict)
    neg_word_num,dec_word_num,neg_word_dict,dec_word_dict=read_document_to_dict(neg_dec_path,neg_word_num,dec_word_num,neg_word_dict,dec_word_dict)

    f=open("nbmodel.txt","w")
    num_dict={"pos_word_num":pos_word_num,"neg_word_num":neg_word_num,"tru_word_num":tru_word_num,"dec_word_num":dec_word_num,"total_word_num":len(total_word_set)}
    write_list=[num_dict,pos_word_dict,neg_word_dict,tru_word_dict,dec_word_dict]

    f.write(json.dumps(write_list))

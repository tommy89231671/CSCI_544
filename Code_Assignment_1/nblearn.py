import os,sys
import re
import math
import json

def read_document_to_dict(path,pos_neg_num,tru_dec_num,pos_neg_dict,tru_dec_dict):
    for dir in os.listdir(path):
        if dir[0]!="." and dir!="fold1":
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




# def predict(path,pos_word_dict,neg_word_dict,tru_word_dict,dec_word_dict,pos_word_num,neg_word_num,tru_word_num,dec_word_num):
#     predict_pos=0
#     predict_neg=0
#     predict_tru=0
#     predict_dec=0
#     for dir in os.listdir(path):
#         if dir=="fold1":
#             for subdir in os.listdir(path+"/"+dir):
#                 f=open(path+"/"+dir+"/"+subdir,"r")
#                 document=re.sub(r'[^\w]', ' ', f.read())
#                 pos_prob=0
#                 neg_prob=0
#                 tru_prob=0
#                 dec_prob=0
#                 for word in set(document.lower().split()):
#                     if word in pos_word_dict:
#                         pos_prob+=math.log((pos_word_dict[word]+1)/(len(pos_word_dict)+len(total_word_set)))
#                     else:
#                         pos_prob+=math.log(1/(len(pos_word_dict)+len(total_word_set)))
#                     if word in neg_word_dict:
#                         neg_prob+=math.log((neg_word_dict[word]+1)/(len(neg_word_dict)+len(total_word_set)))
#                     else:
#                         neg_prob+=math.log(1/(len(neg_word_dict)+len(total_word_set)))
#
#                     if word in tru_word_dict:
#                         tru_prob+=math.log((tru_word_dict[word]+1)/(len(tru_word_dict)+len(total_word_set)))
#                     else:
#                         tru_prob+=math.log(1/(len(tru_word_dict)+len(total_word_set)))
#                     if word in dec_word_dict:
#                         dec_prob+=math.log((dec_word_dict[word]+1)/(len(dec_word_dict)+len(total_word_set)))
#                     else:
#                         dec_prob+=math.log(1/(len(dec_word_dict)+len(total_word_set)))
#
#                 if pos_prob>=neg_prob:
#                     predict_pos+=1
#                 else:
#                     predict_neg+=1
#                 if tru_prob>=dec_prob:
#                     predict_tru+=1
#                 else:
#                     predict_dec+=1
#     print("pos:",predict_pos,", neg:",predict_neg)
#     print("tru:",predict_tru,", dec:",predict_dec)
def predict(path,pos_word_dict,neg_word_dict,tru_word_dict,dec_word_dict,pos_word_num,neg_word_num,tru_word_num,dec_word_num,total_word_num):
    predict_pos=0
    predict_neg=0
    predict_tru=0
    predict_dec=0
    for dir in os.listdir(path):
        if dir=="fold1":
            for subdir in os.listdir(path+"/"+dir):
                f=open(path+"/"+dir+"/"+subdir,"r")
                document=re.sub(r'[^\w]', ' ', f.read())
                pos_prob=0
                neg_prob=0
                tru_prob=0
                dec_prob=0
                for word in set(document.lower().split()):
                    if word in pos_word_dict:
                        pos_prob+=math.log((pos_word_dict[word]+1)/(pos_word_num+total_word_num))
                    else:
                        pos_prob+=math.log(1/(pos_word_num+total_word_num))
                    if word in neg_word_dict:
                        neg_prob+=math.log((neg_word_dict[word]+1)/(neg_word_num+total_word_num))
                    else:
                        neg_prob+=math.log(1/(neg_word_num+total_word_num))

                    if word in tru_word_dict:
                        tru_prob+=math.log((tru_word_dict[word]+1)/(tru_word_num+total_word_num))
                    else:
                        tru_prob+=math.log(1/(tru_word_num+total_word_num))
                    if word in dec_word_dict:
                        dec_prob+=math.log((dec_word_dict[word]+1)/(dec_word_num+total_word_num))
                    else:
                        dec_prob+=math.log(1/(dec_word_num+total_word_num))

                if pos_prob>=neg_prob:
                    predict_pos+=1
                else:
                    predict_neg+=1
                if tru_prob>=dec_prob:
                    predict_tru+=1
                else:
                    predict_dec+=1
    # print("pos:",predict_pos,", neg:",predict_neg)
    # print("tru:",predict_tru,", dec:",predict_dec)



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
    # f.write("pos_word_num:"+str(pos_word_num)+"\n\n")
    # f.write("neg_word_num:"+str(neg_word_num)+"\n\n")
    # f.write("tru_word_num:"+str(tru_word_num)+"\n\n")
    # f.write("dec_word_num:"+str(dec_word_num)+"\n\n")
    write_list=[num_dict,pos_word_dict,neg_word_dict,tru_word_dict,dec_word_dict]

    f.write(json.dumps(write_list))


    """development test"""
    # print(pos_word_num,neg_word_num,tru_word_num,dec_word_num)
    # print(len(pos_word_dict),len(neg_word_dict),len(total_word_set))

    # predict(pos_tru_path,pos_word_dict,neg_word_dict,tru_word_dict,dec_word_dict,pos_word_num,neg_word_num,tru_word_num,dec_word_num,len(total_word_set))
    # predict(pos_dec_path,pos_word_dict,neg_word_dict,tru_word_dict,dec_word_dict,pos_word_num,neg_word_num,tru_word_num,dec_word_num,len(total_word_set))
    # predict(neg_tru_path,pos_word_dict,neg_word_dict,tru_word_dict,dec_word_dict,pos_word_num,neg_word_num,tru_word_num,dec_word_num,len(total_word_set))
    # predict(neg_dec_path,pos_word_dict,neg_word_dict,tru_word_dict,dec_word_dict,pos_word_num,neg_word_num,tru_word_num,dec_word_num,len(total_word_set))

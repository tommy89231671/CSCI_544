import json
import sys
import os
import re
import math
def predict(path,pos_word_dict,neg_word_dict,tru_word_dict,dec_word_dict,pos_word_num,neg_word_num,tru_word_num,dec_word_num,total_word_num):
    predict_pos=0
    predict_neg=0
    predict_tru=0
    predict_dec=0
    result=""
    # for dir in os.listdir(path):
    for file in os.listdir(path):
        f=open(path+"/"+file,"r")
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

        # if pos_prob>=neg_prob:
        #     predict_pos+=1
        # else:
        #     predict_neg+=1
        # if tru_prob>=dec_prob:
        #     predict_tru+=1
        # else:
        #     predict_dec+=1

        label1="truthful" if tru_prob>=dec_prob else "deceptive"
        label2="positive" if pos_prob>=neg_prob else "negative"
        result+=label1+" "+label2+" "+path+file+"\n"
    f=open("nboutput.txt","w")
    f.write(result)
    # print("pos:",predict_pos,", neg:",predict_neg)
    # print("tru:",predict_tru,", dec:",predict_dec)

if __name__ == "__main__":
    arg=sys.argv
    path=arg[1]

    # pos_dec_path = root+"/positive_polarity/deceptive_from_MTurk/fold1"
    # pos_tru_path =  root+"/positive_polarity/truthful_from_TripAdvisor/fold1"
    #
    # neg_dec_path =  root+"/negative_polarity/deceptive_from_MTurk/fold1"
    # neg_tru_path =  root+"/negative_polarity/truthful_from_Web/fold1"

    with open("nbmodel.txt") as modelfile:
         model= json.load(modelfile)
    # print(model[0])
    pos_word_num=model[0]["pos_word_num"]
    neg_word_num=model[0]["neg_word_num"]
    tru_word_num=model[0]["tru_word_num"]
    dec_word_num=model[0]["dec_word_num"]
    total_word_num=model[0]["total_word_num"]

    pos_word_dict=model[1]
    neg_word_dict=model[2]
    tru_word_dict=model[3]
    dec_word_dict=model[4]

    predict(path,pos_word_dict,neg_word_dict,tru_word_dict,dec_word_dict,pos_word_num,neg_word_num,tru_word_num,dec_word_num,total_word_num)

    # predict(pos_tru_path,pos_word_dict,neg_word_dict,tru_word_dict,dec_word_dict,pos_word_num,neg_word_num,tru_word_num,dec_word_num,total_word_num)
    # predict(pos_dec_path,pos_word_dict,neg_word_dict,tru_word_dict,dec_word_dict,pos_word_num,neg_word_num,tru_word_num,dec_word_num,total_word_num)
    # predict(neg_tru_path,pos_word_dict,neg_word_dict,tru_word_dict,dec_word_dict,pos_word_num,neg_word_num,tru_word_num,dec_word_num,total_word_num)
    # predict(neg_dec_path,pos_word_dict,neg_word_dict,tru_word_dict,dec_word_dict,pos_word_num,neg_word_num,tru_word_num,dec_word_num,total_word_num)

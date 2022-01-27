import json
import sys
import os
import re
import math
def predict(root_path,pos_word_dict,neg_word_dict,tru_word_dict,dec_word_dict,pos_word_num,neg_word_num,tru_word_num,dec_word_num,total_word_num):
    predict_pos=0
    predict_neg=0
    predict_tru=0
    predict_dec=0
    result=""

    for root, dirs, files in os.walk(root_path):
        for file in files:
            if file.endswith(".txt") and file!="README.txt":
                file_path=os.path.join(root, file)
                f=open(file_path,"r")
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
                label1="truthful" if tru_prob>=dec_prob else "deceptive"
                label2="positive" if pos_prob>=neg_prob else "negative"
                result+=label1+" "+label2+" "+file_path+"\n"

            f=open("nboutput.txt","w")
            f.write(result)

if __name__ == "__main__":
    arg=sys.argv
    path=arg[1]

    with open("nbmodel.txt") as modelfile:
         model= json.load(modelfile)

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

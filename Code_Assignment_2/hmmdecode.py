import json



if __name__ == "__main__":
    with open("hmmmodel.txt") as modelfile:
         model= json.load(modelfile)
    tag_tag_tr_matrix=model[0] #P(tag|previous_tag)
    tag_tag_size_dict=model[1]
    tag_word_em_matrix=model[2]#P(word|tag)
    tag_word_size_dict=model[3]
    

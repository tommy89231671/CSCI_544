import json
import sys
import math
import copy
class ListNode:
    def __init__(self, val=0, parent=None):
        self.val = val
        self.parent = parent
tag_tag_tr_matrix = {} #P(tag|previous_tag)
tag_tag_size_dict = {}
tag_word_em_matrix = {}#P(word|tag)
tag_word_size_dict = {}
word_set = set()


tag_list=[]
def predict(raw_path):
    # f_tagged = open(tagged_path,"r")
    f_raw = open(raw_path,"r")
    f_outout = open("hmmoutput.txt",'w')
    # for sentence in f_tagged.read().split('\n'):
    result_str=""
    raw_split = f_raw.read().split('\n')

    for iii,sentence in enumerate(raw_split):
        state_pre_prob_dict={}
        state_prob_dict={}
        state_pretag_object_dict={}
        state_tag_object_dict={}
        total_num_tag=len(tag_tag_size_dict)
        head=ListNode("INIT")
        groundtru=[]
        for key in tag_tag_size_dict:
            if key in tag_tag_tr_matrix['INIT']:
                state_pre_prob_dict.update({key:tag_tag_tr_matrix["INIT"][key]/tag_tag_size_dict['INIT']})
                state_pretag_object_dict.update({key:ListNode(key,head)})
            else:
                state_pre_prob_dict.update({key:0})
                state_pretag_object_dict.update({key:ListNode(key,head)})

        # for word_and_tag in sentence.split(' '):
        for word in sentence.split(' '):
            # tmp = word_and_tag.split('/')
            # word = "".join(tmp[:-1])
            # tag = tmp[-1]
            # print(word)
            # groundtru.append(tag)
            for key in tag_list:
                pre_tag=""
                if key!="INIT":
                    if word in word_set:
                        if word in tag_word_em_matrix[key]:
                            em_prob = tag_word_em_matrix[key][word]/tag_word_size_dict[key]
                            max_tmp_prob = -math.inf
                            for pre_key in tag_list: # find highest prob and pre_key
                                tmp_prob = 1;
                                if key in tag_tag_tr_matrix[pre_key]:
                                    # print(key,pre_key,state_pre_prob_dict[pre_key])
                                    tmp_prob = (1+tag_tag_tr_matrix[pre_key][key])/(tag_tag_size_dict[pre_key]+total_num_tag)\
                                        * state_pre_prob_dict[pre_key]
                                else:
                                    tmp_prob = 1/(tag_tag_size_dict[pre_key]+total_num_tag) * state_pre_prob_dict[pre_key]
                                if tmp_prob>max_tmp_prob:
                                    max_tmp_prob = tmp_prob
                                    pre_tag = pre_key
                            state_prob_dict.update({key:em_prob*max_tmp_prob})
                            state_tag_object_dict.update({key:ListNode(key,state_pretag_object_dict[pre_tag])})
                            # print("state_pre_prob_dict\n",state_pre_prob_dict)
                            # print("state_prob_dict\n",state_prob_dict)
                        else:
                             state_prob_dict.update({key:0})
                             state_tag_object_dict.update({key:ListNode(key,None)})
                    else:
                        # print(word," not in word_set")
                        max_tmp_prob = -math.inf
                        for pre_key in tag_list: # find highest prob and pre_key
                            tmp_prob = 1;
                            if key in tag_tag_tr_matrix[pre_key]:
                                tmp_prob = (1+tag_tag_tr_matrix[pre_key][key])/(tag_tag_size_dict[pre_key]+total_num_tag)\
                                    * state_pre_prob_dict[pre_key]

                            else:
                                tmp_prob = 1/(tag_tag_size_dict[pre_key]+total_num_tag) * state_pre_prob_dict[pre_key]
                            if tmp_prob>max_tmp_prob:
                                max_tmp_prob = tmp_prob
                                pre_tag = pre_key
                        state_prob_dict.update({key:max_tmp_prob})
                        state_tag_object_dict.update({key:ListNode(key,state_pretag_object_dict[pre_tag])})
                else:
                    state_prob_dict.update({"INIT":0})
                    state_tag_object_dict.update({"INIT":ListNode("INIT",None)})
                # print(pre_tag)
                # input()
            state_pretag_object_dict =  copy.deepcopy(state_tag_object_dict)
            state_pre_prob_dict =  copy.deepcopy(state_prob_dict)
        predict_last_tag=max(state_prob_dict, key=state_prob_dict.get)
        cur_object=state_tag_object_dict[predict_last_tag]
        predict_tag_list=[]
        while cur_object !=None:
            # print(cur_object.val)
            predict_tag_list.insert(0,cur_object.val)
            cur_object = cur_object.parent
            # predict_last_tag=predict_last_tag.parent
        # print("GT:",groundtru)
        word_list=sentence.split()
        predict_tag_list=predict_tag_list[2:]

        for i in range(len(sentence.split())):
            result_str+=word_list[i]+"/"+predict_tag_list[i]+" "
        if iii<len(raw_split)-1:
            result_str+="\n"
        # print(result_str)
        # print(len(sentence.split()),sentence.split())
        # print(len(predict_tag_list[2:]),predict_tag_list[2:])
        # print()
        # print("sentence end")

        # input()
    f_outout.write(result_str)





if __name__ == "__main__":
    arg = sys.argv
    with open("hmmmodel.txt") as modelfile:
         model = json.load(modelfile)
    tag_tag_tr_matrix = model[0] #P(tag|previous_tag)
    tag_tag_size_dict = model[1]
    tag_word_em_matrix = model[2]#P(word|tag)
    tag_word_size_dict = model[3]
    tag_list=list(tag_tag_size_dict.keys())

    for tag in tag_word_em_matrix:
        for word in tag_word_em_matrix[tag]:
            word_set.add(word)
    tagged_path = "./hmm-training-data/ja_gsd_dev_tagged.txt"
    raw_path = "./hmm-training-data/ja_gsd_dev_raw.txt"
    predict(arg[1])

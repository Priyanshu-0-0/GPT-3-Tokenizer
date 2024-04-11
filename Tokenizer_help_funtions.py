def get_pair_counts(text):
    pair_dict={}

    for i in range(len(text) - 1):
        pair = (text[i],text[i+1])
        if pair in pair_dict:
            pair_dict[pair] += 1
        else:
            pair_dict[pair] = 1

    return pair_dict 


def pair_switch(token,pair,new_pair):
    i=0
    np=[]
    while i < len(token):
        if i<len(token)-1 and token[i] and token[i]==pair[0] and token[i+1]==pair[1]:
            np.append(new_pair)
            i+=2
        else :
            np.append(token[i])
            i+=1
    return np



#!/usr/bin/env python
# coding: utf-8

# In[2]:

import math
import numpy as np
import pickle
from sys import argv

# How this file works: given 3 inputs ( list of ids to evaluate ), dssp directory, dictionary with predictions key=ID, value=dssp_prediction (binary) , output file

def n_class_confmatrix(reald,predd):
    """Given two dictionaries {ID:sequence} the first real the second containing the predictions, return a n-class matrix confusion matrix for the dssp structure"""
    cf=np.zeros(shape=(3,3))
    classes="HEC"
    
    for key in predd:
        rseq=reald[key]
        pseq=predd[key]
        for i in range(len(pseq)):
            p=pseq[i]   #predicted residue 
            r=rseq[i]   #real residue 
            cf[classes.find(r)][classes.find(p)]+=1  #the cf has in the rows the real classes and in the col the predicted ones
    return cf

def get_metrics(cf):
    d={}
    diag=0
    for i in range(len(cf)):
        diag+=cf[i][i]
    
    acc3=diag/cf.sum()
    d["acc_3classes"]=acc3
    
    sss="HEC"
    acc_H_E_C=[]
    for i in range(3):
        tp=cf[i][i]
        fp=sum([cf[a][i] for a in range(len(cf))])-tp
        fn=sum([cf[i][a] for a in range(len(cf[i]))])-tp
        tn=cf.sum()-tp-fp-fn
        #print(sss[i],"tp "+str(tp)+" fp "+str(fp)+" fn "+str(fn)+" tn "+str(tn)) --> used to visualize the binary conf matrix
        acc=(tp+tn)/(tp+tn+fp+fn)
        ppv=tp/(tp+fp)
        rec=tp/(tp+fn)
        mcc=((tp*tn)-(fp*fn))/math.sqrt((tp+fp)*(tp+fn)*(tn+fp)*(tn+fn))
        
        d["acc_"+sss[i]]=acc
        d["ppv_"+sss[i]]=ppv
        d["rec_"+sss[i]]=rec
        d["mcc_"+sss[i]]=mcc
        
    return d   
        



IDS=open(argv[1],"r")
dsspdir=argv[2]
predictedfile=open(argv[3],"rb")
predictionary=pickle.load(predictedfile)
predictedfile.close()

realdictionary={}

for item in IDS:
    ID=item.rstrip()
    #print(ID)
    try:
        dsspfile=open(dsspdir+ID+".dssp","r")
    except:
        print("profile for "+ID+" not found")
        continue

    for line in dsspfile:
        if line[0]!=">" and line[0]!="\n":
            line=line.rstrip()
        realdictionary[ID]=line
    dsspfile.close()

    #except:
        #print("profile for {} does not exists".format(ID))
        #continue
IDS.close()

CF=n_class_confmatrix(realdictionary,predictionary)
#print(CF)
results=open(argv[4],"wb")
pickle.dump(get_metrics(CF),results)
results.close()

print(get_metrics(CF))
    #get_metrics(CF)

#!/usr/bin/env python
# coding: utf-8

# In[3]:


import pickle
import numpy as np
from sys import argv

#How to use this script: \n1st arg: IDs list you want to predict, \n2nd arg: dictionary gor infomatrices (binary), \n3rd: profiles directory of IDs, \n4th: [OUTPUT] dictionary (key=ID,value=dssp prediction)"  

outfile=argv[4]
profilesdir=argv[3] 
matrices=open(argv[2],"rb")     
M=pickle.load(matrices)
matrices.close()
topred=open(argv[1],"r")        
idlist=[]
for ID in topred:
    idlist.append(ID.rstrip())
topred.close()

# In[25]:
   
def pred_dssp(prof):
    """Get a sequence and its profile as inputs and returns its prediction"""
    prof=np.vstack((np.zeros(shape=(8,20)),prof))
    prof=np.vstack((prof,np.zeros(shape=(8,20))))
    
    predicted=""
    
    for i in range(0,len(prof)-16):
        p=prof[i:i+17]
     
        PD={}
        for el in M:
            if el=="OV":
                continue
            else:
                tot=(p*M[el]).sum()
                PD[el]=tot
        
        prediction=max(PD,key=PD.get) # returns the key with the highest value
        if prediction=="C":
            prediction="-"
        predicted+=prediction
        #moltiplica le due matrici (eg: p e M["H"]) e poi fai la .sum() per ottenere la predizione

    return predicted


# In[37]:


predictionary={}

for ID in idlist:
    try:
        profile=open(profilesdir+ID+".txt","r")
        prof=np.loadtxt(profile)
        
    except:
            print("No profile available for %s" %ID)
            continue
            
   
    dsspP=pred_dssp(prof)
    predictionary[ID]=dsspP
    profile.close()
    
out=open(outfile,"wb")
pickle.dump(predictionary,out)
out.close()

    

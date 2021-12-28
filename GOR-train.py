#!/usr/bin/env python
# coding: utf-8
import numpy as np
from sys import argv
import pickle

# How to use this script: 1st input : training list ids , 2nd: output file (dictionary with infomatrices, binary), 3rd: dssp directory, 4th : profiles directory

H=np.zeros(shape=(17,20))
E=np.zeros(shape=(17,20))
C=np.zeros(shape=(17,20))
OV=np.zeros(shape=(17,20))

idlist=open(argv[1],"r")
idl=[]
for item in idlist:
    idl.append(item.rstrip())

idlist.close()


for item in idl:
    try:
        dsspfile=open(argv[3]+item+".dssp","r")  #open("../dssps/{}.dssp".format(item),"r") 
        for line in dsspfile:
            if line[0]!= ">":
                dssp=line.rstrip()
        #print(item,"\n",dssp)
        dsspfile.close()
        profile=open(argv[4]+item+".txt","r") #open("../profiles/{}.txt".format(item),"r")
        pr=np.loadtxt(profile)
        profile.close()
        pr=np.vstack((np.zeros(shape=(8,20)),pr))
        pr=np.vstack((pr,np.zeros(shape=(8,20))))
        for i in range(0,len(dssp)): 

            prof=pr[i:i+17]  

            if dssp[i]=="H":
                for r in range(17):
                    H[r]=H[r]+prof[r]
            elif dssp[i]=="E":
                for r in range(17):
                    E[r]=E[r]+prof[r]
            elif dssp[i]=="-":
                for r in range(17):
                    C[r]=C[r]+prof[r]

            for r in range(17):
                    OV[r]=OV[r]+prof[r]
    except:
        pass

# computing ss probabilities
HP=sum(H[8])/sum(OV[8]) #p(H)
EP=sum(E[8])/sum(OV[8]) #p(E)
CP=sum(C[8])/sum(OV[8]) #p(C)

# creating a list which stores each infomatrix

l=[H,E,C,OV]

# normalization
for r in range(len(OV)):
    tot=sum(OV[r])
    for matrix in l:
        for c in range(len(matrix[r])):
            matrix[r][c]=matrix[r][c]/tot

# computing log for each matrix

for r in range(len(l[0])):
    for c in range(len(l[0][r])):
        l[0][r][c]=np.log(l[0][r][c]/(HP*OV[r][c]))
        # l[1][r][c]=np.log(l[1][r][c]/(EP*OV[r][c])) 
        # l[2][r][c]=np.log(l[2][r][c]/(CP*OV[r][c]))   ---> just ONE LOOP 
        
        
for r in range(len(l[1])):
    for c in range(len(l[1][r])):
        l[1][r][c]=np.log(l[1][r][c]/(EP*OV[r][c]))  

for r in range(len(l[2])):
    for c in range(len(l[2][r])):
        l[2][r][c]=np.log(l[2][r][c]/(CP*OV[r][c]))

    
d={"H":l[0],"E":l[1],"C":l[2],"OV":l[3]}            

                
matrix=open(argv[2],"wb")
pickle.dump(d,matrix)
matrix.close()


#### AGGIUNGI argv[3] e argv[4] to add directory and not hardcoding my files . I can also skip the for loops to iterate over H and prof since I can just do prof+H .  professor suggested also to use dictionary to one-line encode my matrices (d[dssp[i]]=d[dssp[i]]+prof

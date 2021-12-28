from sys import argv
import numpy as np
import pickle,gzip
from sklearn import svm

# Inputs : training ID list , dssp directory, profiles directory,MODELNAME (eg: model0123 for set 0123)
#Outputs: MODELNAME_[01][01].pkl . 0 and 1 refers to the GRID SEARCH table cells (eg: 00 is (C=2,Y=0.5)) #4 outputs in total (00,01,10,11)


idlist=[]
idlistfile=open(argv[1],"r")
for line in idlistfile:
	idlist.append(line.rstrip())
idlistfile.close()

dsspdir=argv[2]
profiledir=argv[3]
outname=argv[4]

featurematrix=[]
classarray=[]
for id in idlist:
	try:
		dssp=open(dsspdir+id+".dssp","r")
		profile=open(profiledir+id+".txt","r")
	except:
		print(id+" not found")  # 96 ids not found
		continue
	for line in dssp:
		if line[0]!=">":
			seq=line.rstrip()

	prof=np.loadtxt(profile)
	prof=np.vstack((np.zeros(shape=(8,20)),prof,np.zeros(shape=(8,20))))

	for i in range(len(seq)):
		p=prof[i:i+17]
		if seq[i]=="H":
			classarray.append(1)
		elif seq[i]=="E":
			classarray.append(2)
		elif seq[i]=="C" or seq [i]=="-":
			classarray.append(3)
		features=p.flatten().tolist()
		featurematrix.append(features)
	#print(len(classarray),len(seq),"\n",classarray,seq)
	dssp.close()
	profile.close()

#print(len(classarray),classarray[0:2])
#print(len(featurematrix),featurematrix[0:2])

modname=argv[4]




r00=open(modname+"_00.pkl","wb")
SVC00=svm.SVC(C=2.0, kernel='rbf', gamma=0.5)
SVC00.fit(featurematrix,classarray)
pickle.dump(SVC00,r00)
r00.close()


'''r01=open(modname+"_01.pkl","wb")
SVC01=svm.SVC(C=2.0, kernel='rbf', gamma=2.0)
SVC01.fit(featurematrix,classarray)
pickle.dump(SVC01,r01)
r01.close()

r10=open(modname+"_10.pkl","wb")
SVC10=svm.SVC(C=4.0, kernel='rbf', gamma=0.5)
SVC10.fit(featurematrix,classarray)
pickle.dump(SVC10,r10)
r10.close()

r11=open(modname+"_11.pkl","wb")
SVC11=svm.SVC(C=4.0, kernel='rbf', gamma=2.0)
SVC11.fit(featurematrix,classarray)
pickle.dump(SVC11,r11)
r11.close()

'''

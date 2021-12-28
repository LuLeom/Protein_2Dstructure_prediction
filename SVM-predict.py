from sys import argv
import pickle
import numpy as np
from sklearn import svm

# Inputs :[1] id list to predict,[2] directory with sequence profiles to predict,[3] model pickle (eg: model0123_00.pkl)  # Output: dictionary with key=ID, value=predicted seq) = RESULTS_[3]

idlistfile=open(argv[1],"r")
profdir=argv[2]

idlist=[]
for line in idlistfile:
        idlist.append(line.rstrip())
idlistfile.close()

SVC00=pickle.load(open(argv[3],"rb"))
#SVC01=pickle.load(argv[4],"rb")
#SVC10=pickle.load(argv[5],"rb")
#SVC11=pickle.load(argv[6],"rb")

#classifiers=[SVC00,SVC01,SVC10,SVC11]

predictionary={}

for id in idlist:
	try:
		profile=open(profdir+id+".txt","r")
		#print("%s found" %id)
	except:
		print(id+" not found")
		continue

	prof=np.loadtxt(profile)
	profile.close()
	#print(id, prof.shape[0])
	lenseq=prof.shape[0]
	prof=np.vstack((np.zeros(shape=(8,20)),prof,np.zeros(shape=(8,20))))


	featureseq=[]
	for i in range(lenseq):
		p=prof[i:i+17]
		features=p.flatten().tolist()
		featureseq.append(features)

	results=SVC00.predict(featureseq)
	seq=""
	for el in results:
		if el==1:
			seq+="H"
		elif el==2:
			seq+="E"
		else:
			seq+="C"

	predictionary[id]=seq

fileout=open("RESULTS_"+argv[3],"wb")
pickle.dump(predictionary,fileout)
fileout.close()

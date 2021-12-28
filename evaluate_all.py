from sys import argv 
import pickle
import numpy as np


#given all the cv metric results file as an input prodices an output file "FINAL_CV_RESULTS" which contains a dictionary with the mean of the metrics and the standard error (in binary format)
l=[]

for file in argv[1:]:
	x=open(file,"rb")
	l.append(pickle.load(x))
	x.close()

fd={}   # dictionary containing as a key the "metric" and as values a list with 2 elements : [mean of metrics values in all cv runs, standard error]
for met in l[0].keys():
	vals=[]
	for d in l:
		vals.append(d[met])
	fd[met]=[np.mean(vals),np.std(vals)/np.sqrt(5)]

print(fd)

fileout=open("FINAL_CV_RESULTS","wb")
pickle.dump(fd,fileout)
fileout.close()

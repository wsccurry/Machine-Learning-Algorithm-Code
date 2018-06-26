import matplotlib.pyplot as plt
import numpy as np
import kNN

datingDataMat,datingDataLabels=kNN.file2matrix('datingTestSet2.txt') 
fig=plt.figure()
ax=fig.add_subplot(111)
ax.scatter(datingDataMat[:,1],datingDataMat[:,2],15*np.array(datingDataLabels),15*np.array(datingDataLabels))
dataLabel1=[]
dataLabel2=[]
dataLabel3=[]
for i in datingDataLabels:
	if i==1:
		dataLabel1.append(i)
	elif i==2:
		dataLabel2.append(i)
	else:
		dataLabel3.append(i)
ax.scatter(datingDataMat[dataLabel1,1],datingDataMat[dataLabel1,2],15*np.array(dataLabel1),15*np.array(dataLabel1),label='didntLike')
ax.scatter(datingDataMat[dataLabel2,1],datingDataMat[dataLabel2,2],15*np.array(dataLabel2),15*np.array(dataLabel2),label='smallDoses')
ax.scatter(datingDataMat[dataLabel3,1],datingDataMat[dataLabel3,2],15*np.array(dataLabel3),15*np.array(dataLabel3),label='largeDoses')
ax.set_xlabel('Time spent of playing games')
ax.set_ylabel('Weekly consumption of ice cream')
ax.legend(loc='best')
plt.show()
import numpy as np 

def loadDataSet(fileName):
	dataMat=[]
	fr=open(fileName)
	for line in fr.readlines():
		curLine=line.strip().split('\t')
		fltLine=map(float,curLine)
		dataMat.append(fltLine)
	return dataMat

def distEclud(vecA,vecB):
	return np.sqrt(np.sum(np.power(vecA-vecB,2)))

def randCent(dataSet,k):
	n=dataSet.shape[1]
	centroids=np.zeros((k,n))
	for j in range(n):
		minJ=np.min(dataSet[:,j])
		rangeJ=float(np.max(dataSet[:,j])-minJ)
		centroids[:,j]=minJ+rangeJ*np.random.rand(1,k)	
	return centroids

def kMeans(dataSet,k,disMeans=distEclud,createCent=randCent):
	m=dataSet.shape[0]
	clusterAssment=np.zeros((m,2))
	centroids=createCent(dataSet,k)
	cluserChanges=True
	while cluserChanges:
		cluserChanges=False
		for i in range(m):
			minDist=float('inf');minIndex=-1
			for j in range(k):
				distJI=distEclud(centroids[j,:],dataSet[i,:])
				if distJI<minDist:
					minDist=distJI
					minIndex=j
			if clusterAssment[i,0]!=minIndex:
				cluserChanges=True
			clusterAssment[i,:]=minIndex,minDist**2
		print centroids
		for cent in range(k):
			ptsInclust=dataSet[clusterAssment[:,0]==cent]
			centroids[cent,:]=np.mean(ptsInclust,axis=0)
	return centroids,clusterAssment

def biKmeans(dataSet,k,distMeas=distEclud):
	m=dataSet.shape[0]
	clusterAssment=np.zeros((m,2))
	centroid=np.mean(dataSet,axis=0)
	centroidList=[centroid]
	for j in range(m):
		clusterAssment[j,1]=distMeas(centroid, dataSet[j,:])**2
	while len(centroidList)<k:
		lowestSSE=float('inf')
		for i in range(len(centroidList)):
			ptsIncurrCluster=dataSet[clusterAssment[:,0]==i]
			centroidMat,splitClustAss=kMeans(ptsIncurrCluster, 2)
			sseSplit=np.sum(splitClustAss[:,1])
			sseNotSplit=np.sum(clusterAssment[clusterAssment[:,0]!=i][:,1])
			print 'sseSplit,and notSplit',sseSplit,sseNotSplit
			if sseSplit+sseNotSplit<lowestSSE:
				bestCentToSplit=i
				bestNewCents=centroidMat
				bestClustAss=splitClustAss.copy()
				lowestSSE=sseSplit+sseNotSplit
		bestClustAss[bestClustAss[:,0]==1][:,0]=len(centroidList)
		bestClustAss[bestClustAss[:,0]==0][:,0]=bestCentToSplit
		print 'the bestCentToSplit is: ',bestCentToSplit
		print 'the len of bestClustAss is: ',len(bestClustAss)
		del centroidList[bestCentToSplit]
		centroidList.extend(bestNewCents.tolist())
		clusterAssment[clusterAssment[:,0]==bestCentToSplit]=bestClustAss
	return np.array(centroidList),clusterAssment

def distSLC(vecA,vecB):
	pi=np.pi
	a=np.sin(vecA[0,1]*pi/180)*np.sin(vecB[0,1]*pi/180)
	b=np.cos(vecA[0,1]*pi/180)*np.cos(vecB[0,1]*pi/180)*cos(pi*(vecB[0,0]-vecA[0,0])/180)
	return np.arccos(a+b)*6371.0

import matplotlib.pyplot as plt

def clusterClubs(numClust=5):
	datList=[]
	lines=open('places.txt').readlines()
	for line in lines:
		lineArr=line.split('\t')
		datList.append([float(lineArr[4]),float(lineArr[3])])
	datMat=np.array(datList)
	myCentroids,clustAssing=kMeans(datMat, numClust,disMeans=distSLC)
	fig=plt.figure()
	rect=[0.1,0.1,0.8,0.8]
	scatterMarker=['s','o','^','8','p','d','v','h','>','<']
	axprops=dict(xticks=[],yticks=[])
	ax0=fig.add_axes(rect,label='ax0',**axprops)
	imgP=plt.imread('Portland.png')
	ax0.imshow(imgP)
	ax1=fig.add_axes(rect,label='ax1',frameon=False)
	for i in range(numClust):
		ptsIncurrCluster=datMat[clustAssing[:,0]==i]
		markerStyle=scatterMarker[i%len(scatterMarker)]
		ax1.scatter(ptsIncurrCluster[:,0],ptsIncurrCluster[:,1],marker=markerStyle,s=90)
	ax1.scatter(myCentroids[:,0],myCentroids[:,1],marker='+',s=300)
	plt.show()





if __name__=='__main__':
	dataMat=loadDataSet('testSet2.txt')
	#kMeans(np.array(dataMat), 4)
	#print biKmeans(np.array(dataMat), 3)
	clusterClubs()
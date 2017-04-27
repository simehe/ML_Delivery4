#character detection
from imageReading import ImageReader
import modelTraining2
from copy import deepcopy
import string
import numpy as np
from PIL import Image
from imagePreProcessing import digitalImagePrep
import math

#modelTraining.classify(matrix of pixels)

ARRAY = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
reader = ImageReader("detection-images/")
imageName = "detection-2.jpg"
reader.readImageFromFileName(imageName)

patchSize = 20 #x20
#print reader.imageVector
numberToDetect = 50
maxPercentageWhite =0.3
stepSize = 2

#bruk classify som tar inn imageMatrix og returnerer et element i ARRAY

outputPic  = deepcopy(reader.imageMatrix)
clf,scaler = modelTraining2.train()

def slidingWindowDetection(clf,scaler,imageMatri,outputPic):
	imageMatrix = np.array(imageMatri)
	rows = len(imageMatrix)
	cols =  len(imageMatrix[0])
	count = 0
	pathcesToKeep = []
	worstAmongNumbersToCheck = 0
	for row in range(0,rows-patchSize,stepSize):
		for col in range(0,cols-patchSize,stepSize):
			#make imageVector
			imageVector = imageMatrix[row:row+patchSize,col:col+patchSize].reshape(1,400)[0]
			#imageVector = digitalImagePrep(imageVector, "fname",2).reshape(1,400)[0]*255
			unique, counts = np.unique(imageVector, return_counts=True)
			b = dict(zip(unique, counts))
			if 255 in b.keys() and b[255]> 20*20*maxPercentageWhite:
				continue
			a = clf.predict_proba([imageVector])[0][:-1]

			best = max(a)
			letterIndex = np.where(a==best)[0][0]
			pathcesToKeep.append([[row,col],best,ARRAY[letterIndex]])
			count += 1
			if count % 10 == 0:
				print count
	

	#find top numberToDetect best:
	pathcesToKeep.sort(key = lambda x : x[1])
	patchesKept = []
	count = 0
	print len(pathcesToKeep)
	while count != numberToDetect:
		try:
			new = pathcesToKeep[-1]
			coor,prob,letter = new
			row,col = coor[0],coor[1]
			pathcesToKeep = pathcesToKeep[:-1]
			notAllowed = False
			#check if patch is close to already added patch
			for coor2,p2,letter2 in patchesKept:
				r2,c2 = coor2[0],coor2[1]
				if abs(r2-row) < patchSize and abs(c2-col)  < patchSize:
					notAllowed = True
					break
			if notAllowed:
				None
			else:
				count+=1
				patchesKept.append(new)
		except:
			break
	for coor,prob,letter in patchesKept:
		row,col = coor[0],coor[1]
		for c in range(col,col+patchSize):
			outputPic[row][c]=0
			outputPic[row+patchSize][c]=0

		for r in range(row,row+patchSize):
			outputPic[r][col]=0
			outputPic[r][col+patchSize]=0



	return outputPic
	


def makePictureFromMatrix(imageMatrix):
	array = np.array(imageMatrix)
	result = Image.fromarray((array).astype(np.uint8))
	result.save('out.bmp')

output = slidingWindowDetection(clf,scaler,reader.imageMatrix,outputPic)
makePictureFromMatrix(outputPic)




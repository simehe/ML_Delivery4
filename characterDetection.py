#character detection
from imageReading import ImageReader
import modelTraining2
from copy import deepcopy
import string
import numpy as np
from PIL import Image
from imagePreProcessing import digitalImagePrep

#modelTraining.classify(matrix of pixels)

ARRAY = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
reader = ImageReader("detection-images/")
imageName = "detection-1.jpg"
reader.readImageFromFileName(imageName)

patchSize = 20 #x20
#print reader.imageVector
numberToDetect = 8

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
	for row in range(0,rows-patchSize,7):
		for col in range(0,cols-patchSize,7):
			#make imageVector
			imageVector = imageMatrix[row:row+patchSize,col:col+patchSize].reshape(1,400)[0]
			#imageVector = digitalImagePrep(imageVector, "fname",2).reshape(1,400)[0]*255
			
			if imageVector.max()==imageVector.min():
				continue
			scaler.transform([imageVector])
			a = clf.predict_proba([imageVector])[0][:-1]
			
			best = max(a)
			pathcesToKeep.append([[row,col],best])
			count += 1
			if count % 10 == 0:
				print count
	#find top numberToDetect best:

	pathcesToKeep.sort(key = lambda x : x[1])
	pathcesToKeep =  pathcesToKeep[-1-numberToDetect:-1]
	for coor,prob in pathcesToKeep:
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




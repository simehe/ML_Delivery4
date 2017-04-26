#character detection
from imageReading import ImageReader
import modelTraining
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
numberToDetect = 15

#bruk classify som tar inn imageMatrix og returnerer et element i ARRAY

outputPic  = deepcopy(reader.imageMatrix)
clf = modelTraining.train()

def slidingWindowDetection(clf,imageMatrix,outputPic):

	rows = len(imageMatrix)
	cols =  len(imageMatrix[0])
	count = 0
	pathcesToKeep = []
	worstAmongNumbersToCheck = 0
	for row in range(0,rows-patchSize,10):
		for col in range(0,cols-patchSize,10):
			#make imageVector
			imageVector = []
			for r in range(row,row+patchSize):
				for c in range(col,col+patchSize):
					imageVector.append(imageMatrix[r][c])
			imageVector =  np.array(imageVector).reshape(20,20)
			imageVector = digitalImagePrep(imageVector, "fname").reshape(1,400)[0]*255
			a = clf.predict_proba([imageVector])[0]
			best = max(a)
			pathcesToKeep.append([[row,col],best])
			count +=1
			if count %10 == 0:
				print count

	#find top numberToDetect best:

	pathcesToKeep.sort(key = lambda x : x[1])
	pathcesToKeep =  pathcesToKeep[-1-numberToDetect:-1]
	for coor,prob in pathcesToKeep:
		row,col = coor[0],coor[1]
		for r in range(row,row+patchSize):
			for c in range(col,col+patchSize):
				outputPic[r][c]=0



	return outputPic
	


def makePictureFromMatrix(imageMatrix):
	array = np.array(imageMatrix)
	result = Image.fromarray((array ).astype(np.uint8))
	result.save('out.bmp')

output = slidingWindowDetection(clf,reader.imageMatrix,outputPic)
makePictureFromMatrix(outputPic)




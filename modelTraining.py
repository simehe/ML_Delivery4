from sklearn.multiclass import OneVsRestClassifier
from sklearn.svm import SVC
from sklearn.svm import LinearSVC
from imageReading import ImageReader
import math
from sklearn.preprocessing import LabelBinarizer



array = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
y = []
X = []
reader = ImageReader("/Users/simenhellem/Documents/chars74k-lite/")
count = 0

testSetRemember = []
testSetAll = []


for i in range(0,10):
    input = array[i] + "/"
    reader.readImage(input)
    print(len(reader.imageVector))
    numberTest = int(math.floor(len(reader.imageVector) * 0.2))
    for j in range(len(reader.imageVector)):
        if(j < len(reader.imageVector) - numberTest):
            y.append(i)
            X.append(reader.imageVector[j])
        else:
            testSetAll.append(reader.imageVector[j])
            testSetRemember.append(i)
    reader.clearVector()


#classif = OneVsRestClassifier(estimator=SVC(random_state=0))
classif = OneVsRestClassifier(LinearSVC(C=100.)).fit(X, y)
print("built model")
#classif.fit(X, y).predict(X)
print("going for prediction")
results = classif.predict(testSetAll)
missedCount = 0
length = len(results)
for i in range(len(results)):
    print(results[i])

for i in range(len(results)):
    if results[i] != testSetRemember[i]:
        print("You thought it was", results[i])
        print("But it was:", testSetRemember[i])
        missedCount += 1
total = float(missedCount)/float(length)
print("you missed: ", total)

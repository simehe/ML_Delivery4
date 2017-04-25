from imageReading import ImageReader
import math

### ONE VS REST ###
from sklearn.multiclass import OneVsRestClassifier
from sklearn.svm import SVC
from sklearn.svm import LinearSVC

### FOREST ###
from sklearn.ensemble import RandomForestClassifier
from sklearn import tree

## NAIVE BAYES ##
from sklearn.naive_bayes import GaussianNB


## CONSTANTS ##
ARRAY = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
TESTSET = 0.2
y = []
X = []
reader = ImageReader("mlImageHolder/")


## FOR TESTING ###
testSetRemember = []
testSetAll = []

def prepareTrainandTestSet():
    for i in range(len(ARRAY)):
        input = ARRAY[i] + "/"
        reader.readImage(input)
        print(len(reader.imageVector))
        numberTest = int(math.floor(len(reader.imageVector) * TESTSET))
        for j in range(len(reader.imageVector)):
            if(j < len(reader.imageVector) - numberTest):
                y.append(i)
                X.append(reader.imageVector[j])
            else:
                testSetAll.append(reader.imageVector[j])
                testSetRemember.append(i)
        reader.clearVector()


def classify():
    results = clf.predict(testSetAll)
    missedCount = 0
    for i in range(len(results)):
        if results[i] != testSetRemember[i]:
            print("You thought it was", results[i])
            print("But it was:", testSetRemember[i])
            missedCount += 1
    total = float(missedCount) / float(len(results))
    print("you missed: ", total)


prepareTrainandTestSet()

### DIFFERENT CLASSIFIERS ###
#clf = OneVsRestClassifier(estimator=SVC(random_state=0))
#clf = OneVsRestClassifier(LinearSVC(C=100.)).fit(X, y)
clf = RandomForestClassifier(n_estimators=40)
#clf = GaussianNB()
#clf = tree.DecisionTreeClassifier()

### FIT TO TRAINING DATA ###
clf.fit(X, y)

print("built model")
print("going for prediction")

### TEST ON TEST SET ###
classify()









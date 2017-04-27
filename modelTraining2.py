from imageReading import ImageReader
import math
from sklearn import preprocessing

### ONE VS REST ###
from sklearn.multiclass import OneVsRestClassifier
from sklearn.svm import SVC
from sklearn.svm import LinearSVC
from sklearn.neural_network import MLPClassifier

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
scaler = 0


## FOR TESTING ###
testSetRemember = []
testSetAll = []

def prepareTrainandTestSet():
    global X
    global testSetAll
    global scaler
    for i in range(len(ARRAY)):
        input = ARRAY[i] + "/"
        inputTest = ARRAY[i] + "/test/"
        reader.readImage(input)
        print("For the letter: ", ARRAY[i], "You train on: ", len(reader.imageVector))
        indexRemember = 0
        for j in range(len(reader.imageVector)):
            indexRemember = j
            y.append(i)
            X.append(reader.imageVector[j])
        reader.clearVector()
        reader.count = indexRemember + 1
        reader.readImage(inputTest)
        for j in range(len(reader.imageVector)):
            testSetAll.append(reader.imageVector[j])
            testSetRemember.append(i)
        reader.clearVector()
        reader.count = 0
    for i in range(300):
        whiteImage = []
        for i in range(400):
            whiteImage.append(255)
        X.append(whiteImage)
        y.append(26)
    scaler = preprocessing.StandardScaler().fit(X)
    scaler.transform(X)
    scaler.transform(testSetAll)


def classify(clf):
    results = clf.predict(testSetAll)
    missedCount = 0
    print("Classified in total: ", len(results))
    for i in range(len(results)):
        if results[i] != testSetRemember[i]:
            missedCount += 1
    total = 1 - (float(missedCount) / float(len(results)))
    print("Overall achievement was: ", total)



def train():
    print "building model"

    prepareTrainandTestSet()

    ### DIFFERENT CLASSIFIERS ###
    #clf = OneVsRestClassifier(estimator=SVC(random_state=0))
    #clf = OneVsRestClassifier(LinearSVC(C=100.))
    clf = RandomForestClassifier(n_estimators=200)
    #clf = GaussianNB()
    #clf = tree.DecisionTreeClassifier()

    ### FIT TO TRAINING DATA ###
    clf.fit(X, y)

    print "model finished"
    return clf,scaler

def test(clf):
    print("going for prediction")

    ### TEST ON TEST SET ###
    classify(clf)

#train()









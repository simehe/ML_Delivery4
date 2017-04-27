from imageReading import ImageReader
import math
from sklearn import preprocessing
from sklearn.externals import joblib

### NN ###
from sklearn.neural_network import MLPClassifier

### FOREST ###
from sklearn.ensemble import RandomForestClassifier

## CONSTANTS ##
ARRAY = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v",
         "w", "x", "y", "z"]
y = []
X = []
reader = ImageReader("mlImageHolder/")
clf = 0
scaler = 0

## FOR TESTING ##
testSetRemember = []
testSetAll = []

## MODE ##
MODE = 1  # Mode = 1 -> Random Forest. Mode = 2 -> Neural Network


### PREPARES THE DIFFERENT SETS FROM IMAGE ###
def prepareTrainandTestSet():
    global X
    global testSetAll
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
        for j in range(400):
            whiteImage.append(255)
        X.append(whiteImage)
        y.append(26)
    scaler = preprocessing.StandardScaler().fit(X)
    scaler.transform(X)
    scaler.transform(testSetAll)


def classify():
    results = clf.predict(testSetAll)
    missedCount = 0
    print("Classified in total: ", len(results))
    for i in range(len(results)):
        if results[i] != testSetRemember[i]:
            missedCount += 1
    total = 1 - (float(missedCount) / float(len(results)))
    print("Overall achievement was: ", total)


def train():
    global clf
    prepareTrainandTestSet()

    ### DIFFERENT CLASSIFIERS ###
    if (MODE == 1):
        clf = RandomForestClassifier(n_estimators=200)
    else:
        clf = MLPClassifier(solver='adam', alpha=1e-05, hidden_layer_sizes=(300, 300, 300))

    ### FIT TO TRAINING DATA ###
    clf.fit(X, y)

    print("The model is built")


def test():
    ### TEST ON TEST SET ###
    classify()

def save():
    # Can be accessed through clf = joblib.load('finishedModel.pkl')
    joblib.dump(clf, 'finishedModel.pkl')

train()
test()
save()












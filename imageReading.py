from PIL import Image

### After reading, all images can be feetched from the imageVector ###

class ImageReader:

    def __init__(self, imageFolder):
        self.imageFolder = imageFolder
        self.sizeX = 20
        self.sizeY = 20
        self.imageVector = []

    def readImage(self, letter):
        source = self.imageFolder + letter
        nextImage = True
        count = 0
        while(nextImage):
            try:
                lett = letter[0] + "_" + str(count) + ".jpg"
                newSource = source
                newSource += lett
                im = Image.open(newSource)
                pix = im.load()
                imageList = []
                for i in range(self.sizeX):
                    for j in range(self.sizeY):
                        imageList.append(pix[i, j])
                self.imageVector.append(imageList)

            except IOError:
                nextImage = False


            count += 1

    def getImageVector(self):
        return self.imageVector
    def clearVector(self):
        self.imageVector = []


reader = ImageReader("/Users/simenhellem/Documents/chars74k-lite/")
reader.readImage("c/")






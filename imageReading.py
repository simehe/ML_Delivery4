from PIL import Image
import skimage
from skimage import io

### After reading, all images can be feetched from the imageVector ###

class ImageReader:

    # NEEDS TO BE INITATED WITH THE ACCEPTABLE FOLDER
    def __init__(self, imageFolder):
        self.imageFolder = imageFolder
        self.sizeX = 20
        self.sizeY = 20
        self.count = 0
        self.imageVector = []
        self.imageHolder = []

    ### INPUT -> BASIS ADRESS FOR EACH IMAGE
    def readImage(self, letter):
        source = self.imageFolder + letter
        nextImage = True
        count = self.count
        while(nextImage):
            try:
                lett = letter[0] + "_" + str(count) + ".jpg"
                newSource = source
                newSource += lett
                image = io.imread(newSource)
                self.imageHolder.append(image)
                imageList = []
                for i in range(self.sizeX):
                    for j in range(self.sizeY):
                        imageList.append(image[i, j])
                self.imageVector.append(imageList)

            except IOError:
                nextImage = False


            count += 1

    def clearVector(self):
        self.imageVector = []
        self.imageHolder = []


reader = ImageReader("chars74k-lite/")
reader.readImage("c/")







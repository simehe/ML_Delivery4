from PIL import Image
import skimage
from skimage import io

### After reading, all images can be feetched from the imageVector ###

class ImageReader:

    def __init__(self, imageFolder):
        self.imageFolder = imageFolder
        self.sizeX = 20
        self.sizeY = 20
        self.imageVector = []
        self.imageHolder = []
        self.imageMatrix = []

    def readImage(self, letter):
        source = self.imageFolder + letter
        nextImage = True
        count = 0
        while(nextImage):
            try:
                lett = letter[0] + "_" + str(count) + ".jpg"
                newSource = source
                newSource += lett
                image = io.imread(newSource)
                #im = Image.open(newSource)
                self.imageHolder.append(image)
                #pix = im.load()
                imageList = []
                for i in range(self.sizeX):
                    for j in range(self.sizeY):
                        imageList.append(image[i, j])
                self.imageVector.append(imageList)

            except IOError:
                nextImage = False


            count += 1

    def readImageFromFileName(self, fileName):
        source = self.imageFolder
        try:
            imagePath = source + fileName
            im = Image.open(imagePath)
            pix = im.load()
            width, height = im.size
            self.sizeX = width
            self.sizeY = height
            imageMatrix = []
            for i in range(height):
                imageRow = []
                for j in range(width):
                    imageRow.append(pix[j, i])
                imageMatrix.append(imageRow)
            self.imageMatrix = imageMatrix
        except IOError:
            nextImage = False


    def clearVector(self):
        self.imageVector = []
        self.imageHolder = []










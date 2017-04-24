import os, sys
from PIL import Image

im = Image.open("/Users/simenhellem/Documents/chars74k-lite/a/a_0.jpg")
x = 3
y = 4

print(im.format, im.size, im.mode)
im.show()
pix = im.load()

imageList = []
for i in range(20):
    for j in range(20):
        imageList.append(pix[i, j])

print(imageList)


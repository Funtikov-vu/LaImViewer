from PIL import Image
from PySide6 import QtCore

Image.MAX_IMAGE_PIXELS = None

import os
import shutil

class ImageReader():
    def __init__(self):
        self.filename = None
        self.dir = None
        self.tileWidth = 150
        self.tileHeight = 150
        self.levelCount = 0

    def getTileSize(self):
        return (self.tileWidth, self.tileHeight)

    def saveImage(self, img):
        w,h = img.size

        xw = 0
        yh = 0

        w1, h1 = w, h
        level = 1
        os.mkdir(os.path.join(self.dir, str(level)))
        while(w1 >= 100 and h1 >= 100 and level <= 10):
            w1 /= 2
            h1 /= 2
            level += 1
            os.mkdir(os.path.join(self.dir, str(level)))

        self.levelCount = level - 1

        while xw < w:
            yh = 0
            xw2 = xw + self.tileWidth if xw + self.tileWidth <= w else w 
            while yh < self.tileHeight:
                yh2 = yh + self.tileHeight if yh + self.tileHeight <= h else h 
                cropped_img = img.crop((xw, yh, xw2, yh2))
                level = 1
                name = str(xw)+"_"+str(yh)+"_"+str(xw2)+"_"+str(yh2)+".png"
                cropName = os.path.join(self.dir, str(level), name)
                cropped_img.save(cropName)
                width, height = cropped_img.size
                while level <= self.levelCount:
                    low_res_img = cropped_img.resize((width // pow(2, level),height //  pow(2, level)))
                    low_res_img.save(os.path.join(self.dir, str(level+1), name), "PNG")
                    level += 1
                yh += self.tileWidth
            xw += self.tileWidth

    def load(self, filename):
        self.filename = filename
        img = Image.open(filename)

        w,h = img.size

        self.dir = os.path.join(os.path.split(filename)[0], "TMP_LaImViewer")

        if os.path.exists(self.dir):
            dir1 = QtCore.QDir(self.dir)
            dir1.removeRecursively()
            os.mkdir(self.dir)
        else:
            os.mkdir(self.dir)
        
        self.saveImage(img)

if __name__ == '__main__':
    import sys

    reader = ImageReader()

    #reader.load("C:\\Users\\Dmitry\\Downloads\\MAES15_Biodiversity_Marine_WGS84_Final\\MAES15_Biodiversity_Marine_WGS84_Final.png")
   # reader.load("C:\\Users\\Dmitry\\Downloads\\MAES15_Biodiversity_Marine_WGS84_Final\\0.tif")
    reader.load("C:\\Users\\Dmitry\\Downloads\\123LaIm\\1.png")
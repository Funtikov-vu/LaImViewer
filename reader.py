from ctypes.wintypes import RGB
from cv2 import resize
import numpy as np
import cv2

class ImageReader():
    def __init__(self):
        self.filename = None
        self.img = None
        self.levels = []

    def load(self, filename):
        self.filename = filename
        self.img = cv2.imread(filename, cv2.IMREAD_COLOR)


        h, w, c = self.img.shape
        # RGB_img = cv2.cvtColor(self.img, cv2.COLOR_RGB2BGR)
        # self.img = RGB_img

        temp = cv2.resize(self.img, (w, h), interpolation=cv2.INTER_LINEAR)
        self.img = temp
        w /= 2
        h /= 2

        cv2.imwrite("C:\\Users\\Dmitry\\Downloads\\MAES15_Biodiversity_Marine_WGS84_Final\\"+str(0)+".tif", self.img)

        

        

        level = 1
        while(w >= 2 and h >= 2 and level <= 10):
            resized = cv2.resize(self.img, (int(w),int(h)), interpolation = cv2.INTER_CUBIC)
            self.levels.append(resized)
            cv2.imwrite("C:\\Users\\Dmitry\\Downloads\\MAES15_Biodiversity_Marine_WGS84_Final\\"+str(level)+".tif", resized)
            w /= 2
            h /= 2
            level += 1

if __name__ == '__main__':
    import sys

    reader = ImageReader()

    reader.load("C:\\Users\\Dmitry\\Downloads\\MAES15_Biodiversity_Marine_WGS84_Final\\MAES15_Biodiversity_Marine_WGS84_Final.tif")
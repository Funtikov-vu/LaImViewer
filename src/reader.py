import os
from math import log2
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtCore import QRect
from src.converter import META_FILENAME


class ImageReader():
    def __init__(self, temp_dir):
        self.image = None
        self.tile_dir = temp_dir
        self.load()
        

    def load(self):
        meta_path = os.path.join(self.tile_dir, META_FILENAME)
        file = open(meta_path, 'r')
        lines = file.readlines()
        
        for line in lines:
            if "height" in line:
                self.height = int(line.split(":")[1])
            elif "width" in line:
                self.width = int(line.split(":")[1])
            elif "tile_size" in line:
                self.tile_size = int(line.split(":")[1])
            elif "ext" in line:
                self.ext = line.split(":")[1].rstrip('\n')
            elif "lvl_nums" in line:
                self.levels = int(line.split(":")[1])
                
                
    def read(self, xtop, ytop, xbottom, ybottom, f):
        level = int(log2(1.0 / f))

        if (level < 0):
            level = 0

        if (level > self.levels - 1):
            level = self.levels - 1
            
        filename = os.path.join(self.tile_dir, str(level), f"{xtop}_{ytop}_{xbottom}_{ybottom}.{self.ext}")
        return QImage(filename)

    def widthImage(self):
        return self.width

    def heightImage(self):
        return self.height

    def rect(self):
        return QRect(0, 0, self.width, self.height)
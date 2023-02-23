import os
from math import log2
from PySide6.QtGui import QImage, QPixmap, QPainter, qRgb
from PySide6.QtCore import QRect, QPoint
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
    
    def getTiles(self, rect : QRect, factor : float, shift : QPoint):
        level = int(log2(1.0 / factor))

        if (level < 0):
            level = 0
        
        rect.translate(QPoint(-shift.x(),-shift.y()))

        if (level > self.levels - 1):
            level = self.levels - 1
            
        tileW = self.tile_size
        tileH = self.tile_size
        w = self.width
        h = self.height
        
        wtop = int((rect.x()//tileW)*tileW)
        htop = int((rect.y()//tileH)*tileH)
        
        wbot = int(((rect.x() + rect.width())//tileW + 1)*tileW)
        hbot = int(((rect.y() + rect.height())//tileH + 1)*tileH)
        
        if wtop < 0:
            wtop = 0
            
        if htop < 0:
            htop = 0
        
        if wtop > self.width:
            wtop = self.width
        
        if htop > self.height:
            htop = self.height
        
        if wbot > self.width:
            wbot = self.width
        
        if hbot > self.height:
            hbot = self.height
            
        if wbot < 0:
            wbot = 0
            
        if hbot < 0:
            hbot = 0
            
        fullImage = None
        painter = None
        
        x = wtop
        y = htop
        
        prevW = 0
        prevH = 0
        
        img = QImage()
        
        while x < wbot:
            y = htop
            xbot = x + tileW if x + tileW < self.widthImage() else self.widthImage()
            while y < hbot:
                ybot =  y + tileH if y + tileH < self.heightImage() else self.heightImage()
                filename = os.path.join(self.tile_dir, str(level), f"{x}_{y}_{xbot}_{ybot}.{self.ext}")
                img = QImage(filename)
                
                if img.isNull():
                    print("nul")
                    continue
                
                if fullImage is None:
                    fullImage = QImage((wbot-wtop)//(2**level), (hbot - htop)//(2**level), img.format())
                    fullImage.fill(qRgb(255, 255, 255))
                    painter = QPainter(fullImage)
                    #painter.begin()
                
                if img.isNull() == False:
                    painter.drawImage(QPoint(prevW,prevH), img)
                else:
                    print("NULLLLL")
                
                prevH += img.height()
                
                y += tileH
            x += tileW
            prevW += img.width()
            prevH = 0
        
        #if painter is not None:
            #painter.end()
        
        if not fullImage.isNull():
            painter.end()
            localW = rect.x()
            if localW < 0:
                localW = 0
            if localW > self.width:
                localW = self.width
            
            localH = rect.y()
            if localH < 0:
                localH = 0
            if localH > self.height:
                localH = self.height
            
            localWbot = rect.x() + rect.width()
            if localWbot < 0:
                localWbot = 0
            if localWbot > self.width:
                localWbot = self.width
                
            localHbot = rect.y() + rect.height()
            if localHbot < 0:
                localHbot = 0
            if localHbot > self.height:
                localHbot = self.height
            
            localrect = QRect(localW, localH, localWbot - localW, localHbot - localH)
            levRect = QRect(localrect.x()//(2**level)-wtop//(2**level), localrect.y()//(2**level)-htop//(2**level), localrect.width()//(2**level), localrect.height()//(2**level))
            return fullImage.copy(levRect), localrect
            #return fullImage.copy(localrect), localrect
            
        #return fullImage, QRect(wtop, htop, wbot-wtop, hbot-htop)
        return None, None           
                
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
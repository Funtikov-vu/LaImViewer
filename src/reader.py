from math import log2
from PySide6.QtGui import QImage, QPixmap


class ImageReader():
    def __init__(self):
        self.image = None
        self.levels = []

    def load(self, filename):
        self.image = QImage(filename)

        if (self.image.isNull()):
            return False

        w = self.image.width()
        h = self.image.height()

        w /= 2
        h /= 2

        level = 1
        while (w >= 2 and h >= 2 and level <= 10):
            self.levels.append(self.image.copy().scaled(w, h))
            w /= 2
            h /= 2
            level += 1

        return not self.image.isNull()

    def read(self, xtop, ytop, xbottom, ybottom, f):
        level = int(log2(1.0 / f)) + 1

        if (level < 1):
            level = 1

        if (level > len(self.levels) + 1):
            level = len(self.levels) + 1

        factor = int(pow(2, level - 1))
        xtop //= factor
        ytop //= factor
        xbottom //= factor
        ybottom //= factor

        # print("level = ", level)

        if (level == 1):
            w = self.image.width()
            h = self.image.height()
            if (xtop < 0):
                xtop = 0
            if (xbottom > w):
                xbottom = w
            if (ytop < 0):
                ytop = 0
            if (ybottom > h):
                ybottom = h
            return self.image.copy(xtop, ytop, xbottom - xtop, ybottom - ytop)
        else:
            # print("w = ", self.levels[level - 2].width())
            # print("h = ", self.levels[level - 2].height())
            # print("xbot = ", xbottom)
            # print("ybot = ", ybottom)
            w = self.levels[level - 2].width()
            h = self.levels[level - 2].height()
            if (xtop < 0):
                xtop = 0
            if (xbottom > w):
                xbottom = w
            if (ytop < 0):
                ytop = 0
            if (ybottom > h):
                ybottom = h
            return self.levels[level - 2].copy(xtop, ytop, xbottom - xtop, ybottom - ytop)

    def width(self):
        return self.image.width()

    def height(self):
        return self.image.height()

    def rect(self):
        return self.image.rect()
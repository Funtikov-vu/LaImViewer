from math import log2
import os.path

from PySide6.QtCore import Qt, QPointF, QPoint, QRect
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtWidgets import QGraphicsView, QGraphicsScene, QFileDialog, QApplication, QGraphicsPixmapItem, QMessageBox

from src.converter import Converter
from src.reader import ImageReader


class PixmapItem(QGraphicsPixmapItem):
    def __init_(self):
        QGraphicsPixmapItem.__init__(self)
    
    def setSceneRect(self, rect):
        self.rect = rect

    def boundingRect(self):
        return self.rect

    def paint(self, painter, options, widget):
        painter.drawImage(self.rect, self.pixmap().toImage(), self.pixmap().toImage().rect())



class LaImViewer(QGraphicsView):
    def __init__(self, meta):
        QGraphicsView.__init__(self)

        self.setMouseTracking(True)

        self.scene = QGraphicsScene()

        self.reader = ImageReader(meta['tile_dir'], meta['ext'])

        self.setScene(self.scene)

        self.startPos = None
        self.mousePos = None

        self.zoom = 1.0
        self.xTrans = 0.0
        self.yTrans = 0.0

        self.maxXTrans = 0.0
        self.maxYTrans = 0.0

        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)

        self.setTransformationAnchor(QGraphicsView.AnchorViewCenter)

        self.verticalScrollBar().valueChanged.connect(self.scrollValueChange)
        self.horizontalScrollBar().valueChanged.connect(self.scrollValueChange)

    def loadImage(self, fileName=""):
        fileName, dummy = QFileDialog.getOpenFileName(self, "Open image")
        if len(fileName) and os.path.isfile(fileName):
            if(self.reader.load(fileName) is False):
                QMessageBox.warning(self, "Error", "Can not open image")
                self.loadImage()
            rect = self.reader.rect()
            self.setSceneRect(rect)
            self.fitInView(rect, Qt.KeepAspectRatio)
            self.maxXTrans = self.reader.width()/2
            self.maxYTrans = self.reader.height()/2
            self.draw()

    def scrollValueChange(self):
        self.draw()

    def draw(self):
        factor =  max(self.zoom*self.width()/self.reader.width(), self.zoom*self.height()/self.reader.height())

        self.scene.clear()

        tileWidth = 500
        tileHeight = 500
        x = 0
        y = 0

        newPose = QPointF(self.xTrans, self.yTrans)
        #print("================================")
        mapRect = self.mapToScene(self.viewport().geometry()).boundingRect()
        while(x < self.reader.width()):
            y = 0
            xbot = x + tileWidth if x + tileWidth < self.reader.width() else self.reader.width()
            while(y < self.reader.height()):
                ybot = y + tileHeight if y + tileHeight < self.reader.height() else self.reader.height()
                tileRect = QRect(0,0,xbot-x+1,ybot-y+1)
                tileRect.translate(QPoint(newPose.x(), newPose.y()) + QPoint(x,y))
                if(mapRect.intersected(tileRect).isNull()):
                    #print("Not visible", x, y, sep = " ")
                    y += tileHeight
                    continue
                #print(x,y,xbot,ybot,xbot-x,ybot-y,sep = "; ")
                image = self.reader.read(x, y, xbot, ybot, factor)
                pixItem = PixmapItem()
                pixmap = QPixmap.fromImage(image)
                pixItem.setPixmap(pixmap)
                pixItem.setSceneRect(QRect(0,0,xbot-x+1,ybot-y+1))
                pixItem.setPos(QPointF(x,y))
                self.scene.addItem(pixItem)
                y += tileHeight

            x += tileWidth
        #print("================================")
        for i in range(len(self.scene.items())):
             self.scene.items()[i].setPos(self.scene.items()[i].pos() + newPose)

    def wheelEvent(self, event):
        if event.angleDelta().y() > 0:
            factor = 1.1
        else:
            factor = 0.9

        if(self.zoom*factor < 1):
            factor = 1.0
        else:
            self.zoom *= factor

        modifiers = QApplication.keyboardModifiers()
        if modifiers == Qt.ControlModifier:
            targetViewportPos = self.mousePos
            targetScenePos = self.mapToScene(self.mousePos)

            self.scale(factor, factor)
            self.centerOn(targetScenePos)

            deltaViewportPos = targetViewportPos - QPoint(self.viewport().width() / 2.0, self.viewport().height() / 2.0)
            viewportCenter = self.mapFromScene(targetScenePos) - deltaViewportPos

            self.centerOn(self.mapToScene(viewportCenter))
            #print("mouse center")
        else:
            targetPos = self.mapToScene(self.viewport().rect().center())
            self.scale(factor, factor)
            self.centerOn(targetPos)
            #print("view center")

        self.draw()

    def resizeEvent(self, event):
        QGraphicsView.resizeEvent(self, event)
        self.draw()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.startPos = event.pos()
        #print(self.mapToScene(self.viewport().geometry()).boundingRect().intersects(self.items()[0].sceneBoundingRect()))
        self.draw()

    def mouseDoubleClickEvent(self, event):
        if event.button() == Qt.RightButton:
            self.fitInView(self.reader.rect(), Qt.KeepAspectRatio)
            self.xTrans = 0
            self.yTrans = 0
            self.zoom = 1.0

    def mouseMoveEvent(self, event):
        #print("move")
        self.mousePos = event.pos()
        if self.startPos is not None:
            delta = self.startPos - event.pos()

            transform = self.transform()

            deltaX = delta.x() / transform.m11()
            deltaY = delta.y() / transform.m22()

            if(abs(self.xTrans - self.zoom*deltaX) > self.maxXTrans):
                deltaX = 0

            if(abs(self.yTrans - self.zoom*deltaY) > self.maxYTrans):
                deltaY = 0

            self.xTrans -= deltaX
            self.yTrans -= deltaY

            self.startPos = event.pos()
        self.draw()

    def mouseReleaseEvent(self, event):
        self.startPos = None
        self.draw()

if __name__ == '__main__':
    import sys

    params = {
        'image_path': r"C:\Users\buriv\PycharmProjects\LaIm\ex1.jpeg",
        'tile_dir': r"C:\Users\buriv\PycharmProjects\LaIm\tiles",
        'tile_size': 2000,
        'lvl_nums': 5,
        'ext': 'png'
    }
    conv = Converter(**params)
    conv.make_tiles()
    meta = conv.generate_meta()

    app = QApplication(sys.argv)

    viewer = LaImViewer(meta)
    viewer.loadImage()
    viewer.setWindowTitle("LaImViewer")

    viewer.show()
    sys.exit(app.exec_())
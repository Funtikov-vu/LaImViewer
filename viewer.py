from math import log2

from PySide6.QtCore import Qt, QPointF, QPoint, QRect, QTimer
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
    def __init__(self):
        QGraphicsView.__init__(self)
        
        self.wasLoaded = False

        self.setMouseTracking(True)

        self.scene = QGraphicsScene()

        self.setScene(self.scene)

        self.startPos = None
        self.mousePos = None

        self.zoom = 1.0
        self.xTrans = 0.0
        self.yTrans = 0.0
        self.skipZoom = False

        self.maxXTrans = 0.0
        self.maxYTrans = 0.0

        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)

        self.setTransformationAnchor(QGraphicsView.AnchorViewCenter)

        self.verticalScrollBar().valueChanged.connect(self.scrollValueChange)
        self.horizontalScrollBar().valueChanged.connect(self.scrollValueChange)

    def loadImage(self):
        self.dir = QFileDialog.getExistingDirectory() 
        self.reader = ImageReader(self.dir)
        self.wasLoaded = True
        rect = self.reader.rect()
        self.setSceneRect(rect)
        self.fitInView(rect, Qt.KeepAspectRatio)
        self.maxXTrans = self.reader.widthImage()/2
        self.maxYTrans = self.reader.heightImage()/2
        self.scene.addItem(PixmapItem())
        self.draw()

    def scrollValueChange(self):
        self.draw()

    def draw(self):
        if not self.wasLoaded or len(self.scene.items()) == 0 :
            return
        
        factor =  max(self.zoom*self.width()/self.reader.widthImage(), self.zoom*self.height()/self.reader.heightImage())

        newPose = QPoint(self.xTrans, self.yTrans)

        mapRect = self.mapToScene(self.viewport().geometry()).boundingRect()
        
        img, rect = self.reader.getTiles(mapRect, factor, newPose)
        
        if img is not None:
            pixmap = QPixmap.fromImage(img)
            self.items()[0].setPixmap(pixmap)
            self.items()[0].setSceneRect(QRect(0,0,rect.width(),rect.height()))
            self.items()[0].setPos(QPoint(rect.x(), rect.y()) + newPose)
            
    def wheelEvent(self, event):
        if self.skipZoom:
            return
        
        self.timer = QTimer()
        self.timer.timeout.connect(self.stopSkipZoom)
        self.skipZoom = True
        self.timer.start(200)
        
        angle = event.angleDelta().y()
        
        for i in range(1):
            factor = pow(1.002, angle)

            if(self.zoom*factor < 1):
                factor = 1.0
                continue
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
            #QTimer.singleShot(500, i)
            
        
        
    def stopSkipZoom(self):
        self.skipZoom = False

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

    app = QApplication(sys.argv)

    viewer = LaImViewer()
    viewer.loadImage()
    viewer.setWindowTitle("LaImViewer")

    viewer.show()
    sys.exit(app.exec())
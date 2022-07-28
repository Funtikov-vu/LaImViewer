import os.path

from PySide6.QtCore import Qt, QRectF, QPointF
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtWidgets import QGraphicsView, QGraphicsScene, QFileDialog, QApplication


class LaImViewer(QGraphicsView):

    def __init__(self):
        QGraphicsView.__init__(self)

        self.scene = QGraphicsScene()

        self.setScene(self.scene)

        self.pixmap = None

        self.startPos = None

        self.zoom = 1.0
        self.xTrans = 0.0
        self.yTrans = 0.0

        self.maxXTrans = 0.0
        self.maxYTrans = 0.0

        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)

        self.setTransformationAnchor(QGraphicsView.AnchorViewCenter)

    def loadImage(self, fileName=""):
        fileName, dummy = QFileDialog.getOpenFileName(self, "Open image")
        if len(fileName) and os.path.isfile(fileName):
            image = QImage(fileName)
            self.maxXTrans = image.width()/2
            self.maxYTrans = image.height()/2
            pixmap = QPixmap.fromImage(image)
            self.pixmap = self.scene.addPixmap(pixmap)
            self.setSceneRect(QRectF(pixmap.rect()))
            self.fitInView(QRectF(pixmap.rect()), Qt.KeepAspectRatio)
    
    def wheelEvent(self, event):
        center = self.mapToScene(self.viewport().rect().center())
        self.centerOn(center)
        if event.angleDelta().y() > 0:
            factor = 1.25
        else:
            factor = 0.8
        self.zoom *= factor
        self.scale(factor, factor)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.startPos = event.pos()
        if event.button() == Qt.RightButton:
            self.fitInView(QRectF(self.pixmap.pixmap().rect()), Qt.KeepAspectRatio)
            item = self.items()[0]
            newPose = item.pos() - QPointF(self.xTrans, self.yTrans)
            item.setPos(newPose)
            self.xTrans = 0
            self.yTrans = 0
            self.zoom = 1.0
        #print(self.mapToScene(self.viewport().geometry()).boundingRect().intersects(self.items()[0].sceneBoundingRect()))
        QGraphicsView.mouseDoubleClickEvent(self, event)

    def mouseMoveEvent(self, event):
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

            item = self.items()[0]
            newPose = item.pos() - QPointF(deltaX, deltaY)
            item.setPos(newPose)
            #print("newPos = ", newPose)
            self.startPos = event.pos()
        QGraphicsView.mouseDoubleClickEvent(self, event)

    def mouseReleaseEvent(self, event):
        self.startPos = None
        QGraphicsView.mouseDoubleClickEvent(self, event)

if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)

    viewer = LaImViewer()
    viewer.loadImage()
    viewer.setWindowTitle("LaImViewer")

    viewer.show()
    sys.exit(app.exec_())
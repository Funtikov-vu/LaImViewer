import sys, os
import shutil
from PySide6.QtWidgets import (QLineEdit, QPushButton, QApplication,
     QDialog, QToolButton, QLabel, QFileDialog, QSpinBox, QGridLayout,QMessageBox,QProgressDialog)

from PySide6.QtCore import QDir, Qt 
from converter import Converter

class ConverterDialog(QDialog):

    def __init__(self, parent=None):
        super(ConverterDialog, self).__init__(parent)
        self.setWindowTitle("Converter")
        
        self.imgNameLable = QLabel("Select image path")
        self.imgNameLine = QLineEdit("Path")
        self.imgButton = QToolButton()
        self.imgButton.setText("...")
        self.imgButton.clicked.connect(self.chooseImage)
                
        self.imgDirLable = QLabel("Select LaIm image dir")
        self.imgDirLine = QLineEdit("Dir")
        self.dirButton = QToolButton()
        self.dirButton.setText("...")
        self.dirButton.clicked.connect(self.chooseDir)
        
        self.levelLabel = QLabel("Level count")
        self.levelSpin = QSpinBox()
        self.levelSpin.setRange(1,10000000)
        self.levelSpin.setValue(6)
        
        self.tileLabel = QLabel("Tile size")
        self.tileSpin = QSpinBox()
        self.tileSpin.setRange(1,100000000)
        self.tileSpin.setValue(10000)

        self.convertButton = QPushButton("Convert")
        self.convertButton.clicked.connect(self.convert)
        
        layout = QGridLayout()
        layout.addWidget(self.imgNameLable,0,0)
        layout.addWidget(self.imgNameLine,0,1)
        layout.addWidget(self.imgButton,0,2)
        
        layout.addWidget(self.imgDirLable,1,0)
        layout.addWidget(self.imgDirLine,1,1)
        layout.addWidget(self.dirButton,1,2)
        
        layout.addWidget(self.levelLabel,2,0)
        layout.addWidget(self.levelSpin,2,1)
        
        layout.addWidget(self.tileLabel,3,0)
        layout.addWidget(self.tileSpin,3,1)
        
        layout.addWidget(self.convertButton,4,1)
        
        self.setLayout(layout)
                
    def chooseImage(self):
        fileName = QFileDialog.getOpenFileName()[0]
        if fileName != "":
            self.imgNameLine.setText(fileName)
            
    def chooseDir(self):
        fileName = QFileDialog.getExistingDirectory()
        if fileName != "":
            self.imgDirLine.setText(fileName)
            
    def convert(self):
        imgName = self.imgNameLine.text()
        dirName = self.imgDirLine.text()
        levels = self.levelSpin.value()
        tileSize = self.tileSpin.value()
        
        dir = QDir(dirName)
        
        if dir.exists(dirName):
            reply = QMessageBox.question(self, 'Message',
                    "Clear input directory?", QMessageBox.Yes | 
                    QMessageBox.No, QMessageBox.No)
            # clear directory if need
            if reply == QMessageBox.Yes:
                for files in os.listdir(dirName):
                    path = os.path.join(dirName, files)
                    try:
                        shutil.rmtree(path)
                    except OSError:
                        os.remove(path)               
        else:
            QMessageBox.warning(self, "Warning", "Directory does not exist")
        
        params = {
            'image_path': imgName,
            'tile_dir': dirName,
            'tile_size': tileSize,
            'lvl_nums': levels,
            'ext': 'png'
        }
        conv = Converter(**params)
        self.progress = QProgressDialog("Convert", "Stop", 0, 100)
        self.progress.setModal(True)
        self.progress.setValue(0)
        self.progress.show()
        self.progress.setWindowTitle("Convert")
        self.progress.setLabelText("Wait please")
        conv.make_tiles(self.progress)
        conv.generate_meta()
        conv.image.close()
        QMessageBox.information(self, "Info", "Converting complite!")
        
        
if __name__ == '__main__':
    # Create the Qt Application
    app = QApplication(sys.argv)
    # Create and show the form
    form = ConverterDialog()
    form.show()
    # Run the main Qt loop
    sys.exit(app.exec())
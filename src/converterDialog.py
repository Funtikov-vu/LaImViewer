import sys
from PySide6.QtWidgets import (QLineEdit, QPushButton, QApplication,
    QVBoxLayout, QDialog, QHBoxLayout, QToolButton, QLabel, QFileDialog)

from PySide6 import QtGui

class ConverterDialog(QDialog):

    def __init__(self, parent=None):
        super(ConverterDialog, self).__init__(parent)
        self.imgNameLable = QLabel("Select image path")
        self.imgNameLine = QLineEdit("Path")
        self.imgButton = QToolButton()
        self.imgButton.setText("...")
        self.imgButton.clicked.connect(self.chooseImage)
        layout1 = QHBoxLayout()
        layout1.addWidget(self.imgNameLable)
        layout1.addWidget(self.imgNameLine)
        layout1.addWidget(self.imgButton)
                
        self.imgDirLable = QLabel("Select LaIm image dir")
        self.imgDirLine = QLineEdit("Dir")
        self.dirButton = QToolButton()
        self.dirButton.setText("...")
        self.dirButton.clicked.connect(self.chooseDir)
        layout2 = QHBoxLayout()
        layout2.addWidget(self.imgDirLable)
        layout2.addWidget(self.imgDirLine)
        layout2.addWidget(self.dirButton)
        
        layout = QVBoxLayout()
        layout.addLayout(layout1)
        layout.addLayout(layout2)
        
        self.setLayout(layout)
                
    def chooseImage(self):
        fileName = QFileDialog.getOpenFileName()[0]
        if fileName != "":
            self.imgNameLine.setText(fileName)
            
    def chooseDir(self):
        fileName = QFileDialog.getExistingDirectory()
        if fileName != "":
            self.imgDirLine.setText(fileName)
            
    


    # Greets the user
    #def greetings(self):
        #print(f"Hello {self.edit.text()}")

if __name__ == '__main__':
    # Create the Qt Application
    app = QApplication(sys.argv)
    # Create and show the form
    form = ConverterDialog()
    form.show()
    # Run the main Qt loop
    sys.exit(app.exec())
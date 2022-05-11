from PyQt5.QtWidgets import QLabel, QTextEdit
from PyQt5.QtCore import Qt

class videoTextBox(QTextEdit):
    def __init__(self):
        super().__init__()
        self.setMinimumHeight(100)
        self.setMinimumWidth(200)
        self.setText('Drag video here')
        self.setAcceptDrops(True)
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setStyleSheet('background-color: grey;')
        self.paths = []

    def dragEnterEvent(self, e):
        if e.mimeData():
            #print('Found video')
            e.accept()

    def dropEvent(self, e):
        if e.mimeData():
            e.setDropAction(Qt.CopyAction)
            #Append all paths of the dragged images to a list.
            self.paths = [url.toLocalFile() for url in e.mimeData().urls()]
            for path in self.paths:
                self.setText('{}\n'.format(path))

class imageTextBox(QTextEdit):
    def __init__(self):
        super().__init__()
        self.setMinimumHeight(100)
        self.setMinimumWidth(200)
        self.setText('Drag Images here')
        self.setAcceptDrops(True)
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setStyleSheet('background-color: grey;')
        self.paths = []
    

    def dragEnterEvent(self, e):
        
        if e.mimeData().hasImage:
            e.accept()
        else:
            e.ignore()
    

    def dropEvent(self, e):
        if e.mimeData().hasImage:
            e.setDropAction(Qt.CopyAction)
            #Append all paths of the dragged images to a list.
            self.paths = [url.toLocalFile() for url in e.mimeData().urls()]
            self.setText('Images Chosen: {}'.format(len(self.paths)))
            #Update text

        else:
            e.ignore()



class SliderLabel(QLabel):
    def __init__(self, text):
        super().__init__()
        self.text = text
    def changeValue(self, e, val):
        if e:
            self.setText('{}: {}%'.format(self.text, val))

from PyQt5.QtWidgets import QPushButton, QFileDialog, QLabel, QCheckBox, QTextEdit
from PyQt5.QtGui import QMouseEvent


class runClassificationButton(QPushButton):
    """
    Button to run inference
    """
    def __init__(self):
        super().__init__('Classify Images')
        self.setMinimumHeight(200)
        self.setMinimumWidth(1000)

    def mousePressEvent(self, e: QMouseEvent) -> None:
        #print('Running Classification...')

        return super().mousePressEvent(e)

class FileButton(QPushButton):
    """
    Button to add files to process
    """
    def __init__(self, title):
        super().__init__(title)
        self.setAcceptDrops(True)
        self.path = QTextEdit()
        #self.setText('Choose')
        self.imagePath = ''
        self.setMinimumHeight(100)
    
    def mousePressEvent(self, e):
        if e:
            path = QFileDialog.getOpenFileName(self, 'Open a file', '', 'All Files (*)')
            if path != ('', ''):
                self.imagePath = path[0]
                self.path.setText(path[0])
            #if e.mimeData():
                #Append all paths of the dragged images to a list.
                #self.paths = [url.toLocalFile() for url in e.mimeData().urls()]
                #for path in self.paths:
                    #self.setText('{}\n'.format(path))
        
        

class VideoCheckboxes(QCheckBox):
    def __init__(self):
        super().__init__()
        self.setText('Save output video')
        self.b1.setChecked(False)
        
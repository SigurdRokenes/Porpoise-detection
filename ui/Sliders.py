from PyQt5.QtWidgets import QSlider
from PyQt5.QtCore import Qt


#from PyQt5.QtGui import *

class Slider(QSlider):
    def __init__(self):
        super().__init__()
        self.setOrientation(Qt.Horizontal)
        self.setRange(0, 100)
        self.setValue(50)
        self.setMinimumHeight(100)
        self.setSingleStep = 5








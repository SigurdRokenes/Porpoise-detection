from PyQt5.QtWidgets import QDialog, QFormLayout, QLabel, QLineEdit, QPushButton, QSpinBox
from PyQt5.QtCore import Qt


class SaveOptions(QDialog):
    def __init__(self):
        super().__init__()

        self.InitUI()
    
    def InitUI(self):
        layout = QFormLayout()
        output_text = QLabel('Video name:')
        self.output_name = QLineEdit('result_vid'+'.mp4')
        fps_text = QLabel('Set frames per second of result video (default = 1)')
        
        self.output_fps = QSpinBox()
        self.output_fps.setValue(1)
        self.output_fps.setMinimum = 1
        self.output_fps.setMaximum = 60

        sampling_text = QLabel('Sample interval from video (seconds). 0 = Not sampling.')
        self.output_samplerate = QSpinBox()
        self.output_samplerate.setValue(0)
        self.output_samplerate.setMinimum = 0

        btn = QPushButton('Save Options')
        btn.clicked.connect(self.close)
        layout.addWidget(output_text)
        layout.addWidget(self.output_name)
        layout.addWidget(fps_text)
        layout.addWidget(self.output_fps)
        layout.addWidget(sampling_text)
        layout.addWidget(self.output_samplerate)
        layout.addWidget(btn)
        
        self.setLayout(layout)

        self.setWindowTitle('Save Options')
        self.setWindowModality(Qt.ApplicationModal)

    def return_values(self):
        return self.output_name.text(), self.output_fps.value(), self.output_samplerate.value()


class ImageSaveOptions(QDialog):
    def __init__(self):
        super().__init__()

        self.InitUI()
    
    def InitUI(self):
        layout = QFormLayout()
        output_text = QLabel('Image name: (numbers are added automatically)')
        self.output_name = QLineEdit('result_image')

        btn = QPushButton('Save Options')
        btn.clicked.connect(self.close)
        layout.addWidget(output_text)
        layout.addWidget(self.output_name)
        layout.addWidget(btn)
        self.setLayout(layout)
        self.setWindowTitle('Save Options')
        self.setWindowModality(Qt.ApplicationModal)

    def return_values(self):
        return self.output_name.text()
import sys, os
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import time
import tensorflow as tf

from ui.config import *
from ui.Sliders import *
from ui.Buttons import *
from ui.Labels import *
from ui.Windows import *
from src.load_model import load_model
from src.detect_video import ClassifyVideo
from src.detect_image import ClassifyImage

#from src.detect_video import ClassifyVideo

load_model_fortesting = True


class GridLayout(QGridLayout):
    def __init__(self):
        super().__init__()
        self.columnCount = 2
        self.rowCount = 4


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Porpoise Detection App')
        self.setFixedSize(QSize(WINDOW_SIZE[0], WINDOW_SIZE[1]))

        self.iou = 50
        self.loaded = 0

        self.InitUI()

    def InitUI(self):
        #self.setWindowTitle(self.title)
        #self.setGeometry(self.top, self.left, self.width, self.height)
        container = QWidget()
        layout = QVBoxLayout()
        container.setLayout(layout)

        #Model Loading text (layout 1)
        self.modelLoadedText = QLabel('Model is loading...')
        sublayout1 = QHBoxLayout()
        sublayout1.addWidget(self.modelLoadedText)
        sublayout1.setAlignment(Qt.AlignCenter)
        
        #Buttons (layout 2)
        sublayout2 = QHBoxLayout()

        buttonImageWindow = QPushButton('Detect from image(s)', self)
        buttonImageWindow.clicked.connect(self.buttonImageWindow_onClick)
        buttonImageWindow.setMinimumHeight(150)

        sublayout2.addWidget(buttonImageWindow)

        buttonVideoWindow = QPushButton('Detect from video', self)
        buttonVideoWindow.setMinimumHeight(150)
        buttonVideoWindow.clicked.connect(self.buttonVideoWindow_onClick)

        sublayout2.addWidget(buttonVideoWindow)
        
        layout.addLayout(sublayout1)
        layout.addLayout(sublayout2)
        self.setCentralWidget(container)

        self.show()

    @pyqtSlot()
    def buttonImageWindow_onClick(self):
        self.statusBar().showMessage("Switched to window 1")
        self.cams = ImageWindow() 
        self.cams.show()
        self.close()

    @pyqtSlot()
    def buttonVideoWindow_onClick(self):
        self.statusBar().showMessage("Switched to window 2")
        self.cams = VideoWindow() 
        self.cams.show()
        self.close()
    
        
class ImageWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Classify Images')
        self.setWindowIcon(self.style().standardIcon(QStyle.SP_FileDialogInfoView))
        self.iou = 50
        self.confidence = 30
        self.loaded = 0
        self.image_path = None
        self.output_name = None
        self.show_images = False
        #self.save_name = 'image'
        self.InitUI()
    
    def InitUI(self):

        layout = QVBoxLayout()
        layout1 = QVBoxLayout()
        layout2 = GridLayout()
        layout3 = QHBoxLayout()
        layout4 = QVBoxLayout()

        self.goBackButton = QPushButton(self)
        self.goBackButton.setStyleSheet('background-color: rgb(0,0,255); color: #fff')
        self.goBackButton.setText('Return to Main Screen')
        self.goBackButton.clicked.connect(self.goMainWindow)
        layout1.addWidget(self.goBackButton)

        self.fileChooseButton = FileButton('Choose single image')
        self.fileChooseButton.path.textChanged.connect(self.update_image_path_from_button)
        self.fileList = imageTextBox()
        self.fileList.textChanged.connect(self.update_image_path)

        self.iouSlider = Slider()
        self.iouSlider.setSingleStep = 5
        iou_text = 'IoU Threshold'
        self.iouLabel = SliderLabel(iou_text)
        self.iouLabel.setText('{}: {}%'.format(iou_text, self.iou))
        self.iouSlider.valueChanged.connect(self.update_iou)

        self.confSlider = Slider()
        self.confSlider.setSingleStep = 5
        conf_text = 'Confidence Threshold'
        self.confLabel = SliderLabel(conf_text)
        self.confSlider.setValue(30)
        self.confLabel.setText('{}: {}%'.format(conf_text, self.confidence))
        self.confSlider.valueChanged.connect(self.update_confidence)


        middleWidgets = [self.fileList, self.fileChooseButton,
                        self.iouLabel, self.iouSlider,
                        self.confLabel, self.confSlider]

        pos = [(i, j) for i in range(4) for j in range(2)]
        for pos, widg in zip(pos, middleWidgets):
            if widg == '':
                continue
            layout2.addWidget(widg, *pos)

        self.show_check = QCheckBox('Show images while processing')
        self.show_check.setChecked(False)
        self.show_check.stateChanged.connect(lambda:self.rad_btn(self.show_check))


        self.save_check= QCheckBox('Save Video')
        self.save_check.setChecked(False)
        self.save_check.stateChanged.connect(lambda:self.rad_btn(self.save_check))

        layout3.addWidget(self.show_check)
        layout3.addWidget(self.save_check)

        self.output_name_label = QLabel()
        layout3.addWidget(self.output_name_label)
        #bottom layout
        classificationButton = runClassificationButton()

        classificationButton.clicked.connect(self.classify_image)
        self.finished_text = QLabel()

        layout4.addWidget(classificationButton)
        layout4.addWidget(self.finished_text)
    

        layout.addLayout(layout1)
        layout.addLayout(layout2)
        layout.addLayout(layout3)
        layout.addLayout(layout4)

        self.setLayout(layout)

    def update_iou(self, e):
        if e:
            self.iou = self.iouSlider.value()
            self.iouLabel.changeValue(e, self.iou)
        
    def update_confidence(self, e):
        if e:
            self.confidence = self.confSlider.value()
            self.confLabel.changeValue(e, self.confidence)

    def goMainWindow(self):
        self.cams = Window()
        self.cams.modelLoadedText.setText('Model Loaded successfully')
        self.cams.show()
        self.close()

    def update_image_path(self):
        self.image_path = self.fileList.paths

    def update_image_path_from_button(self):
        self.image_path = [self.fileChooseButton.imagePath]
        self.fileChooseButton.setText('Chosen image: {}'.format(self.image_path[0]))

    def rad_btn(self, b):
        if b.text() == 'Show images while processing':
            if b.isChecked() == True:
                #print('It is now True')
                self.show_images = False
            
            elif b.isChecked() == False:
                #print('It is now false')
                self.show_images = True
        
        if b.text() == 'Save Images':  
            if b.isChecked() == True:
                self.output_name = self.show_save_options()
            
                self.output_name_label.setText('Output name: {}  '.format(self.output_name))
    
    def show_save_options(self):
        dlg = ImageSaveOptions()
        dlg.exec()
        return dlg.return_values()

    def classify_image(self):
        if self.output_name != None:
            self.finished_text.setText('Processing...')
            ClassifyImage(self.image_path, model = MODEL, size = 1024, output = self.output_name, iou = self.iou / 100,
                          score = self.confidence / 100, dont_show=self.show_images)
            
            self.finished_text.setText('Classification finished. Results can be found in /output/images/{}'.format(self.output_name))
        else:
            self.finished_text.setText('No files chosen.')
        
class VideoWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.iou = 50
        self.confidence = 30
        self.sampling_rate = 0
        self.output_name = None
        self.show_images = False
        self.video_path = None
        self.setWindowTitle('VideoWindow')
        self.setWindowIcon(self.style().standardIcon(QStyle.SP_FileDialogInfoView))

        self.InitUI()

    def InitUI(self):
        #Set layout and Sublayouts
        layout = QVBoxLayout()
        layout1 = QVBoxLayout()
        layout2 = GridLayout()
        layout3 = QHBoxLayout()
        layout4 = QVBoxLayout()

        #Return to mainscreen button
        self.goBackButton = QPushButton(self)
        self.goBackButton.setStyleSheet('background-color: rgb(0,0,255); color: #fff')
        self.goBackButton.setText('Return to Main Screen')
        self.goBackButton.clicked.connect(self.goMainWindow)
        layout1.addWidget(self.goBackButton)

        #Choose file button
        self.fileChooseButton = FileButton('Choose Video')
        self.fileChooseButton.path.textChanged.connect(self.update_video_path_from_button)
        self.fileList = videoTextBox()
        
        self.fileList.textChanged.connect(self.update_video_path)

        #Confidence and IoU Sliders
        self.iouSlider = Slider()
        self.iouSlider.setSingleStep = 5
        iou_text = 'IoU Threshold'
        self.iouLabel = SliderLabel(iou_text)
        self.iouLabel.setText('{}: {}%'.format(iou_text, self.iou))
        self.iouSlider.valueChanged.connect(self.update_iou)

        self.confSlider = Slider()
        self.confSlider.setSingleStep = 5
        conf_text = 'Confidence Threshold'
        self.confLabel = SliderLabel(conf_text)
        self.confSlider.setValue(30)
        self.confLabel.setText('{}: {}%'.format(conf_text, self.confidence))
        self.confSlider.valueChanged.connect(self.update_confidence)

        #Checkbox to choose if saving video
        saveOptions = QLabel('Options for saving classified video:')
        
        #showOptions = QLabel('Show images as they classify (seperate window)')

        middleWidgets = [self.fileList, self.fileChooseButton,
                        self.iouLabel, self.iouSlider,
                        self.confLabel, self.confSlider,
                        saveOptions]
       
        pos = [(i, j) for i in range(4) for j in range(2)]
        for pos, widg in zip(pos, middleWidgets):
            if widg == '':
                continue
            layout2.addWidget(widg, *pos)
        

        self.save_check= QCheckBox('Save Video')
        self.save_check.setChecked(False)
        self.save_check.stateChanged.connect(lambda:self.rad_btn(self.save_check))

        self.show_check = QCheckBox('Show sampled images while processing')
        self.show_check.setChecked(False)
        self.show_check.stateChanged.connect(lambda:self.rad_btn(self.show_check))

        self.output_name_label = QLabel()
        self.output_fps_label = QLabel()
        self.output_samplingrate_label = QLabel()

        layout3.addWidget(self.show_check)
        layout3.addWidget(self.save_check)
        
        layout3.addWidget(self.output_name_label)
        layout3.addWidget(self.output_fps_label)
        layout3.addWidget(self.output_samplingrate_label)

        classificationButton = runClassificationButton()
        classificationButton.clicked.connect(self.classify_video)
        self.finished_text = QLabel()

        layout4.addWidget(classificationButton)
        layout4.addWidget(self.finished_text)
        
        layout.addLayout(layout1)
        layout.addLayout(layout2)
        layout.addLayout(layout3)
        layout.addLayout(layout4)
        
        self.setLayout(layout)
        
        self.show()

    def update_video_path_from_button(self):
        self.video_path = self.fileChooseButton.imagePath
        self.fileChooseButton.setText('Chosen video: {}'.format(self.video_path[0]))

    def update_video_path(self):
        self.video_path = self.fileList.paths[0]
        #print(self.video_path)

    def goMainWindow(self):
        self.cams = Window()
        self.cams.modelLoadedText.setText('Model Loaded successfully')
        self.cams.show()
        self.close()    

    def update_iou(self, e):
        if e:
            self.iou = self.iouSlider.value()
            self.iouLabel.changeValue(e, self.iou)
    
    def update_confidence(self, e):
        if e:
            self.confidence = self.confSlider.value()
            self.confLabel.changeValue(e, self.confidence)
    
    def rad_btn(self, b):
        if b.text() == 'Save Video':
            if b.isChecked() == True:
                self.output_name, self.output_fps, self.sampling_rate  = self.show_save_options()
            
                self.output_name_label.setText('Output name: {}  '.format(self.output_name))
                self.output_fps_label.setText('Saving with {} frames per second.  '.format(self.output_fps))
                if self.sampling_rate != 0:
                    self.output_samplingrate_label.setText('Sampling video with interval of: {} seconds.  '.format(self.sampling_rate))
                else:
                    self.output_samplingrate_label.setText('Not sampling video.  ')
                

        if b.text() == 'Show sampled images while processing':
            if b.isChecked() == True:
                print('It is now True')
                self.show_images = False
            
            elif b.isChecked() == False:
                print('It is now false')
                self.show_images = True

    def classify_video(self):
        if self.fileList.paths != None:
            self.finished_text.setText('Processing...')
            ClassifyVideo(self.video_path, model = MODEL, size = 1024, output = self.output_name, iou = self.iou / 100,
                        score = self.confidence / 100, dont_show=self.show_images, interval = self.sampling_rate)
            
            self.finished_text.setText('Classification finished. Results can be found in /output/{}'.format(self.output_name))
        else:
            self.finished_text.setText('No file chosen.')


    def show_save_options(self):
        dlg = SaveOptions()
        dlg.exec()
        return dlg.return_values()




if __name__ == '__main__':
    app=QApplication(sys.argv)
    #ex = LoadingScreen()
    ex=Window()
    ex.show()
    app.setStyle('Fusion')
    
    if load_model_fortesting:
        print('Load model')
        MODEL = load_model()
        ex.modelLoadedText.setText('Model Loaded successfully')
    sys.exit(app.exec_())

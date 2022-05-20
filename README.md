# Porpoise-detection

YOLOv4 model trained to detect porpoises from drone images. GUI for easy use.

Compiled .exe (no installation requirered) can be downloaded from:

###### Download link (TODO)

## Installation from source
1) Install Anaconda3 or Miniconda3.

2) Download / clone this repo, and open a command prompt in this location.

3) Download model from here:


    ###### [Download Link](https://drive.google.com/drive/folders/1eLdVz99Z16dVR5mH6izrTk8TNoQ7kHnR?usp=sharing)

4) Un-zip and place `models/` folder inside the `Porpoise-Detection` folder.

5) Create a python environment with the required dependencies:

    `conda env create -f requirements.yml`
 
6) Activate the new environment when installation is done.

   `conda activate tf_gpu`

7) Run the program

    `python run.py`
 
 Note: Loading the model might take a few minutes. The program might seem frozen on launch while it is loading.

## Instructions:

## Images:
###### UI Elements explained:
![classify_images_instreuctions](https://user-images.githubusercontent.com/68111038/167891029-8a1804ed-2283-45d7-935a-9b7e4db3c609.png)

1) Return to main screen. Model stays loaded.
2) Drag and drop images you want to classify to this box.
3) Option to drag and drop: Can choose single images.
4) IoU Threshold: Sensitivity to overlapping objects. If there is a trend in multiple bounding boxes for a single object, this value should be lowered a bit. If the detector seems to miss objects that are close-by each other, increase the value.
5) Confidence Threshold: Adjust the cut-off threshold for the probability score from the model. Increasing this will result in increased precision of the model, at the cost of missing detections. Vice-versa, lowering this threshold will result in an increased amount of false positives, but it might miss fewer detections.
6) Option to show the images seperately while processing. Might decrease classification speed depending on hardware.
7) Option to save images the images. Input a name, and the images will be saved to the output folder in order as 'input_name' + 'imagenumber'.
8) Run classification.

## Video

**_Note:_** UI Elements are identical to Images. Only difference is in the save options.

![video_save](https://user-images.githubusercontent.com/68111038/167894496-27f81c8d-3708-4bf4-9f4b-75690052df36.png)

1) The result from this classification will be a video. This sets the number of classified images per second shown in a result video.
2) Sets the number of seconds (in the video) between each image that should be classified. Default value is zero, which classifies every frame of the video.


## Thanks to
1) TheAIGuys work on converting YOLO to Tensorflow. (https://github.com/theAIGuysCode/tensorflow-yolov4-tflite)
2) AlexeyB Darknet YOLOv4 (https://github.com/AlexeyAB/darknet)

import time
import tensorflow as tf
physical_devices = tf.config.experimental.list_physical_devices('GPU')
if len(physical_devices) > 0:
    tf.config.experimental.set_memory_growth(physical_devices[0], True)
import core.utils as utils
from PIL import Image
import cv2
import numpy as np
from tensorflow.compat.v1 import ConfigProto
from tensorflow.compat.v1 import InteractiveSession

def ClassifyVideo(video, model, size, output = None, output_format = 'XVID', iou = 0.5, score = 0.4, dont_show = False, interval = 0):
    """
    Big thanks to TheAIGuy for the core code
    """
    config = ConfigProto()
    config.gpu_options.allow_growth = True
    session = InteractiveSession(config=config)
    STRIDES, ANCHORS, NUM_CLASS, XYSCALE = utils.load_config()
    input_size = size
    video_path = video

    saved_model_loaded = model

    infer = saved_model_loaded.signatures['serving_default']

    if output != None:
        output = 'output/videos/'+output

    try:
        vid = cv2.VideoCapture(int(video_path))
    except:
        #print('Ruh roh')
        vid = cv2.VideoCapture(video_path)
    
    out = None

    width = int(vid.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(vid.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(vid.get(cv2.CAP_PROP_FPS))
    codec = cv2.VideoWriter_fourcc(*output_format)
    out = cv2.VideoWriter(output, codec, 1, (width, height))


    #Number of frames in video
    frame_count = int(vid.get(cv2.CAP_PROP_FRAME_COUNT))
    #Time unit of one frame
    frame_rate = int(vid.get(5))
    #Every n seconds
    
    n = interval
    #Read interval setting
    #read_interval = int((frame_rate * n) - 1)

    print('Frame count: ', frame_count)
    print('frame_rate: ', frame_rate)
    #print('read_interval: ', read_interval)
    #Total number of acquired frames
    if interval != 0:
        frame_all = int((frame_count / frame_rate) / n)
    else:
        frame_all = n
    print('frame_all: ', frame_all)
    #while True:
    for i in range(frame_all):

        if n != 0:

            frame_set = frame_rate * n * i
            if frame_set > frame_count:
                print('Frame_set > Framecount...')
                break

            vid.set(1, frame_set)
            return_value, frame = vid.read()
        
        else:
            return_value, frame = vid.read()
        
        if return_value is False:
            print('Return Value is false, breaking...')
            break

        if return_value:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image = Image.fromarray(frame)
        else:
            print('Video has ended or failed, try a different video format!')
            break
            
        frame_size = frame.shape[:2]
        #print(frame_size)
        image_data = cv2.resize(frame, (input_size, input_size))
        image_data = image_data / 255.
        image_data = image_data[np.newaxis, ...].astype(np.float32)
        start_time = time.time()

        batch_data = tf.constant(image_data)
        pred_bbox = infer(batch_data)

        for key, value in pred_bbox.items():
            boxes = value[:, :, 0:4]
            pred_conf = value[:, :, 4:]
        
        boxes, scores, classes, valid_detections = tf.image.combined_non_max_suppression(
            boxes=tf.reshape(boxes, (tf.shape(boxes)[0], -1, 1, 4)),
            scores=tf.reshape(
                pred_conf, (tf.shape(pred_conf)[0], -1, tf.shape(pred_conf)[-1])),
            max_output_size_per_class=50,
            max_total_size=50,
            iou_threshold=iou,
            score_threshold=score
        )

        pred_bbox = [boxes.numpy(), scores.numpy(), classes.numpy(), valid_detections.numpy()]
        image = utils.draw_bbox(frame, pred_bbox)
        fps = 1.0 / (time.time() - start_time)
        print("FPS: %.2f" % fps)
        result = np.asarray(image)
        cv2.namedWindow("result", cv2.WINDOW_AUTOSIZE)
        result = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        if not dont_show:
            #print('not dont show')
            cv2.imshow("result", result)
        
        if output:
            #print('outputting')
            out.write(result)
        if cv2.waitKey(1) & 0xFF == ord('q'): break
    
    cv2.destroyAllWindows()


"""
if __name__=='__main__':
    ClassifyVideo(video = 'Porpoise-detection/examples/videos/Documentary edit_Large.mp4', size = 1024,
                  output='result001.mp4', iou = 0.5, score = 0.3, dont_show = True, interval = 10)
"""
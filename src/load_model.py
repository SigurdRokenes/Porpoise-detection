import tensorflow as tf
from tensorflow.python.saved_model import tag_constants
from ui.config import MODEL_PATH

def load_model():
    
    #MODEL_PATH = "Porpoise-detection/models/yolov4_1024"
    tf.keras.backend.clear_session()
    #Loads model
    model = tf.saved_model.load(MODEL_PATH, tags=[tag_constants.SERVING])
    print('Model Loaded...')
    return model

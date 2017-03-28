import keras
import os
import numpy as np
import tensorflow as tf
from django.conf import settings
from keras.models import model_from_json
from PIL import Image
from sklearn.preprocessing import LabelEncoder

class HandClassifier:
    instance = None
    class __HandClassifier:
        def __init__(self):
            pass

    def __init__(self):
        if not HandClassifier.instance:
            HandClassifier.instance = HandClassifier.__HandClassifier()
            self.main_path = settings.BASE_DIR + '/mexican_signs/'
            self.model = self.load_model()
            print('[INFO] Loaded model from disk')
            self.graph = tf.get_default_graph()
            self.compile_model()        
            print('[INFO] Model compiled')
            label_order = ['t', 'x', 'r', 'p', 'q', 'n', 'j', 'm', 'f', 'b', 'a', 'z', 'o', 'w', 's',
                           'g', 'c', 'i', 'e', 'l', 'd', 'y', 'h', 'v', 'u']
            self.encoder = LabelEncoder()
            self.labels = self.encoder.fit_transform(label_order)
    
    def load_model(self):
        model_path = os.path.join(self.main_path, 'my_model_architecture.json')
        json_file = open(model_path, 'r')
        loaded_model_json = json_file.read()
        json_file.close()
        return model_from_json(loaded_model_json)

    def compile_model(self):
        weigths_path = os.path.join(self.main_path, 'weights.hdf5')
        self.model.load_weights(weigths_path)
        self.model.compile(loss="categorical_crossentropy", optimizer="rmsprop", 
            metrics=["accuracy"])

    def predict_instance(self, img):
        global graph
        with self.graph.as_default():
            img = np.reshape(img,(1,400))
            predictions = self.model.predict(img)
            prediction = predictions.argmax(axis=-1)
            return self.encoder.inverse_transform([prediction])

    def image_url_to_prediction(self, img_url):
        absolute = settings.BASE_DIR + img_url
        img = Image.open(absolute)
        flat = np.array(img).flatten()
        flat = np.array(flat) / 255.0
        return self.predict_instance(flat)

    def is_valid_input(self, img_url):
        absolute = settings.BASE_DIR + img_url
        img = Image.open(absolute)
        flat = np.array(img).flatten()
        return len(flat) == 400

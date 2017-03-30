import os
import numpy as np
import tensorflow as tf
from django.conf import settings
from keras.models import model_from_json
from PIL import Image
from sklearn.preprocessing import LabelEncoder


class HandClassifier:
    """ Main class for the web application.

    This class loads and compiles a single HandClassifier by implementing a Singleton,
    this class takes an image url as an input and validates if it is a valid image
    for the model.
    It also is used to predict a letter from the image based on the weigths it loads.

    Attributes:
    -----------
    instance : HandClassifierObject
        This is used in order to make sure we only are using a single instanece of this class.
    main_path: String
        The model folder general path
    model: Keras Model
        This model is used to predict the queries.
    encoder: LabelEncoder
        This is used to change from letters to numbers in order to make the right guess.
    """
    instance = None

    class __HandClassifier:
        """ Subclass for the HandClassifier singleton implementation.

        """
        def __init__(self):
            pass

    def __init__(self):
        """ Constructor for the HandClassifier.

        It initializes the model by loading and compiling, it also restablishes the encodes
        """
        if not HandClassifier.instance:
            HandClassifier.instance = HandClassifier.__HandClassifier()
            self.main_path = settings.BASE_DIR + '/mexican_signs/'
            self.model = self.load_model()
            print('[INFO] Loaded model from disk')
            self.graph = tf.get_default_graph()
            self.compile_model()
            print('[INFO] Model compiled')
            label_order = ['t', 'x', 'r', 'p', 'q', 'n', 'm', 'f', 'b', 'a', 'z', 'o', 'w',
                           's', 'g', 'c', 'i', 'e', 'l', 'd', 'y', 'h', 'v', 'u']
            self.encoder = LabelEncoder()
            self.labels = self.encoder.fit_transform(label_order)

    def load_model(self):
        """ Function which loads the model from the main path

        """
        model_path = os.path.join(self.main_path, 'my_model_architecture.json')
        json_file = open(model_path, 'r')
        loaded_model_json = json_file.read()
        json_file.close()
        return model_from_json(loaded_model_json)

    def compile_model(self):
        """ Function which compiles the model with the weights from the main path

        """
        weigths_path = os.path.join(self.main_path, 'weights.hdf5')
        self.model.load_weights(weigths_path)
        self.model.compile(loss="categorical_crossentropy", optimizer="rmsprop",
                           metrics=["accuracy"])

    def predict_instance(self, img):
        """ Function which predicts the content of the image

        This takes an image as an input and it feeds it to the previously trained model in order
        to get a list of predictions of the possible classes, this is interpreted an the label of
        the actual class is returned.
        """
        global graph
        with self.graph.as_default():
            img = np.reshape(img, (1, 400))
            predictions = self.model.predict(img)
            prediction = predictions.argmax(axis=-1)
            return self.encoder.inverse_transform([prediction])

    def image_url_to_prediction(self, img_url):
        """ Function which predicts given a url

        This takes as an input a string which represents the url of an image which is loaded in
        memory, preprocessed and fed to the predict_instance function.
        """
        absolute = settings.BASE_DIR + img_url
        img = Image.open(absolute)
        flat = np.array(img).flatten()
        flat = np.array(flat) / 255.0
        return self.predict_instance(flat)

    def is_valid_input(self, img_url):
        """ Function which validates the image url corresponds to a valid image for the model.

        """
        absolute = settings.BASE_DIR + img_url
        img = Image.open(absolute)
        flat = np.array(img).flatten()
        return len(flat) == 400

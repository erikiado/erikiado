import numpy as np
from PIL import Image
from django.conf import settings
from django.test import TestCase
from erikiado.mexican_signs.hand_classifier import HandClassifier


class HandClassifierUnitTests(TestCase):
    """Unit test suite for testing the HandClassifier

    Test that the views for 'administracion' are correctly received as a response and that
    they use the correct template.
    """

    def setUp(self):
        """Initialize the HandClassifier and get initial address

        """
        self.hand_clf = HandClassifier()
        self.initial_address = hex(id(self.hand_clf))

    def test_init(self):
        """Unit Test: Test the HandClassifier can be created correctly

        """
        self.hand_clf = None
        self.assertEqual(self.hand_clf, None)
        self.hand_clf = HandClassifier()
        self.assertNotEqual(self.hand_clf, None)

    def test_singleton_pattern(self):
        """Unit Test: Test the singleton pattern on the classifier

        Test the memory address of the classifier is the same when a new
        constructor is called.
        """
        self.hand_clf = HandClassifier()
        self.assertEqual(self.initial_address, hex(id(self.hand_clf)))

    def test_validator_valid(self):
        """Unit Test: Test the HandClassifier can validate the image correctly

        """
        image_url = '/../test_images/a/0.png'
        self.assertTrue(self.hand_clf.is_valid_input(image_url))

    def test_validator_invalid(self):
        """Unit Test: Test the HandClassifier can validate the invalid image correctly

        """
        image_url = '/../test_images/invalid.png'
        self.assertFalse(self.hand_clf.is_valid_input(image_url))

    def test_image_prediction(self):
        """Unit Test: Test the HandClassifier can make an accurate prediction from an image

        """
        image_url = '/../test_images/a/0.png'
        absolute = settings.BASE_DIR + image_url
        img = Image.open(absolute)
        flat = np.array(img).flatten()
        self.assertEqual(self.hand_clf.predict_instance(flat)[0][0], 'a')

    def test_url_prediction(self):
        """Unit Test: Test the HandClassifier can make an accurate prediction from an image url

        """
        image_url = '/../test_images/a/0.png'
        self.assertEqual(self.hand_clf.image_url_to_prediction(image_url)[0][0], 'a')

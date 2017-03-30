import time
import os
from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from splinter import Browser


class WebSiteUnitTests(TestCase):
    """Unit test suite for testing the HandClassifier

    Test that the views for 'administracion' are correctly received as a response and that
    they use the correct template.
    """

    def setUp(self):
        pass

    def test_view_main_page(self):
        """Unit Test: Test for url with name 'classifier_upload'

        """
        test_url_name = 'classifier_upload'
        response = self.client.get(reverse(test_url_name), follow=True)
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, 'projects/msl.html')


class WebSiteIntegrationTests(StaticLiveServerTestCase):
    """Integration test suite for testing the HandClassifier Site

    Test that the view from the classifier works as expected.
    This means it should receive only a certain type of image and that it actually
    classifies and gives a result.
    """

    def setUp(self):
        """Initialize the browser and visit the app url

        """
        self.browser = Browser('chrome')
        self.browser.visit(self.live_server_url + reverse('classifier_upload'))

    def tearDown(self):
        """At the end of tests, close the browser.

        """
        self.browser.quit()

    def test_main_page(self):
        """Test for url with name 'classifier_upload'

        Check it actually renders what is expected from this template
        """
        test_text = 'Clasificación de Imágenes: Lenguaje de Señas Mexicano'
        self.assertTrue(self.browser.is_text_present(test_text))

    def test_main_button(self):
        """ Test for url with name 'classifier_upload'

        Check if the url is accesible and check the buttons are showing correctly
        """
        self.assertTrue(self.browser.is_text_present('SELECCIONAR IMAGEN'))
        self.assertTrue(self.browser.is_text_present('CLASIFICAR'))

    def test_accurate_classification(self):
        """ Test for url with name 'classifier_upload'

        Check that the prediction is the desired
        Check that the model is accurate
        """
        cwd = os.getcwd()
        self.browser.attach_file('hand_img', cwd + '/test_images/a/0.png')
        time.sleep(2)
        self.browser.find_by_id('guardar').click()
        self.assertTrue(self.browser.is_text_present('Resultado: a'))

    def test_invalid_image(self):
        """ Test for url with name 'classifier_upload'

        Check that any invalid image is getting an error
        """
        cwd = os.getcwd()
        self.assertFalse(self.browser.is_text_present('Error:'))
        self.browser.attach_file('hand_img', cwd + '/test_images/invalid.png')
        time.sleep(2)
        self.browser.find_by_id('guardar').click()
        self.assertTrue(self.browser.is_text_present('Error:'))

    def test_no_image(self):
        """ Test for url with name 'classifier_upload'

        Check that if no image is uploaded it returns the error.
        """
        self.assertFalse(self.browser.is_text_present('Error:'))
        self.browser.find_by_id('guardar').click()
        self.assertTrue(self.browser.is_text_present('Error:'))

    def test_image_upload(self):
        """ Test for url with name 'classifier_upload'

        Check the image is shown inmediately after being selected.
        """
        cwd = os.getcwd()
        img = self.browser.find_by_id('imageTemp1')
        self.browser.attach_file('hand_img', cwd + '/test_images/a/0.png')
        time.sleep(2)
        img = self.browser.find_by_id('imageTemp1')
        # Check if the content is the recently loaded
        self.assertTrue('data:' in img['src'])

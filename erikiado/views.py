# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from .mexican_signs.hand_classifier import HandClassifier
# from .models import Prediction

# Create a single HandClassifier when the app starts.
hands_clf = HandClassifier()


def home(request):
    """ View to redirect to the DAS app if erikiado.com is reached.

    """
    # return render(request, "erikiado/index.html", {})
    return redirect('classifier_upload')


def piradio(request):
    """ View to render PiRadio project

    """
    return render(request, "projects/piradio.html", {})


def muestrame(request):
    """ View to render muestraMe project.

    """
    return render(request, "projects/muestrame.html", {})


def tosp(request):
    """ View to render [tosp] project.

    """
    return render(request, "projects/tosp.html", {})


def znake(request):
    """ View to render Znake project.

    """
    return render(request, "projects/znake.html", {})


def life(request):
    """ View to render Game of Life project.

    """
    return render(request, "projects/life.html", {})


def manos(request):
    """ View to render Hand Sign Dataset project.

    """
    return render(request, "projects/manos.html", {})


def tianguis(request):
    """ View to render Tianguis project.

    """
    return render(request, "projects/tianguis.html", {})


def msl(request):
    """ View to render Mexican Sign Language project.

    """
    return render(request, 'projects/msl.html', {})


def classifier_upload(request):
    """ View to render the classifier GUI.

    If the request is a POST the image is given as an input to the HandClassifier
    and the answer is passed to the template to be displayed.
    """
    context = {}
    if request.method == 'POST':
        if 'hand_img' in request.FILES:
            file = request.FILES['hand_img']
            fs = FileSystemStorage()
            file_neu_name = 'test.' + file.name.split('.')[-1]
            filename = fs.save(file_neu_name, file)
            uploaded_file_url = fs.url(filename)
            # Check if the image is valid for the HandClassifier
            if hands_clf.is_valid_input(uploaded_file_url):
                answer = hands_clf.image_url_to_prediction(uploaded_file_url)[0][0]
                context['label'] = answer
                context['img_url'] = uploaded_file_url
            else:
                context['error'] = 'La imagen no es valida, se requiere una imagen de \
                                    20x20 pixeles en solo una dimension'
        else:
            context['error'] = 'La imagen no es valida, se requiere una imagen de \
                                20x20 pixeles en solo una dimension'
    return render(request, 'projects/msl.html', context)

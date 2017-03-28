# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from .mexican_signs.hand_classifier import HandClassifier
from .mexican_signs.image_processor import upload_image
from .models import Prediction

hands_clf = HandClassifier()

def home(request):
    return redirect('classifier_upload')
	# return render(request, "erikiado/index.html", {})

def piradio(request):
	return render(request, "projects/piradio.html", {})

def muestrame(request):
	return render(request, "projects/muestrame.html", {})

def tosp(request):
	return render(request, "projects/tosp.html", {})
 
def znake(request):
	return render(request, "projects/znake.html", {})

def life(request):
	return render(request, "projects/life.html", {})

def manos(request):
	return render(request, "projects/manos.html", {})

def tianguis(request):
	return render(request, "projects/tianguis.html", {})

def msl(request):
    return render(request, 'projects/msl.html', {})

def classifier_upload(request):
    context = {}
    if request.method == 'POST':
        file = request.FILES['hand_img']
        fs = FileSystemStorage()
        file_neu_name = 'prueba.' + file.name.split('.')[-1]
        filename = fs.save(file_neu_name, file)
        uploaded_file_url = fs.url(filename)
        if hands_clf.is_valid_input(uploaded_file_url):
            answer = hands_clf.image_url_to_prediction(uploaded_file_url)[0][0]
            context['label'] = answer
            context['img_url'] = uploaded_file_url
        else:
            context['error'] = 'La imagen no es valida, se requiere una imagen de 20x20 pixeles en solo una dimension'
    return render(request, 'projects/msl.html', context)

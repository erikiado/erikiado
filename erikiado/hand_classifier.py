# -*- coding: utf-8 -*-
from django.shortcuts import render
from classifier import HandClassifier
def home(request):
	return render(request, "erikiado/index.html", {})

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
    if request.method == 'POST':
        print(request.POST)
        print(request.FILES)
    return render(request, 'projects/msl.html', {})

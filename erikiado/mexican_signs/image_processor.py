
def upload_image(img):
    file_name = 'static/hands/prueba.'+((img.name).split('.')[1])
    with open(file_name, 'wb+') as destination:
        for chunk in img.chunks():
            destination.write(chunk)

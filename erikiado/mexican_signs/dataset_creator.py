import cv2
import numpy as np
import sys
import os

# Size of the batch to train with
tamBatch = 300

# Path to the directory
pathArchivo = os.path.dirname(os.path.realpath(__file__))

# RANGES
rango = {}
rango['piel'] = [np.array([0, 20, 10]),
                 np.array([30, 200, 255])]
rango['rojo'] = [np.array([170, 20, 10]),
                 np.array([179, 230, 255])]
rango['control'] = [np.array([0, 0, 0]),
                    np.array([0, 0, 0])]


def ignore_parameter(x):
    """ Function to ignore the parameter which is passed in a cv2 function

    """
    pass


def encontrarMano(contours):
    """ Function to find the hand coordinates in the contours found on the image

    """
    areaMayor = 0
    contMayor = contours[0]
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if(area > areaMayor):
            areaMayor = area
            contMayor = cnt

    maxX = maxY = 0
    minX = minY = 100000
    for i in contMayor:
        x = i[0][0]
        y = i[0][1]
        maxX = max(maxX, x)
        minX = min(minX, x)
        maxY = max(maxY, y)
        minY = min(minY, y)
    maxX += 50
    minX -= 50
    minY -= 50
    maxY = minY + (maxX - minX)
    return minY, maxY, minX, maxX


def procesar(img):
    """ Function to preprocess each frame in order to get the mask of the image

    """
    bilBlur = cv2.bilateralFilter(img, 7, 75, 75)
    hsv = cv2.cvtColor(bilBlur, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, rango['control'][0], rango['control'][1])
    msk1 = cv2.inRange(hsv, rango['control'][0], rango['control'][1])
    return mask, msk1


def crearDirectorios(letra):
    """ Function to create the directories needed if they are not already created

    """
    pathOrg = "/dset/org/" + letra + "/"
    pathMask = "/dset/mask/" + letra + "/"
    path20 = "/dset/20x20/" + letra + "/"
    path40 = "/dset/40x40/" + letra + "/"
    pathMama = "/dset/mama/" + letra + "/"
    pathMano = "/dset/mano/" + letra + "/"
    wd = pathArchivo
    if not os.access(pathArchivo + "/dset", os.R_OK):
        os.mkdir(wd + "/dset")
        os.mkdir(wd + "/dset/org")
        os.mkdir(wd + "/dset/mask")
        os.mkdir(wd + "/dset/40x40")
        os.mkdir(wd + "/dset/20x20")
        os.mkdir(wd + "/dset/mama")
        os.mkdir(wd + "/dset/mano")
    os.mkdir(wd + pathMama)
    os.mkdir(wd + pathOrg)
    os.mkdir(wd + pathMano)
    os.mkdir(wd + pathMask)
    os.mkdir(wd + path20)
    os.mkdir(wd + path40)


def crearMinis(org, y, x):
    """ Function to resize the images to the dataset size 20x20 and 40x40

    """
    i20 = cv2.resize(org, (20, 20))
    i40 = cv2.resize(org, (40, 40))
    return i20, i40


# Start script if the batch number and letter are received
if(len(sys.argv) > 2):
    # Initialize camera and variables needed
    camara = cv2.VideoCapture(0)
    font = cv2.FONT_HERSHEY_PLAIN
    _, original = camara.read()
    tomandoFrames = False
    contadorFrame = 0

    # Kernel
    k3 = (3, 3)

    letra = str(sys.argv[1]).lower()
    pathMuestra = "muestras/" + letra + ".png"
    pathOrg = "dset/org/" + letra + "/"
    pathMask = "dset/mask/" + letra + "/"
    path20 = "dset/20x20/" + letra + "/"
    path40 = "dset/40x40/" + letra + "/"
    pathMama = "dset/mama/" + letra + "/"
    pathMano = "dset/mano/" + letra + "/"
    batch = int(sys.argv[2])
    cont = batch * tamBatch
    finBatch = (batch * tamBatch) + tamBatch

    # Load the image of the sign no copy
    muestra = cv2.imread(pathMuestra, 0)
    cv2.imshow(('Muestra de letra: ' + letra), muestra)
    # Create a controls window which control the mask values
    cv2.namedWindow('control')
    cv2.createTrackbar('HI', 'control', 0, 179, ignore_parameter)
    cv2.createTrackbar('HS', 'control', 25, 179, ignore_parameter)
    cv2.createTrackbar('SI', 'control', 40, 255, ignore_parameter)
    cv2.createTrackbar('SS', 'control', 240, 255, ignore_parameter)
    cv2.createTrackbar('VI', 'control', 50, 255, ignore_parameter)
    cv2.createTrackbar('VS', 'control', 190, 255, ignore_parameter)
    guardar = False
    teclas = ""

    # Create directories if they dont exist
    if not os.access(pathArchivo + "/" + pathMama, os.R_OK):
        crearDirectorios(letra)

    while(True):
        # Take the picture or frame from the stream
        _, original = camara.read()
        presentacion = mask = original
        nombreImg = str(cont) + ".png"

        # Update the value from the trackbar
        hi = cv2.getTrackbarPos('HI', 'control')
        si = cv2.getTrackbarPos('SI', 'control')
        vi = cv2.getTrackbarPos('VI', 'control')
        hs = cv2.getTrackbarPos('HS', 'control')
        ss = cv2.getTrackbarPos('SS', 'control')
        vs = cv2.getTrackbarPos('VS', 'control')

        # Ranges to mask
        rango['control'][0] = np.array([hi, vi, si])
        rango['control'][1] = np.array([hs, vs, ss])

        # Filter the image every 5 frames
        if contadorFrame % 5 == 0:
            mask, mk1 = procesar(original)
            cv2.imshow('control', mask)
            # Get the blobs in the mask
            _, contours, _ = cv2.findContours(mk1, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            # If there is a blob, get the one with most area
            if len(contours) != 0 and tomandoFrames:
                minY, maxY, minX, maxX = encontrarMano(contours)
                if minY < maxY and minX < maxX:
                    # If something was found, calculate the square which contains the blob
                    yAurea = maxY
                    mano = original[minY:yAurea, minX:maxX]
                    mama = mask[minY:yAurea, minX:maxX]
                    mama = cv2.morphologyEx(mama, cv2.MORPH_CLOSE, k3)
                    if mama is not None:
                        # If there is a big blob, create the miniatures for the model
                        # and save the images
                        cv2.imshow("j", mama)
                        X = maxX - minX
                        Y = yAurea - minY
                        img20, img40 = crearMinis(mama, Y, X)
                        # Activate save state
                        guardar = True

        # Present the images in their corresponding window and with some text
        cv2.putText(presentacion, ("(Z) Tomar Frames: " + str(tomandoFrames)), (20, 30), font, 1,
                    (0, 0, 0), 1, cv2.LINE_AA)
        cv2.putText(presentacion, ("Path: ./dset/$tipo/" + letra + "/" + nombreImg), (20, 40),
                    font, 1, (0, 0, 0), 1, cv2.LINE_AA)
        cv2.putText(presentacion, str(contadorFrame), (20, 50), font, 1, (0, 0, 0), 1, cv2.LINE_AA)
        cv2.putText(presentacion, teclas, (20, 60), font, 1, (0, 0, 0), 1, cv2.LINE_AA)
        cv2.imshow('Estado', presentacion)

        if guardar:
            # If save state save the images on their corresponding paths
            cv2.imwrite(pathArchivo + '/' + pathMask + nombreImg, mask)
            cv2.imwrite(pathArchivo + '/' + pathMama + nombreImg, mama)
            cv2.imwrite(pathArchivo + '/' + pathMano + nombreImg, mano)
            cv2.imwrite(pathArchivo + '/' + pathOrg + nombreImg, original)
            cv2.imwrite(pathArchivo + '/' + path20 + nombreImg, img20)
            cv2.imwrite(pathArchivo + '/' + path40 + nombreImg, img40)
            cont += 1
            guardar = False
        # Update the counter
        contadorFrame += 1

        # Controls section
        # Listen to keys
        k = cv2.waitKey(30) & 0xff  # Bitwise And: Abs
        if k != 255:
            teclas += chr(k)
            # If 'z' key is pressed start capturing
            if k == ord('z'):
                if tomandoFrames:
                    tomandoFrames = False
                else:
                    tomandoFrames = True
            # If 'esc' key is pressed finish
            elif k == 27:
                break
        # Finish if the batch is complete
        if cont > finBatch:
            break
    camara.release()
    cv2.destroyAllWindows()
else:
    # Error
    print("Chavo, te hacen falta parametros:\npython " + sys.argv[0] + " $letra $batch")

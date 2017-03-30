""" This script assumes the dataset_creator script was already used.
    The purpose of this script is to create a new dataset directory were the images on the original
    dataset are transformed multiple times and saved in order to expand the dataset which will be
    used to train the model for more accuracy in general cases.
"""
import cv2
import sys
import os
import random as r


def crearCarpeta(wd):
    """ Function which creates the directory if it is not already created

    """
    if not os.access(wd, os.R_OK):
        os.mkdir(wd)


pathArchivo = os.path.dirname(os.path.realpath(__file__))

# Check the script receives an argument which needs to be a path to the dataset
if len(sys.argv) != 1:
    directory = pathArchivo + "/" + sys.argv[1]
    crearCarpeta(pathArchivo + "/dset_t/")
    # For each directory in the dataset get its path and create the same directory
    # on the new dataset
    for root, dirs, files in os.walk(directory):
        crearCarpeta(pathArchivo + "/dset_t/" + root.split("/")[-2])
        wd = pathArchivo + "/dset_t/" + root.split("/")[-2] + "/" + root.split("/")[-1]
        crearCarpeta(wd)
        cont = 0
        print(wd)
        # For each file in the directory
        for x in files:
            # Read the file as an image
            img = cv2.imread((root + "/" + x), 0)
            # Calculate the shape of the image to find the center
            (h, w) = img.shape[:2]
            center = (w / 2, h / 2)
            cv2.imwrite(wd + "/" + str(cont) + ".png", img)
            cont += 1

            # Generate 12 images from the original each rotated 30 degrees
            for i in range(0, 360, 30):
                zoom = 1.0
                if i % 90 > 20 and i % 90 < 75:
                    zoom = 1.2
                if i % 90 > 34 and i % 90 < 60:
                    zoom = 1.4
                M = cv2.getRotationMatrix2D(center, r.randint(i, i+30), zoom)
                rotated = cv2.warpAffine(img, M, (w, h))
                # Save the new image on the new dataset
                cv2.imwrite(wd + "/" + str(cont) + ".png", rotated)
                cont += 1
else:
    print("rot.py directory")

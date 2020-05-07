# -*- encoding: utf-8 -*-
import PIL.Image
import numpy

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def get_image_np(image_file):
    image = PIL.Image.open(image_file)
    return numpy.array(image)

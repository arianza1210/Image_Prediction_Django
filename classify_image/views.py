from django.shortcuts import render
from django.http import JsonResponse
import base64
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.conf import settings
import tensorflow as tf
from tensorflow.keras.preprocessing.image import load_img
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.applications.imagenet_utils import decode_predictions
import matplotlib.pyplot as plt
import numpy as np
from tensorflow.keras.applications import vgg16
import datetime
import traceback


def index(request):
    if request.method == "POST":
        f = request.FILES['sentFile']  # here you get the files needed
        response = {}
        file_name = "pic.jpg"
        file_name_2 = default_storage.save(file_name, f)
        file_url = default_storage.url(file_name_2)
        original = load_img(file_url, target_size=(224, 224))
        numpy_image = img_to_array(original)

        image_batch = np.expand_dims(numpy_image, axis=0)
        # prepare the image for the VGG model
        processed_image = vgg16.preprocess_input(image_batch.copy())

        # get the predicted probabilities for each class
        predictions = settings.VGG_MODEL.predict(processed_image)

        label = decode_predictions(predictions)
        label = list(label)[0]
        response['name'] = str(label)
        return render(request, 'homepage.html', response)
    else:
        return render(request, 'homepage.html')


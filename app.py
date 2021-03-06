from __future__ import division, print_function
import numpy as np
from flask import Flask, request, jsonify, render_template
import pickle

# coding=utf-8
import sys
import os
import glob
import re
import numpy as np

# Keras
from keras.applications.imagenet_utils import preprocess_input, decode_predictions
from keras.models import load_model
from keras.preprocessing import image
from tensorflow.keras.models import Sequential

# Flask utils
from flask import Flask, redirect, url_for, request, render_template
from werkzeug.utils import secure_filename
from gevent.pywsgi import WSGIServer


model = pickle.load(open('model.pkl', 'rb'))   



UPLOAD_FOLDER = '/static/uploads'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def model_predict(img_path, model):
    test_image = image.load_img(img_path, target_size=(64, 64))
    test_image=image.img_to_array(test_image) #converts it into 3d array
    test_image=np.expand_dims(test_image,axis=0)
    prediction = model.predict(test_image)
    return prediction

@app.route('/')
def home_page():
    return render_template('index.html')


@app.route('/predict',methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        if 'file' not in request.files:
            return render_template('index.html', prediction_text='No file at all ! ! ')
        file = request.files['file']

        if file.filename == '':
            return render_template('index.html', prediction_text='File Error ! ')

        if file and allowed_file(file.filename):
            file_path=os.path.join(os.getcwd() + UPLOAD_FOLDER, file.filename)
            file.save(file_path)
            prediction = model_predict(file_path, model)
            if(prediction[0]==0):
                output="Cat!!"
                pic='https://rocketpopmedia.com/wp-content/uploads/2011/12/500x300.jpeg'
                
            else:
                output="Dog!!"
                pic='https://www.bentonsroadvet.com.au/wp-content/uploads/2016/07/Dental%20problems-.png'
            return render_template('final.html', prediction_text='Your animal is a : {}'.format(output),pic=pic)
            



if __name__ == '__main__':
    app.run(debug=True)
    

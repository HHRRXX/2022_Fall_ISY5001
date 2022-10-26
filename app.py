from flask import  Flask, render_template, jsonify, request
app=Flask(__name__)
from sklearn.preprocessing import LabelEncoder
import joblib

import json
import pandas as pd
import pickle
import numpy as np
import base64
from io import BytesIO
from PIL import Image
from test import predict
from genre import detect
clf = joblib.load('models/best.pkl')
genre = pd.read_csv('genre.csv',index_col=0)
genre = pd.DataFrame(genre['Genre'])
vectorizer = pickle.load(open("models/vectorizer.pickle", "rb"))
encoder = LabelEncoder()
encoder.classes_ = np.load('models/classes.npy')
@app.route('/getCategoryByName', methods=['GET'])
def getCategoryByName():
        
        bookName = request.args.get('bookName')
        bookName = [bookName]
        # handle the request and return 
        bookName[0] = bookName[0].lower()
        c = vectorizer.transform(bookName)
        d = (clf.predict(c))
        cate = encoder.inverse_transform(d)[0]
        return jsonify({"category":cate, "name":bookName})


@app.route('/getPopularity', methods=['POST'])
def getPopularity():
        data = json.loads(request.get_data())
        imageBase64Str = data['imageBase64Str']
        imageBase64Str = imageBase64Str[imageBase64Str.index(","):]
        img_data = base64.b64decode(imageBase64Str)
        image = Image.open(BytesIO(img_data))
        image = image.convert('RGB')
        #image.show()
        # todo 用 image 对象做 ocr，返回popularity
        gen = detect(image)
        popularity = predict(image)+1
        return jsonify({"popularity":popularity,'Genre':gen})


@app.route('/')
def index():
        return render_template("index.html")


if __name__=="__main__":
    app.run(port=8080,host="127.0.0.1",debug=True)

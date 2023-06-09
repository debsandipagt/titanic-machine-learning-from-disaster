from flask import Flask, request, jsonify, app, url_for, render_template
import numpy as np
import pandas as pd
import pickle

app = Flask(__name__)

svmmodel = pickle.load(open('titanic_model0.1.0.pkl', 'rb'))
scaler = pickle.load(open('scaling.pkl', 'rb'))

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/predict_api', methods = ['POST'])
def predict_api():
    data = request.json['data']
    print(data)
    print(np.array(list(data.values())).reshape(1,-1))
    new_data = scaler.transform(np.array(list(data.values())).reshape(1,-1))
    output = svmmodel.predict(new_data)
    print(output)
    if output == 0:
        result = 'Passenger died'
    else:
        result = 'Passenger is alive'
    return jsonify(result)

@app.route('/predict', methods=['POST'])
def predict():
    data = [x if x != '' else '0' for x in request.form.values()]
    final_input = scaler.transform(np.array(data).reshape(1, -1))
    print(final_input)
    output = svmmodel.predict(final_input)
    if output == 0:
        prediction_text = "died"
    else:
        prediction_text = "survived"
    return render_template('home.html', prediction_text='The Predicted outcome is {}'.format(prediction_text))
    
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)

    
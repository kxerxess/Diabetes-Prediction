# Serve model as a flask application

import pickle
import numpy as np
from flask import Flask, request, url_for, redirect, render_template
import tensorflow

model = None
scaler = None
app = Flask(__name__)


def load_model_prereq():
    global model
    global scaler
    # model variable refers to the global variable
    # with open('trained_models/final_model.pkl', 'rb') as f:
    #     model = pickle.load(f)
    model = tensorflow.keras.models.load_model('trained_models/TF_128x128x32x32_bs16_rms_200e_rs154_acc90.h5')
    with open('scaler/scaler.pkl', 'rb') as f:
        scaler = pickle.load(f)


@app.route('/')
def home_endpoint():
    return render_template("index.html")


@app.route('/predict', methods=['POST', 'GET'])
def get_prediction():
    # Works only for a single sample
    values = [x for x in request.form.values()]
    # Standard Properties
    user_dict = {"Pregnancies": int(values[0]), "Glucose": float(values[1]), "BloodPressure": float(values[2]),
                 "SkinThickness": float(values[3]), "Insulin": float(values[4]), "BMI": float(values[5]), "Age": int(values[6])}
    # Additional Features

    #f0
    if user_dict['Age']<=30 and user_dict['Glucose']<=120:
        user_dict['f0']=1
    else:
        user_dict['f0']=0

    #f1
    if user_dict['BMI']<=30:
        user_dict['f1']=1
    else:
        user_dict['f1']=0

    #f2
    if user_dict['Age']<=30 and user_dict['Pregnancies']<=6:
        user_dict['f2']=1
    else:
        user_dict['f2']=0

    #f3
    if user_dict['Glucose']<=105 and user_dict['BloodPressure']<=80:
        user_dict['f3']=1
    else:
        user_dict['f3']=0

    #f4
    if user_dict['BMI']<30 and user_dict['SkinThickness']<=20:
        user_dict['f4']=1
    else:
        user_dict['f4']=0

    #f5
    if user_dict['Glucose']<=105 and user_dict['BMI']<=30:
        user_dict['f5']=1
    else:
        user_dict['f5']=0

    #f6
    if user_dict['SkinThickness']<=20:
        user_dict['f6']=1
    else:
        user_dict['f6']=0

    #f7
    if user_dict['Insulin']<=200:
        user_dict['f7']=1
    else:
        user_dict['f7']=0

    #f8
    if user_dict['BloodPressure']<=80:
        user_dict['f8']=1
    else:
        user_dict['f8']=0

    #f9
    if user_dict['Pregnancies']<4 and user_dict['Pregnancies']!=0:
        user_dict['f9']=1
    else:
        user_dict['f9']=0

    #f10, f11, f12
    user_dict['f10']=user_dict['BMI']*user_dict['SkinThickness']
    user_dict['f11'] = user_dict['Pregnancies'] / user_dict['Age']
    user_dict['f12'] = user_dict['Age'] / user_dict['Insulin']

    #f13
    if user_dict['f10']<1034:
        user_dict['f13']=1
    else:
        user_dict['f13']=0

    num_val = []
    cat_val = []
    num_feat = ['Pregnancies', 'Glucose', 'BloodPressure', 'SkinThickness', 'Insulin', 'BMI', 'Age', 'f10', 'f11', 'f12']
    cat_feat = ['f0', 'f1', 'f2', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8', 'f9', 'f13']
    for i in num_feat:
        num_val.append(user_dict[i])
    for i in cat_feat:
        cat_val.append(user_dict[i])

    num_val = np.array(num_val)
    num_val = scaler.transform(np.array([num_val]))

    final_val = np.append(num_val, cat_val)
    final_val = np.array([final_val])

    pred = model.predict(final_val)

    if pred>0.5:
        result='DIABETIC'
        accuracy=pred*100
        return render_template("result_diabetic.html", prediction=str(result), accuracy=accuracy[0][0])
    elif pred<=0.5:
        result='NOT DIABETIC'
        accuracy=(1-pred)*100
        return render_template("result_non.html", prediction=str(result), accuracy=accuracy[0][0])
    return None


if __name__ == '__main__':
    load_model_prereq()  # load model at the beginning once only
    app.run(host='127.0.0.1', port=5000, debug=False)

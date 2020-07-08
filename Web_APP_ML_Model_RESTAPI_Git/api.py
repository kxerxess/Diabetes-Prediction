import pandas as pd
import joblib
from flask import Flask
from flask_restful import reqparse, abort, Api, Resource

app = Flask(__name__)
api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument("recieved_input")

scaler_loaded = joblib.load("Scaler/Scaler_MinMax_0_1.pkl")
rfc_loaded = joblib.load("Trained_Models/Model_RandomForestClassifier_88.pkl")

def string_to_float_array(input_data):
    x = input_data.split(',')
    x =[float(i) for i in x]
    return x

def ml_predict(input_data):
    input_data =[input_data]
    #adding additional features(f0-f13)
    label= ["Pregnancies","Glucose","BloodPressure","SkinThickness","Insulin","BMI","Age"]
    data = pd.DataFrame(input_data, columns=label)
    # f0
    data.loc[:,'F0']=0
    data.loc[(data['Age']<=30) & (data['Glucose']<=120),'F0']=1
    # f1
    data.loc[:,'F1']=0
    data.loc[(data['BMI']<=30),'F1']=1
    # f2
    data.loc[:,'F2']=0
    data.loc[(data['Age']<=30) & (data['Pregnancies']<=6),'F2']=1
    # f3
    data.loc[:,'F3']=0
    data.loc[(data['Glucose']<=105) & (data['BloodPressure']<=80),'F3']=1
    # f4
    data.loc[:,'F4']=0
    data.loc[(data['BMI']<30) & (data['SkinThickness']<=20),'F4']=1
    # f5
    data.loc[:,'F5']=0
    data.loc[(data['Glucose']<=105) & (data['BMI']<=30),'F5']=1
    # f6
    data.loc[:,'F6']=0
    data.loc[(data['SkinThickness']<=20) ,'F6']=1
    # f7
    data.loc[:,'F7']=0
    data.loc[(data['Insulin']<200),'F7']=1
    # f8
    data.loc[:,'F8']=0
    data.loc[(data['BloodPressure']<80),'F8']=1
    # f9
    data.loc[:,'F9']=0
    data.loc[(data['Pregnancies']<4) & (data['Pregnancies']!=0) ,'F9']=1
    # f10 , f11, f12
    data['F10'] = data['BMI'] * data['SkinThickness']
    data['F11'] =  data['Pregnancies'] / data['Age']
    data['F12'] = data['Age'] / data['Insulin']
    # f13
    data.loc[:,'F13']=0
    data.loc[(data['F10']<1034) ,'F13']=1
    #scaling input Data
    testing_data = data
    testing_data_x = testing_data.loc[:,].values
    testing_data_x_scaled = scaler_loaded.transform(testing_data_x)
    #final result
    result = rfc_loaded.predict(testing_data_x_scaled)[0]
    if result == 0 :
        result_string = "Non Diabetic"
    if result == 1 :
        result_string = "Diabetic"
    return result_string

class Prediction(Resource):
    def get(self):
        args = parser.parse_args()
        user_query = args['recieved_input']
        print('Recieved input...\n'+user_query)
        user_query = string_to_float_array(user_query)
        pred_result  = ml_predict(user_query)
        print('Response sent...\n'+pred_result)
        return (pred_result)

api.add_resource(Prediction, '/')

if __name__ == '__main__':
    app.run(debug=False)

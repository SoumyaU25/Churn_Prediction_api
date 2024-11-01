from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import pickle
import json


app = FastAPI()



app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChurnPrediction(BaseModel):
    gender: int
    age: int
    balance: int
    num_of_products: int
    is_active_member: int
    geo_germany:int
    geo_spain:int


# loading model 
prediction_model = pickle.load(open('churn_model.pkl','rb'))

@app.get('/')
def welcome():
    return "Hey welcome to this page. To view the model deployed you can visit the endpoint /predict/docs to check it."

@app.post('/predict')
def churn_prediction(input_parameters: ChurnPrediction):
    input_data = input_parameters.dict()
    input_list = [input_data[field] for field in input_data]
    
    prediction = prediction_model.predict([input_list])

    if prediction[0] == 0:
        return "The customer will exit the bank."
    else:
        return "The customer will stay with the bank."
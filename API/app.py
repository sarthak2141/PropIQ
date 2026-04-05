from fastapi import FastAPI,HTTPException
from fastapi.responses import JSONResponse
import  pandas as pd
import numpy as np
from API.Validator.Input_Validation import predict_IP_validation
from API.Components.price_prediction import price_prediction
app=FastAPI()
# <<══════════════════════════════════<< Routes >>════════════════════════════════>>

@app.get('/')
def home():
    return {"message":"House price prediction website"}
# <<══════════════════════════════════<< price prediction >>════════════════════════════════>>
@app.post('/predict')

def predict_price(pred_IP:predict_IP_validation):
    print(pred_IP)
    predict_input = {
    "property_type": pred_IP.property_Type,
    "sector": pred_IP.sector,
    "bedRoom": pred_IP.bedRooms,
    "bathroom": pred_IP.bathrooms,
    "balcony": pred_IP.balconies,
    "built_up_area": pred_IP.built_up_area,
    "servent room": pred_IP.servent_room,
    "store room": pred_IP.store_room,
    "floor_category": pred_IP.floor_category,
    "area_per_bedroom": pred_IP.area_per_bedroom
}
    try:
    # give one_df data to pipeline /model 
     prediction=price_prediction(predict_input)
     print(prediction)
     return JSONResponse(status_code=200,content={"price":float(prediction)})
    # return the predicted price
    except Exception as e:
       return JSONResponse(status_code=500,content={"error":str(e)})

    

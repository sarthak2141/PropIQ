import pickle
import pandas as pd
import logging
import os

logging.basicConfig(level=logging.INFO)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
model_path = os.path.join(BASE_DIR, "Models", "pipeline.pkl")

with open(model_path, "rb") as file:
    pridiction_model = pickle.load(file)

def price_prediction(user_ip):
    one_df = pd.DataFrame([user_ip])
    logging.info(f"\n{one_df}")
    logging.info(f"\n{one_df.dtypes}")
    prediction = pridiction_model.predict(one_df)
    return float(prediction[0])
# inference.py

import io
import uvicorn
import requests 
import numpy as np
import pandas as pd
from PIL import Image
import tensorflow as tf
from pydantic import BaseModel
import matplotlib.pyplot as plt
from load_model import load_model
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from tensorflow.keras.losses import cosine_similarity

# FILEPATH
WEIGHTS = {"location": 6, "description": 5}
MODEL_FILE = r"D:\CSES\AI\Projects\Natural Language Processing\Hackathons\Holiday Vacation Recommendation\files\my_model.keras"
WEIGHTS_FILE = r"D:\CSES\AI\Projects\Natural Language Processing\Hackathons\Holiday Vacation Recommendation\files\best_model.weights.h5"
ENCODED_FILE = r"D:\CSES\AI\Projects\Natural Language Processing\Hackathons\Holiday Vacation Recommendation\files\encoded_file.npy"
FILEPATH = r"D:\CSES\AI\Projects\Natural Language Processing\Hackathons\Holiday Vacation Recommendation\files\hackathons.xlsx"

holiday_vacation = pd.read_excel(FILEPATH, sheet_name = "Sheet1")
results = np.load(ENCODED_FILE)

# Load model
model = load_model(MODEL_FILE, WEIGHTS_FILE)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

class ModelInput(BaseModel):
    input_data: dict

@app.post("/predict")
async def perform_inference(inputs: ModelInput):
    continents = ["Asia", "Africa", "America", "Oceania", "Europe"]

    location_output, description_output = model(inputs.input_data)
    # Your scoring and result extraction code goes here...
    list_results = []
    for idx in range(len(results)):
        location_result, description_result = results[idx]
        
        location_score = -cosine_similarity(location_output, location_result)
        description_score = -cosine_similarity(description_output, description_result)

        location_data = inputs.input_data["location"]
        if (location_data == "Around the world" or location_data not in continents):
            score = description_score
        else:
            score = (location_score*WEIGHTS["location"] + description_score*WEIGHTS["description"]) / (WEIGHTS["location"] + WEIGHTS["description"])

        if (location_data == "Around the world" or location_data == holiday_vacation.loc[idx, "Nation"] or location_data in continents):
            list_results.append((score, idx))
        
    sorted_list_results = sorted(list_results, reverse=True)

    list_results = []
    for _, idx in sorted_list_results[:5]:
        data = holiday_vacation.loc[idx, ["Nation", "Location", "Image", "O_Description"]]

        list_results.append((f"{data.Location}  ({data.Nation}): {data.O_Description}", data.Image))
    return list_results
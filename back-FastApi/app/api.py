# api.py
from fastapi import APIRouter
from pydantic import BaseModel
import torch
import numpy as np
import joblib
from .model import CVAE 
from .utils import load_scaler  

router = APIRouter()  

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

input_dim = 4  
condition_dim = 1  
latent_dim = 4

model = CVAE(input_dim, condition_dim, latent_dim)
model.load_state_dict(torch.load("data/cvae_model.pth", map_location=torch.device('cpu'), weights_only=True))
model.eval()  
model = model.to(device)

scaler = joblib.load("data/scaler_data.pkl")

class SlidersInput(BaseModel):
    intensity: float 

@router.post("/generate-parameters/")
async def generate_parameters(sliders: SlidersInput):

    user_input = np.array([[0, sliders.intensity, 0, 0, 0]])  
    scaled_input = scaler.transform(user_input)
    
    intensity_scaled = torch.tensor(scaled_input[0, 1], dtype=torch.float32).reshape(1, -1).to(device)
    z = torch.randn(1, latent_dim).to(device)

    with torch.no_grad():
        generated_parameters = model.decode(z, intensity_scaled)

    
    scaled_data_partial = np.zeros((1, 5))
    scaled_data_partial[0, [0, 2, 3, 4]] = generated_parameters.cpu().numpy()[0]


    descaled_output = scaler.inverse_transform(scaled_data_partial)

    parameters = {
        "Temperature": float(descaled_output[0][0]),
        "Precipitation": float(sliders.intensity),  
        "WindSpeed": float(descaled_output[0][2]),
        "EmissionRate": float(descaled_output[0][3]),
        "HorizontalVelocity": float(descaled_output[0][4])
    }

    return {"generated_parameters": parameters}

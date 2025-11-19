import pickle
from pathlib import Path

# Set project root to the directory that contains this utils file
project_root = Path(__file__).resolve().parents[1]

# Create the model_path variable pointing to assets/model.pkl
model_path = project_root / "assets" / "model.pkl"

def load_model():
    with model_path.open('rb') as file:
        model = pickle.load(file)
    return model
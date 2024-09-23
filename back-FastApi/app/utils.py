import joblib

def load_scaler(filepath):
    return joblib.load(filepath)

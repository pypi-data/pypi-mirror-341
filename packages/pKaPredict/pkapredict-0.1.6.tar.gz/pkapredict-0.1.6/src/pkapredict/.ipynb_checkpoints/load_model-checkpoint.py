from pathlib import Path
import pickle
import importlib.resources as pkg_resources
import pkapredict.models  # Your actual package name here

def load_model():
    with pkg_resources.files(pkapredict.models).joinpath("best_pKa_model.pkl").open("rb") as f:
        model = pickle.load(f)
    print("✅ LGBMRegressor model successfully loaded!")
    return model
    
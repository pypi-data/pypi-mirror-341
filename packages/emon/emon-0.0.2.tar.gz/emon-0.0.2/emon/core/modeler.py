import joblib
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
import numpy as np
import os

def makemodel(output_path):
    from emon.core.trainer import model, X_train, y_train
    from emon.core.cleaner import label_encoder

    if model is None:
        raise RuntimeError("[emon.makemodel] Please run emon.train() before saving the model.")

    ext = os.path.splitext(output_path)[-1]

    if ext == ".joblib":
        joblib.dump(model, output_path)
        print(f"\n[emon.makemodel] Model saved to {output_path} (scikit-learn)")

    elif ext == ".h5":
        model.save(output_path)
        print(f"\n[emon.makemodel] Model saved to {output_path} (TensorFlow/Keras)")
    else:
        raise ValueError("[emon.makemodel] Unsupported file format. Use .h5 or .joblib")
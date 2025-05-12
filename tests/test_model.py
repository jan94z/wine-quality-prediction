import pickle
import numpy as np

def test_model_prediction():
    model_path = "/home/jan/wine-quality-prediction/models/rf.pkl"
    with open(model_path, "rb") as f:
        model = pickle.load(f)

    X_sample = np.array([[7.0, 0.27, 0.36, 20.7, 0.045,
                          45.0, 170.0, 1.001, 3.0, 0.45, 8.8]])
    pred = model.predict(X_sample)
    
    assert isinstance(pred[0], (int, np.integer))
    assert 0 <= pred[0] <= 10
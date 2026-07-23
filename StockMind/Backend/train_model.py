import numpy as np
import joblib
from sklearn.linear_model import LogisticRegression
import os

def build_model():
    x_train= np.array([
        # --- CLEAR BUY SETUPS ---
        [25,  0.8, 1],  
        [20,  0.9, 1],  
        [32,  0.4, 1], 
        
        # --- CLEAR SELL SETUPS ---
        [75, -0.7, 0],  
        [85, -0.9, 0],  
        [68, -0.3, 0],  
        
        # --- HOLD / NEUTRAL SETUPS ---
        [50,  0.0, 1], 
        [45,  0.1, 0], 
        [55, -0.1, 1],  
    ])
    y_train = np.array([1,1,1,-1,-1,-1,0,0,0])

    model=LogisticRegression(max_iter=1000)
    model.fit(x_train, y_train)

    current_dir= os.path.dirname(__file__)
    save_path = os.path.join(current_dir, "stockmind.joblib")

    joblib.dump(model,save_path)


if __name__ == "__main__":
    build_model()

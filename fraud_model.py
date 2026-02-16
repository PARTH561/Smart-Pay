import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

def train_fraud_model():
    # Create synthetic dataset (simulation)
    data = {
        "amount": [1000, 2000, 50000, 150000, 300000, 800, 120000, 6000, 250000, 4000],
        "device_change": [0, 0, 1, 1, 1, 0, 1, 0, 1, 0],
        "otp_failures": [0, 1, 2, 3, 4, 0, 2, 0, 3, 1],
        "fraud_flag": [0, 0, 0, 1, 1, 0, 1, 0, 1, 0]
    }

    df = pd.DataFrame(data)

    X = df[["amount", "device_change", "otp_failures"]]
    y = df["fraud_flag"]

    model = LogisticRegression()
    model.fit(X, y)

    return model

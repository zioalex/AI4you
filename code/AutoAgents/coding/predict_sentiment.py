import numpy as np
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score
import json

# Load sentiment data from JSON file
with open('big_training_data_with_crypto_date_sentiment.json', 'r') as f:
    sentiment_data = json.load(f)

# Preprocess data and extract features
X = []
y = []
crypto_names = []

# Mapping cryptocurrency names to unique labels
crypto_label_map = {}

for record in sentiment_data:
    X.append(record["sentiment"])
    crypto_name = record["crypto"]
    if crypto_name not in crypto_label_map:
        crypto_label_map[crypto_name] = len(crypto_label_map)
    y.append(crypto_label_map[crypto_name])
    crypto_names.append(crypto_name)

X = np.array(X)
y = np.array(y)

# Model training
model = SVC(kernel='linear')
model.fit(X, y)

# Model evaluation (optional)
y_pred = model.predict(X)
accuracy = accuracy_score(y, y_pred)
print("Model Accuracy:", accuracy)

# Prediction for the next days (example)
new_data = np.array([[55, 20, 25], [30, 25, 45]])  # Example sentiment data for the next days
predictions = model.predict(new_data)

print("Predictions for the next days:")
for pred, crypto_name in zip(predictions, crypto_names):
    print("Predicted sentiment label for {}:".format(crypto_name), pred)


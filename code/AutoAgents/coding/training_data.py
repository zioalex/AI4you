import json
import random
from datetime import datetime, timedelta

# Generate random sentiment data with crypto name, date, and sentiment
sentiment_data = []
cryptos = ["bitcoin", "ethereum"]

start_date = datetime(2023, 1, 1)
end_date = datetime(2023, 12, 31)

for _ in range(1000):
    crypto = random.choice(cryptos)
    positive = random.randint(0, 100)
    negative = random.randint(0, 100 - positive)
    neutral = 100 - positive - negative
    date = start_date + timedelta(days=random.randint(0, (end_date - start_date).days))
    sentiment_data.append({"crypto": crypto, "date": date.strftime('%Y-%m-%d'), "sentiment": [positive, negative, neutral]})

# Save sentiment data to JSON file
with open('big_training_data_with_crypto_date_sentiment.json', 'w') as f:
    json.dump(sentiment_data, f)

print("Big training data JSON file with crypto name, date, and sentiment created successfully.")


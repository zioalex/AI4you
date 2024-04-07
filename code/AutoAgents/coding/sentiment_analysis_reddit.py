import praw
from textblob import TextBlob

# Reddit API credentials
client_id = 'SuyKXGR2yorrzMqHtKIwqg'
client_secret = 'ZVF3wV73YkRhOnUKPAnpdbtca45Eew'
user_agent = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:123.0) Gecko/20100101 Firefox/123.0'

# Authenticate
reddit = praw.Reddit(client_id=client_id,
                     client_secret=client_secret,
                     user_agent=user_agent)

# Subreddit to search
subreddit = reddit.subreddit('cryptocurrency')

# Search for posts mentioning cryptocurrencies
posts = subreddit.search('Ethereum', limit=100)

# Analyze sentiment
positive = 0
negative = 0
neutral = 0

for post in posts:
    analysis = TextBlob(post.title)
    if analysis.sentiment.polarity > 0:
        positive += 1
    elif analysis.sentiment.polarity < 0:
        negative += 1
    else:
        neutral += 1

total = positive + negative + neutral

print("Sentiment Analysis of", total, "Reddit posts mentioning cryptocurrencies:")
print("Positive:", positive)
print("Negative:", negative)
print("Neutral:", neutral)

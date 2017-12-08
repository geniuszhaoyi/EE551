import pandas as pd
from textblob import TextBlob

data = pd.read_csv('/Users/enyaning/Desktop/BIA660/BIA660_TEAM_2/test.csv')

arr = []
for index, row in data.iterrows():
    blob = TextBlob(row['sentence'])
    arr.append({
        'phrase': row['phrase'],
        'polarity': blob.sentences[0].sentiment.polarity,
        'restaurantId': row['restaurantId'],
        'review_id': row['review_id'],
        'sentence_id': row['sentence_id'],
        'sentence': row['sentence']
    })

df = pd.DataFrame(arr)
df.to_csv('test_polarity.csv')

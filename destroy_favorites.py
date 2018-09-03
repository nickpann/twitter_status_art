import twitter
import json
import config

'''
Warning, this will destroy all of your favorites!
'''

api = twitter.Api(consumer_key = config.consumer_key,
                  consumer_secret = config.consumer_secret,
                  access_token_key = config.access_token_key,
                  access_token_secret = config.access_token_secret)

with open('status_logs/likes_data_dump.json') as data_file:
    likes = json.load(data_file)

count = 0
for like in likes:
    tweet_id = like['like']['tweetId']
    try:
        statuses = api.DestroyFavorite(status_id=tweet_id)
        count += 1
        print("Favorite destroyed.")

    except Exception as e:
        print(e)

print(count, "favorites destroyed.")

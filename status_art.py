# -*- coding: utf-8 -*-
import twitter
import json
import time
from PIL import Image, ImageDraw, ImageFont
import textwrap
import config

'''
The module I'm using is twitter-python (not to be confused with tweepy!)

Attribution
https://python-twitter.readthedocs.io/en/latest/twitter.html#twitter.api.Api.GetFavorites
'''
api = twitter.Api(consumer_key = config.consumer_key,
                  consumer_secret = config.consumer_secret,
                  access_token_key = config.access_token_key,
                  access_token_secret = config.access_token_key,
                  tweet_mode='extended') # Without this condition Tweets will be truncated

def main():
    draw_images()


'''
Returns 200 most recent favorites.
200 limit imposed by Twitter.
'''
def fetch_favorites_from_api():
    favorites = api.GetFavorites(screen_name="nickpann", count=200, return_json=True)
    ts = time.gmtime()
    formatted_ts = time.strftime("%Y_%m_%d %H:%M:%S", ts)
    with open('status_logs/200_recent_favorites ' + formatted_ts + '.json', 'w') as outfile:
        json.dump(favorites, outfile)


'''
Generate a list of IDs for favorited Tweets.
Enrich with statuses, screen names, etc.
Output to JSON.
'''
def fetch_favorites_from_dump():
    with open('status_logs/likes_data_dump.json') as data_file:
        likes = json.load(data_file)

    likes_list = []
    for like in likes:
        tweet_id = like['like']['tweetId']
        likes_list.append(tweet_id)

    try:
        statuses = api.GetStatuses(likes_list, map=True)
        s_list = [] # What we'll append JSON-serializable statuses to
        count = 0
        for status in statuses:
            status_object = statuses[status]
            # make a JSON serializble object
            if status_object is not None:
                s = {
                    "created_at": status_object.created_at,
                    "favorite_count": status_object.favorite_count,
                    "full_text": status_object.full_text,
                    "id": status_object.id,
                    # "media": status_object.media, # This is a TwitterModel
                    "retweet_count": status_object.retweet_count,
                    # "text": status_object.text, # Null when tweet_mode='extended' https://github.com/bear/python-twitter/issues/537
                    # "urls": status_object.urls, # This is a TwitterModel
                    "user_name": status_object.user.name,
                    "user_screen_name": status_object.user.screen_name
                }
                s_list.append(s)
                count += 1

        print(count, "statuses serialized.")
        ts = time.gmtime()
        formatted_ts = time.strftime("%Y_%m_%d %H:%M:%S", ts)
        with open('status_logs/favorites_enriched ' + formatted_ts + '.json', 'w') as outfile:
            json.dump(s_list, outfile)

    except Exception as e:
        print(e)


'''
Takes a JSON file.
'''
def draw_images():
    with open('status_logs/favorites.json') as data_file:
        statuses = json.load(data_file)

    count = 0
    for status in statuses:
        id = status["id"]
        full_text = status["full_text"]
        user_name = status["user_name"]
        make_image(id, full_text, user_name)
        count += 1
    print(count, "images created.")

'''
Outputs Twitter status art using Pillow module.

Attribution
https://code-maven.com/create-images-with-python-pil-pillow
https://stackoverflow.com/questions/8257147/wrap-text-in-pil
https://stackoverflow.com/questions/1166317/python-textwrap-library-how-to-preserve-line-breaks/1166367
'''
def make_image(status_id, status_full_text, status_user_name):

        img = Image.new('RGB', (800, 600), color = (226, 225, 221))
        font = ImageFont.truetype('/Library/Fonts/Menlo.ttc', 32)
        draw = ImageDraw.Draw(img)
        margin = offset = 40

        status_body = '\n'.join(['\n'.join(textwrap.wrap(line, width=35,
                         break_long_words=False, replace_whitespace=False))
                         for line in status_full_text.splitlines() if line.strip() != ''])

        status_body += "\n\n  - " + status_user_name
        draw.text((margin, offset), status_body, font=font, fill=(31,30,28))
        img.save("status_images/" + str(status_id) + ".png")


main()

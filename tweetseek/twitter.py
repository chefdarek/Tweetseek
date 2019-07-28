"""Retrieve Tweets, embeddings, and persist the database
    to add new user call new_user()
    to get user information or "status" at Flask shell >>> twitter_user = TWITTER.get_user('Austen')
    twitter_user
    to get user tweets tweets = twitter_user.timeline()
    limit is 200 and default is 20 tweets
    to get specific tweets tweets[0].text shows the first sent back
    params to get tweets -----
        tweets = twitter_user.timeline(count=200,
        exclude_replies=True, include_rts=False, tweet_mode='extended')
        must use tweet[0].full_text to get results after
    extended tweet mode means more than 140 or 280 character limit

    tweets[0].created_at
    returns ---> datetime.datetime(2019, 7, 24, 4, 16, 51)

    to get actually Twitter assigned i.d.'s >>> tweets[0].id
                                                1153881708145463297
    to get embeddings from Basilica >>> tweet_text = tweets[0].full_text
                                    #>>> embedding = BASILICA.embed_sentence(
                                                    tweet_text, model='twitter')
    RETURNS embeddings of words from API in a python list
"""

import tweepy
import basilica
from decouple import config
from .models import DB, Tweet, User

#  pass in the config from .env for authenticate
TWITTER_AUTH = tweepy.OAuthHandler(config('TWITTER_CONSUMER_KEY'),
                                   config('TWITTER_CONSUMER_SECRET'))

TWITTER_AUTH.set_access_token(config('TWITTER_ACCESS_TOKEN'),
                              config('TWITTER_ACCESS_SECRET'))
TWITTER = tweepy.API(TWITTER_AUTH)

#  https://www.basilica.ai/
BASILICA = basilica.Connection(config('BASILICA_KEY'))

"""Script file of various functions"""


def new_set_pull_bed(handle, count=200):
    """Creates a new user and grabs 200 tweets, embeddings"""

    twitter_user = TWITTER.get_user(handle)
    tweets = twitter_user.timeline(
        count=count, exclude_replies=True,
        include_rts=False, tweet_mode='extended')
    db_user = User(id=twitter_user.id, name=twitter_user.screen_name,
                   newest_tweet_id=tweets[0].id)
    for tweet in tweets:
        embedding = BASILICA.embed_sentence(tweet.full_text, model='twitter')
        db_tweet = Tweet(id=tweet.id, text=tweet.full_text[:500], embedding=embedding)
        DB.session.add(db_tweet)
        db_user.tweets.append(db_tweet)

    if tweets:
        # this will update the newest tweet id or not if none
        db_user.newest_tweet_id = tweets[0].id

    DB.session.add(db_user)
    DB.session.commit()

    print(f"{handle} was put in the Database, with {count} tweets and embedded")

# def add_or_update_user(username):
#     """for the html request add or update err if no or private user"""
#     try:
#         twitter_user = TWITTER.get_user(username) #  API queries to database
#         db_user = (User.query.get(twitter_user.id))  #  API Query to see if they exist
#         DB.session.add(db_user)
#         #  want as many recent non-retweet/reply statuses
#         tweets = twitter_user.timeline(
#             count=200, exclude_replies=True, include_rts=False,
#             tweet_mode='extended', since_id=db_user.newest_tweet_id)
#
#         if tweets:
#             # this will update the newest tweet id or not if none
#             db_user.newest_tweet_id = tweets[0].id
#         for tweet in tweets:
#             #  get embedding for tweet and store in db
#             embedding = BASILICA.embed_sentence(tweet.full_text,
#                                                 model='twitter')
#             db_tweet = Tweet(id=tweet.id, text=tweet.full_text[:500],
#                              embedding=embedding)
#             db_user.tweets.append(db_tweet)
#             DB.session.add(db_tweet)
#             DB.session.commit()
#     except Exception as e:
#         print('Error processing {}: {}'.format(username, e))
#         raise e
#     else:
#         DB.session.commit()

def new_user():
    """prompt to run Q&A for DB user entry"""
    answer = input ("Would you like to add a new user: y or n? ")

    answer = str(answer.lower())

    if answer == "y":
        handle = str(input("What is the Twitter handle?:"))
        count = int(input("Tweet count (default=200):"))
        return new_set_pull_bed(handle, count)

    if answer == "n":
        print("Okay, if you would like to add a new user new_set_pull_bed(handle, count=200)")

# TODO write some more useful functions



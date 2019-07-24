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
        DB.session.add(db.tweet)
        db_user.tweets.append(db_tweet)

    DB.session.add(db_user)
    DB.session.commit()

    print(f"{handle} was put in the Database, with {count} tweets and embedded")


answer = input ("Would you like to add a new user: y or n? ")

answer = str(answer.lower())

if answer == "y":
    handle = str(input("What is the Twitter handle?:   "))
    count = int(input("Tweet count (default=200):  "))
    new_set_pull_bed(handle, count)

if answer == "n":
    print("Okay, if you would like to add a new user new_set_pull_bed(handle, count=200)")




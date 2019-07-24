"""SQL Alchemy Models for Flask"""

from flask_sqlalchemy import SQLAlchemy


DB = SQLAlchemy()


class User(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    name = DB.Column(DB.String(15), nullable=False)
    #  adding this will make sure you can target newest tweet of user
    newest_tweet_id = DB.Column(DB.BigInteger)

    def __repr__(self):
        """Returns and identified user Name object and content of the object"""

        return '<User {}>'.format(self.name)


class Tweet(DB.Model):
    """Tweets"""

    #  change to Big bc twitter id are long
    id = DB.Column(DB.BigInteger, primary_key=True)

    # increase up to 500 to accommodate without truncating
    text = DB.Column(DB.Unicode(500))

    #  to save the embeddings we need a blob
    #  (holds images too) good for serializing, SQLAlchemy they are PickleTypes
    embedding = DB.Column(DB.PickleType, nullable=False)

    user_id = DB.Column(DB.BigInteger, DB.ForeignKey('user.id'), nullable=False)
    user = DB.relationship('User', backref=DB.backref('tweets'), lazy=True)

    def __repr__(self):
        """Returns and identified Tweet object and content of the object"""

        return '<Tweet {}>'.format(self.text)

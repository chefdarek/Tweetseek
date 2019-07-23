"""SQL Alchemy Models for Flask"""

from flask_sqlalchemy import SQLalchemy

DB = SQLAlchemy()

class User(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    name = DB.Column(DB.String(15), nullable=False)

class Tweet(DB.Model):
    """Tweets"""
    id = DB.Column(DB.Integer, primary_key=True)
    text  DB.Column(DB.Unicode(280))



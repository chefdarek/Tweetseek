from decouple import config
from flask import Flask, render_template, request
from .models import *
from .twitter import *


def create_app():
    """Create and configure an instance of the Flask application"""
    app = Flask(__name__)
    #  connects the database to the flask instance
    #  if the schema is changed you loose the data and have
    #  to re-instantiate it
    #  after the code is added below you must go to the flask shell in
    #  the Tweetseek/tweetseek folder run flask shell
    #  from tweetseek.models import * then add the data as variables

    app.config['SQLALCHEMY_DATABASE_URI'] = config('DATABASE_URL')
    #  gives err message codes and will update on the fly

    #  gives err message codes and will update off

    app.config['SQLALCHEMY_TRACK_NOTIFICATIONS'] = False
    DB.init_app(app)

    #  app.route determines the page to route to after "/"

    @app.route("/")
    def preds():
        """creates a list of users from the SQLDB and renders the home.html template."""
        users = User.query.all()

        return render_template("home.html", title='Home', users=users)

    @app.route("/about")
    def about():
        """creates a list of users from the SQLDB and renders renders the about.html page."""

        users = User.query.all()  # DB query for SQL

        return render_template("about.html", title='About', users=users)

    @app.route("/reset")
    def reset():
        """Drop all tables and create all new tables to clear Data base"""
        DB.drop_all()
        DB.create_all()
        return render_template('home.html', title='DB Reset!', users=[])

    @app.route("/user", methods=['POST'])
    @app.route("/user<name>", methods=['GET'])
    def user(name=None):
        message = ''
        thisone = request.values['user_name']
        try:
            if request.method == 'POST':
                new_set_pull_bed(thisone)
                message = 'User {} successfully added'.format(thisone)
            tweets = User.query.filter(User.name == thisone).tweets
            #import pdb;
            #pdb.set_trace()  # sets the  python debugger

        except Exception as e:
            message = 'Error adding {}:{}'.format(thisone, e)
            tweets = []
        return render_template('user.html', title=thisone, tweets=tweets, message=message)

    return app

    #  Todo should add a login decorator over reset route for authorization of admin user to use function
    #  When it is run again the first time after change here you will have to use the reset route and will lose data

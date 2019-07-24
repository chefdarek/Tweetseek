from flask import Flask, render_template #request
from .models import DB, User

def create_app():
    """Create and configure an instance of the Flask application"""
    app = Flask(__name__)
    #connects the database to the flask instance
    #if the schema is changed you loose the data and have
    #to re-instantiate it
    #after the code is added below you must go to the flask shell in
    #the Tweetseek/tweetseek folder run flask shell
    #from tweetseek.models import * then add the data as variables

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
    DB.init_app(app)

    #app.route determines the page to route to after "/"
    #@app.route('/')
    #def root():
        #"""render templates autolooks in the template folder."""
        #users = User.query.all()

        #return render_template("templates.html", title='Home', users=users)

    @app.route("/")
    def preds():
        """render the home.html template."""
        users = User.query.all()

        return render_template("home.html", title='Home', users=users)

    @app.route("/about")
    def about():
        """render the about.html page."""

        users = User.query.all()

        return render_template("about.html", title='About', users=users)

    return app




#if __name__ == "__main__":
 #   app.run(debug=True)



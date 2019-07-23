from flask import Flask, render_template

def create_app():
    """ Create and configure an instance of the Flask application"""
    app = Flask(__name__)

    #app.route determines the page to route to after "/"
    @app.route('/')
    def root():
        """render templates autolooks in the template folder"""

        return render_template("home.html")
    
        return app

    #@app.route("/templates")
    #def preds():
        #""" render the home.html template """
        #return render_template("home.html")

    #@app.route("/about")
    #def about():
        """ render the about.html page """

        #return render_template("about.html")

#if __name__ == "__main__":
 #   app.run(debug=True)



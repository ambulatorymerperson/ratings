"""Movie Ratings."""

from jinja2 import StrictUndefined

from flask import (Flask, render_template, redirect, request, flash,
                   session, copy_current_request_context)
from flask_debugtoolbar import DebugToolbarExtension

from model import User, Rating, Movie, connect_to_db, db


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails
# silently. This is horrible. Fix this so that, instead, it raises an
# error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""
    return render_template("homepage.html")


@app.route("/users")
def user_list():
    """Show list of users"""

    users = User.query.all()
    return render_template("user_list.html", users=users)

@app.route("/register", methods=["GET"])
def register_form():
    """Registration Form."""


    return render_template("register_form.html")

@app.route("/register", methods=["POST"])
def register_process():
    """Registration Form."""

    email_input = request.form['email_input']
    pw_input = request.form['pw_input']

    if User.query.filter_by(email = email_input).all() != []:
        return redirect('/')       
    else:
        new_user = User(email= email_input, password=pw_input)
        db.session.add(new_user)
        db.session.commit() 

    return redirect('/')

@app.route("/login", methods=["GET"])
def login_form():
    """Show login form"""

    return render_template("log_in.html")


@app.route("/login", methods=["POST"])
def login():
#    @copy_current_request_context
 #   def more_login():
    email_input = request.form['email_input']
    pw_input = request.form['pw_input']

    if User.query.filter(User.email == email_input, User.password == pw_input).all() != []:
        session['current_user'] = email_input
        print session['current_user']
        flash('You were successfully logged in')
        return redirect("/")
    else:
        flash('Your e-mail or password was incorrect! Please try again or Register.')
        return render_template("log_in.html")

@app.route("/user_info/<user_id>", methods=["GET"])
def show_info():
    # user_name = User.query.filter_by(user_id=)
    # age =
    # zipcode =
    # movies =
    # scores =

    return render_template("log_in.html", user_name=user_name, age=age, zipcode=zipcode, movies=movies, scores = scores)



@app.route("/logout")
def logout():
    del session['current_user']


    flash('Byyyyyyyyyyyyyyyyyyyyyyyyyyyye. You have been succesfully logged out!')
    return redirect ("/login")






if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    # make sure templates, etc. are not cached in debug mode
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')

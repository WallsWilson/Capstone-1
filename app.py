import os
from flask import Flask, redirect, render_template, g, session, flash,request,abort
from models import db, connect_db, User, Drinks
from form import UserAddForm, LoginFrom, DrinkAddForm
from sqlalchemy.exc import IntegrityError
import requests



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///booze_app'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'secret_key'
app.config['WTF_CSRF_ENABLED'] = True


CURR_USER_KEY = "curr_user"

api_key = '/ttTpCoqYCC4Og/ew8jM0A==Wy5XuBs2mz8erLBx'
COCKTAIL_API = 'https://api.api-ninjas.com/v1/cocktail?name='

connect_db(app)

@app.before_request
def add_user_to_g():
    """If we're logged in, add curr user to Flask global."""

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])

    else:
        g.user = None


def do_login(user):
    """Log in user."""

    session[CURR_USER_KEY] = user.id


def do_logout():
    """Logout user."""

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]

# Base pages
@app.route('/', methods=['GET'])
def index():
    return render_template('form.html')


@app.route('/search', methods=['POST'])
def search():

    """Search from the API to retrive a drinks name, recipe, and ingreidnets. Also allows you to search using specific ingredients. Ex. Vodka"""

    name = request.form['name']
    ingredients = request.form['ingredients']


    url = 'https://api.api-ninjas.com/v1/cocktail?'
    if name:
        url += f'name={name}&'
    if ingredients:
        url += f'ingredients={ingredients}&'
    
    headers = {'X-Api-Key': '/ttTpCoqYCC4Og/ew8jM0A==Wy5XuBs2mz8erLBx'}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        return render_template('results.html', data=data)
    else:
        return 'Error'

    
# Fav Drink routes
    
@app.route('/users/<int:id>/favorites', methods=["GET"])
def favorites_list(id):
    """Show a list of liked drinks by the user."""

    if not g.user:
        flash("Please log in to view favorites.", "Danger")
        return redirect("/")
    
    user = User.query.get_or_404(id)
    return render_template("favorites/favorites.html", user=user, favs=user.favs)

@app.route('/drink/<int:drink_id>/fav', methods=["POST"])
def add_fav(drink_id):
    """Add a drink to favs list for the currently-logged-in user."""

    if not g.user:
        flash("Please log in to view favorites.", "Danger")
        return redirect("/")
     
    faved_drink = Drinks.query.get_or_404(drink_id)
    if faved_drink.user_id == g.user.id:
        return abort(403)
    
    user_favs = g.user.favs

    if faved_drink in user_favs:
        g.user.favs = [fav for fav in user_favs if fav != faved_drink]
    else:
        g.user.favs.append(faved_drink)
    
    db.session.commit()

    return redirect("/")
    

# Drink Recipe routes

@app.route('/drink/<int:drink_id>', methods=['GET'])
def drink_show(drink_id):
    """Store the drink and giving it a drink_id for the database."""

    drk = Drinks.query.get_or_404(drink_id)
    return render_template('drink/show.html', drinks = drk)

@app.route('/drink/<int:drink_id>/remove', methods=["POST"])
def remove_drink(drink_id):
    """Removing drink from the favs. """

    if not g.user:
        flash("Please log in to remove a drink.", "Danger")
        return redirect('/')
    
    drk = Drinks.query.get_or_404(drink_id)
    if drk.user_id != g.user.id:
        flash("Access not allowed.", "danger")
        return redirect('/')
    
    db.session.delete(drk)
    db.session.commit()

    return redirect(f'/users/{g.user.id}')


# User signup/login/logout

@app.route('/signup', methods=["GET", "POST"])
def signup():
    """Handle user signup.

    Create new user and add to DB. Redirect to home page.

    If form not valid, present form.

    If the there already is a user with that username: flash message
    and re-present form.
    """
    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]
    form = UserAddForm()

    if form.validate_on_submit():
        try:
            user = User.signup(
                username=form.username.data,
                password=form.password.data
            )
            db.session.commit()

        except IntegrityError as e:
            flash("Username already taken", 'danger')
            return render_template('signup.html', form=form)

        do_login(user)

        return redirect("/")

    else:
        return render_template('signup.html', form=form)
    

@app.route('/login', methods=["GET", "POST"])
def login():
    """Handle user login."""

    form = LoginFrom()

    if form.validate_on_submit():
        user = User.authenticate(form.username.data, form.password.data)

        if user:
            do_login(user)
            flash(f"Hello, {user.username}!", "success")
            return redirect("/")

        flash("Invalid. Remeber your password is 6 charachters or mmore.", 'danger')

    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    """Handle logout of user."""

    do_logout()

    flash("The party is not over!", 'success')
    return redirect("/login")



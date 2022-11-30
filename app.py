# Nathan Laney, Kaitlyn Finberg, Sumi Verma, Tyler Minnis, Honna Sammos
from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, session
from flask_bcrypt import Bcrypt
import os
from models import db
from src.models.user import User
from werkzeug.utils import secure_filename
from src.models.game import game 
from src.repositories.game_repository import game_repository_singleton


# Imports for our database tables. These are in a specific order, 
# to correctly populate the foreign keys. 
# Having these imports allows for them to be created on flask run
# if they do not already exist
from src.models.user_data import user_data
from src.models.game import game
from src.models.tag import tag
from src.models.tag_game import tag_game
from src.models.review import review
from src.models.user_favorites import user_favorites
from src.models.game_review import game_review


load_dotenv()
app = Flask(__name__)

print(os.getenv('SQLALCHEMY_DATABASE_URI'))
# postgresql://username:password@host:port/database_name
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
app.secret_key = os.getenv('APP_SECRET_KEY')

db.init_app(app)
bcrypt = Bcrypt(app)

# Creates tables that do not exist
with app.app_context():
    db.create_all()

page_index = {
    1:   "index",
    2:   "about",
    3:   "all_games",
    4:   "search",
    5:   "other"
}

current_page = "index"


@app.get('/')
def index():
    current_page = "index"
    return render_template('index.html')


@app.route('/header')
def header():
    current_page = "index"
    return render_template('index.html')


@app.get('/about')
def about():
    current_page = "about"
    return render_template('about.html')


@app.get('/search')
def search():
    q = request.args.get('q', '')
    current_page = "search"
    # this isn't working -> need to also set it up w/ correct database
    # title = game_repository_singleton.get_game_by_title(title = q) 
    return render_template('search.html', search_query=q)

@app.get('/all_games')
def all_games():
    current_page = "all_games"
    return render_template('all_games.html')

#kaitlyn is doing things and crying while dylan watches and judges 
@app.get('/profile')
def profile():
    current_page = "profile"
    #TODO: get the current session user STATUS: Done
    current_user = User.query.filter_by(user_id=session['user']['user_id']).first()
    #print(current_user.username)
    #TODO: If the user isnt logged in, dont let them go to the profile page STATUS: Almost Complete
    #getting a Key Error
    return render_template('profile.html', current_user=current_user, profile_path=session['user']['profile_path'])


@app.get('/post_review')
def post_review():
    current_page = "post_review"
    return render_template('post_review.html')


@app.get('/gamepage')
def gamepage():
    current_page = "gamepage"
    return render_template('gamepage.html')

# This is the start of the login in logic


@app.get('/login')
def login():
    current_page = "login"
    return render_template('login.html')


@app.post('/login')
def loginform():
    password = request.form.get('password')
    email = request.form.get('email')
    print(email)
    print(password)

    existing_user = user_data.query.filter_by(email=email).first()

    if not existing_user:
        return redirect('/login')

    #if not bcrypt.check_password_hash(existing_user.password, password):
        #return redirect('/login')

    session['user'] = {
        'user_id': existing_user.user_id,
        'profile_path': existing_user.profile_path
    }
    return redirect('/youGotIn')
# this is a post... you might have to make a get so that the page will load.....


@app.get('/youGotIn')
def temp():
    return render_template('youGotIn.html')


@app.get('/register')
def register():
    current_page = "register"
    return render_template('register.html')

#found some errors in register. login should work fine when these are fixed
@app.post('/register')
def registerForm():
    #username resturning null
    user_id = request.form.get('user_id')
    username = request.form.get('user_name')
    password = request.form.get('password')
    first_name = request.form.get('first_name')
    email = request.form.get('email')
    existing_user = user_data.query.filter_by(username=username).first()
    existing_email = user_data.query.filter_by(email=email).first()

    if (existing_email and existing_user):
        return redirect('/login')

    bcryptRounds = int(os.getenv('BCRYPT_ROUNDS'))
    if bcryptRounds == 'None':
        print("Defaulting bcryptRounds (error)")
        #bcrypt rounds are too high
        bcryptRounds = 20000 # If bcrypt rounds is not found, falls back to default value of 20k

    print(password)
    print(bcryptRounds)
    #rounds caused this to fail
    hashed_bytes = bcrypt.generate_password_hash(
        password, bcryptRounds)
    hashed_password = hashed_bytes.decode('utf-8')

    #Kaitlyn- Save the profile picture 
    if 'profile' not in request.files:
        return redirect('/')

    profile_picture = request.files['profile']

    if profile_picture.filename == '':
        return redirect('/')
    
    if profile_picture.filename.rsplit('.', 1)[1].lower() not in ['jpg', 'jpeg', 'png', 'gif']:
        return redirect('/')

    safe_filename = secure_filename(f'{user_id}-{profile_picture.filename}')

    profile_picture.save(os.path.join('static', 'profile-pics', safe_filename))

    #added username=username, password=hashed_password, etc bc it wouldnt work without it
    new_user = User(username=username, password=hashed_password, first_name=first_name, email=email, profile_path=safe_filename)

    db.session.add(new_user)
    db.session.commit()
    return redirect('/login')


@app.get('/resetPassword')
def resetPassword():
    current_page = "resetPassword"
    return render_template('resetPassword.html')


@app.post('/logout')
def logout():
    session.pop('user')
    return redirect('/')


if __name__ == '__main__':
    app.run()

#@app.get('/secret')

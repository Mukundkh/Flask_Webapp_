from datetime import datetime
from flask import Flask, render_template, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from forms import UserLoginForm, UserRegistrationForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'a554b3ef67376e97e2a6f9204e59a258'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.username}','{self.email}','{self.image}')"

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    on_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
     

    def __repr__(self):
        return f"Post('{self.title}','{self.on_date}')"




posts = [
    {
    'author' : 'Mukund',
    'title' : 'Blog1',
    'content' : 'Java Programming',
    'date' : '2-Sept-2021',
    },
    {
     'author' : 'Aman',
    'title' : 'Blog2',
    'content' : 'Python Programming',
    'date' : '2-October-2021',   
    }
]

@app.route("/")

@app.route("/home")

def home():
    return render_template('home.html', posts=posts, title='home')

@app.route("/about")

def about():
    return render_template('about.html')

@app.route("/register", methods=['GET', 'POST'])

def register():
    form = UserRegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)

@app.route("/login")
def login():
    form = UserLoginForm()
    return render_template('login.html', title='Login', form=form)

if __name__== "__main__":
    app.run(debug=True)

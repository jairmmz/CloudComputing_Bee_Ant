from flask import Flask, render_template, flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)

# Add database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'

# Secret key
app.config['SECRET_KEY'] = 'My super secret that no one is supposed to know'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initializa the database
db = SQLAlchemy(app)


# Create Model
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
   # Create a String
    def __repr__(self):
        return '<Name %r>' % self.name



# CREATE FORM CLASS
class NameForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = SubmitField('Email', validators=[DataRequired()])
    submit = SubmitField('Submit')

# CREATE FORM CLASS
class NameForm(FlaskForm):
    name = StringField("What's your name", validators=[DataRequired()])
    submit = SubmitField('Submit')


@app.route('/')
def index():
    first_name = 'Jairo'
    flash("Welcome To Our Website!")
    stuff = 'This is bold text'
    favorite_pizzas = ['Peperoni', 'Queso', 'Italiana', 41]
    return render_template("index.html",
                           first_name=first_name, stuff=stuff, favorite_pizzas=favorite_pizzas)

# Create User Page


@app.route('/user/<name>')
def user(name):
    # <h1>Hello {} </h1>'.format(name)
    return render_template('user.html', user_name=name)

# Create User Page


@app.route('/name', methods=['GET', 'POST'])
def name():
    name = None
    form = NameForm()
    # Validate Form
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ''
        flash("From Submitted Successfully!")
    return render_template('name.html', name=name, form=form)


# Invalid URL
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

# INTERNAL SERVER ERROR


@app.errorhandler(500)
def page_not_found(e):
    return render_template('500.html'), 500


# Recargar automática para el server.
if __name__ == '__main__':
    app.run(debug=True)

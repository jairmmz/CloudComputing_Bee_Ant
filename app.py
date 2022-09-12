from urllib import request
from flask import Flask, render_template, flash, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)

# Add database
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/users'

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
class UserForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    submit = SubmitField('Submit')

# CREATE FORM CLASS
class NameForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
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
    return render_template("index.html", first_name=first_name, stuff=stuff, favorite_pizzas=favorite_pizzas)

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

# Create Add User
@app.route('/user/add', methods=['GET', 'POST'])
def add_user():
    name = None
    form = UserForm()
    # Validate Form
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user is None:
            user = Users(name=form.name.data, email=form.email.data)
            db.session.add(user)
            db.session.commit()
        name = form.name.data
        form.name.data = ''
        form.email.data = ''
        flash("User Added Succesfully!")
    our_users = Users.query.order_by(Users.date_added)
    return render_template('add_user.html', form=form, name=name, our_users=our_users)

# Update User
@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update_user(id):
    form = UserForm()
    name_update = Users.query.get_or_404(id)
    if request.method == "POST":
        name_update.name = request.form['name']
        name_update.email = request.form['email']
        try:
            db.session.commit()
            flash("User updated successfully!")
            return render_template('update_user.html', form=form, name_update=name_update)
        except:
            flash("Error! in update user!")
            return render_template('update_user.html', form=form, name_update=name_update)
    else:
        return render_template('update_user.html', form=form, name_update=name_update)

# Delete User
@app.route('/delete/<int:id>')
def delete_user(id):
    user_delete = Users.query.get_or_404(id)
    name = None
    form = UserForm()
    try:
        db.session.delete(user_delete)
        db.session.commit()
        flash("User deleted successfully!")

        our_users = Users.query.order_by(Users.date_added)
        return render_template('add_user.html', form=form, name=name, our_users=our_users)

    except:
        flash("Ops! There was a problem from deleted User!")
        return render_template('add_user.html', form=form, name=name, our_users=our_users)

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

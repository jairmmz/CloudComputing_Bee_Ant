from flask import Flask, render_template, flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


app = Flask(__name__)
app.config['SECRET_KEY'] = 'My super secret that no one is supposed to know'

# CREATE FORM CLASS
class NameForm(FlaskForm):
    name = StringField("What's your name", validators=[DataRequired()])
    submit = SubmitField('Submit')


@app.route('/')
def index():
    first_name = 'Jairo'
    flash("Welcome To Our Website!")
    stuff='This is bold text'
    favorite_pizzas = ['Peperoni', 'Queso', 'Italiana', 41]
    return render_template("index.html",
    first_name=first_name, stuff=stuff, favorite_pizzas=favorite_pizzas)

#Create User Page
@app.route('/user/<name>')
def user(name):
    # <h1>Hello {} </h1>'.format(name)
    return render_template('user.html', user_name=name)

#Create User Page
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







#Invalid URL
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

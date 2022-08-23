from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


app=Flask(__name__)
app.config['SECRET_KEY']='My super secret that no one is supposed to know'

#CREATE FORM CLASS

class NameForm(FlaskForm):
    name=StringField("What's your name", validators=[DataRequired()])
    submit=SubmitField('Submit')

@app.route('/')
def index():
    first_name='Jairo no trabajo en su casa.'
    favorite_pizzas = ['Peperoni','Queso','Italiana',41]
    return render_template("name.html",
    first_name=first_name, favorite_pizzas=favorite_pizzas)

@app.route('/user/<name>')
def user(name):
    #<h1>Hello {} </h1>'.format(name)
    return render_template('user.html', user_name=name) 

@app.route('/name', methods=['GET', 'POST'])
def name():
    name=None
    form=NameForm()
    #Validate Form
    if form.validate_on_submit():
        name=form.name.data
        form.name.data=''

    return render_template('name.html', name=name, form=form)


    
#Recargar automática para el server.
if __name__ == '__main__':
    app.run(debug=True)

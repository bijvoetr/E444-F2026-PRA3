from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email
from flask import Flask, render_template, session, redirect, url_for

class NameForm(FlaskForm):
    name = StringField(
        'What is your name?',
        validators=[DataRequired()]
    )
    email = StringField(
        'What is your email?',
        validators=[DataRequired(), Email()]
    )
    submit = SubmitField('Submit')


app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'
bootstrap = Bootstrap(app)
moment = Moment(app)


from flask import Flask, render_template, session, redirect, url_for, flash

@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        old_name = session.get('name')
        if old_name is not None and old_name != form.name.data:
            flash('Looks like you have changed your name!')
        session['name'] = form.name.data
        if "utoronto" in form.email.data:
            session['email'] = form.email.data
            return redirect(url_for('chatbot'))
        else:
            flash('Please enter a valid UofT email address.')
        return redirect(url_for('index'))
    return render_template('index.html',
        form = form, name = session.get('name'), email = session.get('email'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/chatbot')
def chatbot():
    return render_template('chat.html')

@app.route('/user/<name>')
def user(name):
    return render_template(
        'user.html',
        name=name,
        current_time=datetime.utcnow()
    )

@app.route("/chat", methods=["POST"])
def chat():
    message = request.json["message"]

    # else:
    #     reply = "I don't understand."
    if "hello" in message.lower():
        reply = "Hello!"
    elif "my name is" in message.lower():
        session['chatName'] = message[message.lower().find("my name is") + len("my name is"):].strip()
        reply = f"Nice to meet you, {session['chatName']}!"
    elif "what is my name" in message.lower():
        if 'chatName' in session:
            reply = f"Your name is {session['chatName']}."
        else:
            reply = "I don't know your name yet."
    else:
        reply = "I don't understand."

    return {"reply": reply}
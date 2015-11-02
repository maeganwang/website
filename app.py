from flask import Flask, redirect, render_template, request, url_for
from flask_mail import Mail
from flask.ext.mail import Message
import json
import os

app = Flask(__name__)
app.config.from_pyfile('config.py')
mail = Mail(app)
data = {}

from config import SECRET_KEY
from forms import ContactForm

# import data from relevant JSON
def load_data():
    global data
    for name, path in app.config['DATA_FILENAMES'].iteritems():
        path = os.path.join(os.path.dirname(__file__), path)
        with open(path, 'r') as data_file:
            data[name] = json.loads(data_file.read())

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/events')
def events():
    return render_template('events.html')

@app.route('/initiatives')
def initiatives():
    return render_template('initiatives.html', **data['initiatives'])

@app.route('/jade')
def jade():
    return render_template('jade.html')

@app.route('/infographic')
def infographic():
    return render_template('infographic.html')

@app.route('/team')
def team():
    return render_template('team.html', **data['team'])

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        print form.email.data
        msg = Message(form.subject.data,
                    recipients=[(form.name.data, form.email.data),
                                ('CORE Board', 'coreboard@columbia.edu')])
        msg.body = form.message.data
        mail.send(msg)
        return redirect(url_for('index'))
    return render_template('contact.html', form=form)

load_data()

if __name__ == '__main__':
    app.run(debug = True, host='0.0.0.0', port=5000)

application = app
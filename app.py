from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import math

app = Flask(__name__)

ENV = 'prod'

if ENV == 'prod':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://ecejchfpejyxnv:6433310403f5c2a229d27a3642f2adc7d395aff86c71d992c0997e660403f3b2@ec2-54-158-1-189.compute-1.amazonaws.com:5432/dce89pnoivkfem'
else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = ''

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Feedback(db.Model):
    __tablename__ = 'feedback'
    id = db.Column(db.Integer, primary_key=True)
    customer = db.Column(db.String(200), unique=True)
    dealer = db.Column(db.String(200))
    rating = db.Column(db.Integer)
    comments = db.Column(db.Text())

    def __init__(self, customer, dealer, rating, comments):
        self.customer = customer
        self.dealer = dealer
        self.rating = rating
        self.comments = comments


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        customer = request.form['customer']
        dealer = request.form['dealer']
        rating = request.form['rating']
        comments = request.form['comments']
        data = Feedback(customer, dealer, rating, comments)
        db.session.add(data)
        db.session.commit()
        return render_template('success.html')
    return render_template('index.html', message='Sorry')
@app.route('/viewfeedback', methods=['GET','POST'])
def viewfeedback():
    posts = Feedback.query.filter_by().all()
    return render_template('feedback.html',posts=posts)


if __name__ == '__main__':
    app.run()

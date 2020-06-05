from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import datetime
import psycopg2, os

app = Flask(__name__)

DATABASE_URL = os.environ['DATABASE_URL']

conn = psycopg2.connect(DATABASE_URL, sslmode='require')

app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL

# app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:user@localhost:5432/cougardb"  
 #postgresql+psycopg2://user:password@hostname/database_name'


db = SQLAlchemy(app)
migrate = Migrate(app, db)


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String())
    phoneNumber = db.Column(db.String())
    typeOfUser = db.Column(db.String())
    code = db.Column(db.Integer())

    def __init__(self, firstName, phoneNumber, typeOfUser, code):
        self.firstName = firstName
        self.phoneNumber = phoneNumber
        self.typeOfUser = typeOfUser
        self.code = code

    def __repr__(self):
        return f"<User {self.firstName}>"


class RideRequest(db.Model):
    __tablename__ = 'riderequests'

    id = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String())
    phoneNumber = db.Column(db.String())
    currentLocation = db.Column(db.String())
    destination = db.Column(db.String())
    date = db.Column(db.String())
    time = db.Column(db.String())

    def __init__(self, firstName, phoneNumber, currentLocation, destination, date,time):
        self.firstName = firstName
        self.phoneNumber = phoneNumber
        self.currentLocation = currentLocation
        self.destination = destination
        self.date = date
        self.time = time

    def serialize(self):
        return {
            "name": self.firstName,
            "phoneNumber": self.phoneNumber,
            "currentLocation":self.currentLocation,
            "destination":self.destination,
            "date": self.date,
            "time":self.time
        }

    def __repr__(self):
        return f"<User {self.firstName}>"



@app.route('/api', methods=['POST'])
def index():
    d = {}
    d['firstName'] = str(request.form['firstName'])
    d['phoneNumber'] = str(request.form['phoneNumber'])
    d['typeOfUser'] = str(request.form['typeOfUser'])
    d['code'] = str(request.form['code'])
    print(d['firstName'])
    # http://127.0.0.1:5000/api?firstName=Hannah&phoneNumber=233266180856
    jd = jsonify(d)
    new_user = User(firstName=d['firstName'], phoneNumber=d['phoneNumber'], typeOfUser=d['typeOfUser'], code=d['code'])
    db.session.add(new_user)
    db.session.commit()
    return "<h1>Helooo {}<h1>".format(d['firstName'])


@app.route('/rideRequest', methods=['POST'])
def ride():
    now = datetime.datetime.now()
    today = str(now.year)+"-"+ str(now.month)+"-"+str(now.day)
    timestamp = str(now.hour)+":"+ str(now.minute)+":"+str(now.second)
    d = {}
    d['firstName'] = str(request.form['firstName'])
    d['phoneNumber'] = str(request.form['phoneNumber'])
    d['currentLocation'] = str(request.form['currentLocation'])
    d['destination'] = str(request.form['destination'])
    print(d['firstName'])
    # http://127.0.0.1:5000/api?firstName=Hannah&phoneNumber=233266180856
    jd = jsonify(d)
    new_request = RideRequest(firstName=d['firstName'], phoneNumber=d['phoneNumber'], currentLocation=d['currentLocation'], destination=d['destination'], date=today, time=timestamp)
    db.session.add(new_request)
    db.session.commit()
    return "<h1>Helooo {}<h1>".format(d['firstName'])


@app.route('/getRideRequest', methods=['GET'])
def getRideRequest():
    return jsonify({'Requests': list(map(lambda dev: dev.serialize(), RideRequest.query.all()))})

if __name__ == '__main__':
    app.run()
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data/user.db'
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))


class UserSchema(Schema):
    __tablename__ = 'user'
    # id = fields.Integer()
    name = fields.String()
    last_name = fields.String()


@app.route('/')
def get():
    userschema = UserSchema(many=True)
    user = db.session.query(User).all()
    return userschema.dump(user)


@app.route('/', methods=['POST'])
def post():
    req = request.json
    userschema = UserSchema()
    user = User(name=req['name'], last_name=req['last_name'])
    db.session.add(user)
    db.session.commit()
    return userschema.dump(user)


if __name__ == "__main__":
    app.run()

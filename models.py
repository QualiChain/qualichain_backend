from werkzeug.security import generate_password_hash, check_password_hash

from app import db


class Book(db.Model):
    __tablename__ = 'books'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    author = db.Column(db.String())
    published = db.Column(db.String())

    def __init__(self, name, author, published):
        self.name = name
        self.author = author
        self.published = published

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'author': self.author,
            'published': self.published
        }


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    userPath = db.Column(db.String())
    role = db.Column(db.String())
    pilotId = db.Column(db.Integer())
    userName = db.Column(db.String())
    fullName = db.Column(db.String())
    name = db.Column(db.String())
    surname = db.Column(db.String())
    gender = db.Column(db.String())
    birthDate = db.Column(db.String())
    country = db.Column(db.String())
    city = db.Column(db.String())
    address = db.Column(db.String())
    zipCode = db.Column(db.String())
    mobilePhone = db.Column(db.String())
    homePhone = db.Column(db.String())
    email = db.Column(db.String())
    password_hash = db.Column(db.String())

    def __init__(self, userPath, role, pilotId, userName, fullName, name, surname, gender, birthDate, country, city,
                 address, zipCode, mobilePhone, homePhone, email):
        self.userPath = userPath
        self.role = role
        self.pilotId = pilotId
        self.userName = userName
        self.fullName = fullName
        self.name = name
        self.surname = surname
        self.gender = gender
        self.birthDate = birthDate
        self.country = country
        self.city = city
        self.address = address
        self.zipCode = zipCode
        self.mobilePhone = mobilePhone
        self.homePhone = homePhone
        self.email = email

    def __repr__(self):
        return '<id: {} userName: {}>'.format(self.id, self.userName)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def serialize(self):
        return {
            'id': self.id,
            'userPath': self.userPath,
            'role': self.role,
            'pilotId': self.pilotId,
            'userName': self.userName,
            'fullName': self.fullName,
            'name': self.name,
            'surname': self.surname,
            'gender': self.gender,
            'birthDate': self.birthDate,
            'country': self.country,
            'city': self.city,
            'address': self.address,
            'zipCode': self.zipCode,
            'mobilePhone': self.mobilePhone,
            'homePhone': self.homePhone,
            'email': self.email
        }

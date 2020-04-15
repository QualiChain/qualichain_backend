import datetime

import jwt
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash

from app import db
from settings import SECRET_KEY, TOKEN_EXPIRATION


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


class Skill(db.Model):
    __tablename__ = 'skills'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<id: {} name: {}>'.format(self.id, self.name)

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name
        }


class Job(db.Model):
    __tablename__ = 'jobs'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String())
    job_description = db.Column(db.String())
    level = db.Column(db.String())
    date = db.Column(db.String())
    start_date = db.Column(db.String())
    end_date = db.Column(db.String())
    creator_id = db.Column(db.Integer())
    employment_type = db.Column(db.String())
    skills = db.Column(db.JSON())

    def __init__(self, title, job_description, level, date, start_date, end_date, creator_id, employment_type, skills):
        self.title = title
        self.job_description = job_description
        self.level = level
        self.date = date
        self.start_date = start_date
        self.end_date = end_date
        self.creator_id = creator_id
        self.employment_type = employment_type
        self.skills = skills

    def __repr__(self):
        return '<id: {} job title: {}>'.format(self.id, self.title)

    def serialize(self):
        return {
            'id': self.id,
            'title': self.title,
            'job_description': self.job_description,
            'level': self.level,
            'date': self.date,
            'start_date': self.start_date,
            'end_date': self.end_date,
            'creator_id': self.creator_id,
            'employment_type': self.employment_type,
            'skills': self.skills
        }


class UserJob(db.Model):
    __tablename__ = 'users_jobs'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.ForeignKey(User.id))
    job_id = db.Column(db.ForeignKey(Job.id))
    role = db.Column(db.String())
    available = db.Column(db.String())
    exp_salary = db.Column(db.String())
    score = db.Column(db.Integer)

    user = relationship('User', foreign_keys='UserJob.user_id')
    job = relationship('Job', foreign_keys='UserJob.job_id')

    def __repr__(self):
        return '<user_id: {} job_id: {}>'.format(self.user_id, self.job_id)

    def __init__(self, user_id, job_id, role, available, exp_salary, score):
        self.user_id = user_id
        self.job_id = job_id
        self.role = role
        self.available = available
        self.exp_salary = exp_salary
        self.score = score

    def serialize(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'job': self.job.serialize(),
            'user': self.user.serialize(),
            'role': self.role,
            'available': self.available,
            'exp_salary': self.exp_salary,
            'score': self.score
        }

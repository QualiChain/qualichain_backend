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


class Course(db.Model):
    __tablename__ = 'courses'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    description = db.Column(db.String())
    semester = db.Column(db.String())
    endDate = db.Column(db.String())
    startDate = db.Column(db.String())
    updatedDate = db.Column(db.String())
    skills = db.Column(db.JSON())
    events = db.Column(db.JSON())

    def __init__(self, name, description, semester, endDate, startDate, updatedDate, skills, events):
        self.name = name
        self.description = description
        self.semester = semester
        self.endDate = endDate
        self.startDate = startDate
        self.updatedDate = updatedDate
        self.skills = skills
        self.events = events

    def __repr__(self):
        return '<id: {} name: {}>'.format(self.id, self.name)

    def serialize(self):
        return {
            'name': self.name,
            'description': self.description,
            'semester': self.semester,
            'endDate': self.endDate,
            'startDate': self.startDate,
            'updatedDate': self.updatedDate,
            'skills': self.skills,
            'events': self.events
        }


class UserCourse(db.Model):
    __tablename__ = 'user_courses'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.ForeignKey(User.id))
    course_id = db.Column(db.ForeignKey(Course.id))
    course_status = db.Column(db.String())

    user = relationship('User', foreign_keys='UserCourse.user_id')
    course = relationship('Course', foreign_keys='UserCourse.course_id')

    def __repr__(self):
        return '<user_id: {} course_id: {}>'.format(self.user_id, self.course_id)

    def __init__(self, user_id, course_id, course_status):
        self.user_id = user_id
        self.course_id = course_id
        self.course_status = course_status

    def serialize(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'course_status': self.course_status,
            'course': self.course.serialize()
        }


class UserCourseRecommendation(db.Model):
    __tablename__ = 'user_course_recommendations'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.ForeignKey(User.id))
    course_id = db.Column(db.ForeignKey(Course.id))
    rating = db.Column(db.String())
    user = relationship('User', foreign_keys='UserCourseRecommendation.user_id')
    course = relationship('Course', foreign_keys='UserCourseRecommendation.course_id')

    def __repr__(self):
        return '<user_id: {} recommended_course_id: {}>'.format(self.user_id, self.course_id)

    def __init__(self, user_id, course_id, rating):
        self.user_id = user_id
        self.course_id = course_id
        self.rating = rating

    def serialize(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'rating': self.rating,
            'course': self.course.serialize()
        }


class UserSkillRecommendation(db.Model):
    __tablename__ = 'user_skill_recommendations'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.ForeignKey(User.id))
    skill_id = db.Column(db.ForeignKey(Skill.id))
    description = db.Column(db.String())
    relevant_skills = db.Column(db.JSON())
    related_jobs = db.Column(db.JSON())
    user = relationship('User', foreign_keys='UserSkillRecommendation.user_id')
    skill = relationship('Skill', foreign_keys='UserSkillRecommendation.skill_id')

    def __repr__(self):
        return '<user_id: {} recommended_skill_id: {}>'.format(self.user_id, self.skill_id)

    def __init__(self, user_id, skill_id, description, relevant_skills, related_jobs):
        self.user_id = user_id
        self.skill_id = skill_id
        self.description = description
        self.relevant_skills = relevant_skills
        self.related_jobs = related_jobs

    def serialize(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'skill_id': self.skill_id,
            'description': self.description,
            'relevant_skills': self.relevant_skills,
            'related_jobs': self.related_jobs,
            'user': self.user.serialize(),
            'skill': self.skill.serialize()
        }


class UserJobRecommendation(db.Model):
    __tablename__ = 'user_job_recommendations'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.ForeignKey(User.id))
    job_id = db.Column(db.ForeignKey(Job.id))

    user = relationship('User', foreign_keys='UserJobRecommendation.user_id')
    job = relationship('Job', foreign_keys='UserJobRecommendation.job_id')

    def __repr__(self):
        return '<user_id: {} recommended_job_id: {}>'.format(self.user_id, self.job_id)

    def __init__(self, user_id, job_id):
        self.user_id = user_id
        self.job_id = job_id

    def serialize(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'job_id': self.job_id,
            'user': self.user.serialize(),
            'job': self.job.serialize()
        }


class CV(db.Model):
    __tablename__ = 'CVs'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.ForeignKey(User.id))
    person_URI = db.Column(db.String())
    label = db.Column(db.String())
    target_sector = db.Column(db.String())
    expected_salary = db.Column(db.String())
    description = db.Column(db.String())
    skills = db.Column(db.JSON())
    work_history = db.Column(db.JSON())
    education = db.Column(db.JSON())

    user = relationship('User', foreign_keys='CV.user_id')

    def __repr__(self):
        return '<user_id: {}, CV id: {}>'.format(self.user_id, self.id)

    def __init__(self, user_id, person_URI, label, target_sector, expected_salary, description, skills, work_history,
                 education):
        self.user_id = user_id
        self.person_URI = person_URI
        self.label = label
        self.target_sector = target_sector
        self.expected_salary = expected_salary
        self.description = description
        self.skills = skills
        self.work_history = work_history
        self.education = education

    def serialize(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'person_URI': self.person_URI,
            'label': self.label,
            'target_sector': self.target_sector,
            'expected_salary': self.expected_salary,
            'description': self.description,
            'skills': self.skills,
            'work_history': self.work_history,
            'education': self.education,
            'user': self.user.serialize()
        }


class Notification(db.Model):
    __tablename__ = 'notifications'

    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String())
    readed = db.Column(db.Boolean())
    user_id = db.Column(db.ForeignKey(User.id))

    def __repr__(self):
        return '<notification_id: {}, user_id: {}>'.format(self.id, self.user_id)

    def __init__(self, user_id, message):
        self.user_id = user_id
        self.message = message
        self.readed = False

    def serialize(self):
        return {
            'id': self.id,
            'message': self.message,
            'readed': self.readed,
            'user_id': self.user_id
        }


from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash

from application.database import db


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


class UserAvatar(db.Model):
    __tablename__ = 'avatars'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.ForeignKey(User.id))
    avatar = db.Column(db.LargeBinary(), nullable=False)

    user = relationship('User', foreign_keys='UserAvatar.user_id')

    def __init__(self, user_id, avatar):
        self.user_id = user_id,
        self.avatar = avatar


class UserFile(db.Model):
    __tablename__ = 'user_files'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.ForeignKey(User.id))
    filename = db.Column(db.String())

    user = relationship('User', foreign_keys='UserFile.user_id')

    def __init__(self, user_id, filename):
        self.user_id = user_id,
        self.filename = filename


class Job(db.Model):
    __tablename__ = 'jobs'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String())
    job_description = db.Column(db.String())
    level = db.Column(db.String())
    date = db.Column(db.String())
    start_date = db.Column(db.String())
    end_date = db.Column(db.String())
    creator_id = db.Column(db.ForeignKey(User.id))
    employment_type = db.Column(db.String())

    creator = relationship('User', foreign_keys='Job.creator_id')

    def __init__(self, title, job_description, level, date, start_date, end_date, creator_id, employment_type):
        self.title = title
        self.job_description = job_description
        self.level = level
        self.date = date
        self.start_date = start_date
        self.end_date = end_date
        self.creator_id = creator_id
        self.employment_type = employment_type

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
            'employment_type': self.employment_type
        }


class Skill(db.Model):
    __tablename__ = 'skills'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    type = db.Column(db.String())
    hard_skill = db.Column(db.Boolean())

    def __init__(self, name, type, hard_skill):
        self.type = type
        self.name = name
        self.hard_skill = hard_skill

    def __repr__(self):
        return '<id: {} name: {}>'.format(self.id, self.name)

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'type': self.type,
            'hard_skill': self.hard_skill
        }


class JobSkill(db.Model):
    __tablename__ = 'job_skills'

    id = db.Column(db.Integer, primary_key=True)
    job_id = db.Column(db.ForeignKey(Job.id))
    skill_id = db.Column(db.ForeignKey(Skill.id))

    skill = relationship('Skill', foreign_keys='JobSkill.skill_id')
    job = relationship('Job', foreign_keys='JobSkill.job_id')

    def __init__(self, skill_id, job_id):
        self.skill_id = skill_id
        self.job_id = job_id

    def serialize(self):
        return {
            'id': self.job_id,
            'skill_id': self.skill_id,
            'skill': self.skill
        }


class UserApplication(db.Model):
    __tablename__ = 'user_applications'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.ForeignKey(User.id))
    job_id = db.Column(db.ForeignKey(Job.id))
    available = db.Column(db.String())
    exp_salary = db.Column(db.Float())

    user = relationship('User', foreign_keys='UserApplication.user_id')
    job = relationship('Job', foreign_keys='UserApplication.job_id')

    def __repr__(self):
        return '<user_id: {} job_id: {}>'.format(self.user_id, self.job_id)

    def __init__(self, user_id, job_id, available, exp_salary):
        self.user_id = user_id
        self.job_id = job_id
        self.available = available
        self.exp_salary = exp_salary

    def serialize(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'job': self.job.serialize(),
            'user': self.user.serialize(),
            'available': self.available,
            'exp_salary': self.exp_salary,
        }


class Course(db.Model):
    __tablename__ = 'courses'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    description = db.Column(db.String())
    semester = db.Column(db.String())
    updatedDate = db.Column(db.String())
    events = db.Column(db.JSON())

    def __init__(self, name, description, semester, updatedDate, events):
        self.name = name
        self.description = description
        self.semester = semester
        self.updatedDate = updatedDate
        self.events = events

    def __repr__(self):
        return '<id: {} name: {}>'.format(self.id, self.name)

    def serialize(self):
        return {
            'courseid': self.id,
            'name': self.name,
            'description': self.description,
            'semester': self.semester,
            'updatedDate': self.updatedDate,
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

    def serialize_usersofacourse(self):
        return {
            'id': self.id,
            'user': self.user.serialize(),
            'course_status': self.course_status
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


class SkillCourse(db.Model):
    __tablename__ = 'skills_courses'

    id = db.Column(db.Integer, primary_key=True)
    skill_id = db.Column(db.ForeignKey(Skill.id))
    course_id = db.Column(db.ForeignKey(Course.id))

    skill = relationship('Skill', foreign_keys='SkillCourse.skill_id')
    course = relationship('Course', foreign_keys='SkillCourse.course_id')

    def __repr__(self):
        return '<skill_id: {} course_id: {}>'.format(self.skill_id, self.course_id)

    def __init__(self, skill_id, course_id):
        self.skill_id = skill_id
        self.course_id = course_id

    def serialize(self):
        return {
            'id': self.id,
            'skill_id': self.skill_id,
            'course': self.course.serialize(),
            'skill': self.skill.serialize(),
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
    target_sector = db.Column(db.String())
    description = db.Column(db.String())
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


class CVSkill(db.Model):
    __tablename__ = 'cv_skills'

    id = db.Column(db.Integer, primary_key=True)
    cv_id = db.Column(db.ForeignKey(CV.id))
    skill_id = db.Column(db.ForeignKey(Skill.id))

    cv = relationship('CV', foreign_keys='CVSkill.cv_id')
    skill = relationship('Skill', foreign_keys='CVSkill.skill_id')

    def __repr__(self):
        return '<cv_id: {} skill_id: {}>'.format(self.cv_id, self.skill_id)

    def __init__(self, cv_id, skill_id):
        self.cv_id = cv_id
        self.skill_id = skill_id

    def serialize(self):
        return {
            'id': self.id,
            'cv_id': self.cv_id,
            'skill': self.skill.serialize()
        }


class Notification(db.Model):
    __tablename__ = 'notifications'

    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String())
    read = db.Column(db.Boolean())
    user_id = db.Column(db.ForeignKey(User.id))

    def __repr__(self):
        return '<notification_id: {}, user_id: {}>'.format(self.id, self.user_id)

    def __init__(self, user_id, message):
        self.user_id = user_id
        self.message = message
        self.read = False

    def serialize(self):
        return {
            'id': self.id,
            'message': self.message,
            'read': self.read,
            'user_id': self.user_id
        }


class SmartBadge(db.Model):
    __tablename__ = 'smart_badges'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    issuer = db.Column(db.String())
    description = db.Column(db.String())

    def __init__(self, name, issuer, description):
        self.name = name
        self.issuer = issuer
        self.description = description

    def __repr__(self):
        return '<id: {} name: {}>'.format(self.id, self.name)

    def serialize(self):
        return {
            'id': self.id,
            'issuer': self.issuer,
            'name': self.name,
            'description': self.description
        }


class BadgeCourseRelation(db.Model):
    __tablename__ = 'badge_course_relation'

    id = db.Column(db.Integer, primary_key=True)
    badge_id = db.Column(db.ForeignKey(SmartBadge.id))
    course_id = db.Column(db.ForeignKey(Course.id))

    badge = relationship('SmartBadge', foreign_keys='BadgeCourseRelation.badge_id')
    course = relationship('Course', foreign_keys='BadgeCourseRelation.course_id')

    def __repr__(self):
        return '<badge_id: {} course_id: {}>'.format(self.badge_id, self.course_id)

    def __init__(self, badge_id, course_id):
        self.badge_id = badge_id
        self.course_id = course_id

    def serialize(self):
        return {
            'id': self.id,
            'badge': self.badge.serialize(),
            'course': self.course.serialize()
        }


class UserBadgeRelation(db.Model):
    __tablename__ = 'user_badge_relation'

    id = db.Column(db.Integer, primary_key=True)
    badge_id = db.Column(db.ForeignKey(SmartBadge.id))
    user_id = db.Column(db.ForeignKey(User.id))

    badge = relationship('SmartBadge', foreign_keys='UserBadgeRelation.badge_id')
    user = relationship('User', foreign_keys='UserBadgeRelation.user_id')

    def __repr__(self):
        return '<badge_id: {} user_id: {}>'.format(self.badge_id, self.user_id)

    def __init__(self, badge_id, user_id):
        self.badge_id = badge_id
        self.user_id = user_id

    def serialize(self):
        return {
            'id': self.id,
            'badge': self.badge.serialize(),
            'user': self.user.serialize()
        }

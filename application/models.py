import json

from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash

from application.database import db

import enum


class UserRole(enum.Enum):
    student = 'student'
    professor = 'professor'
    recruiter = 'recruiter'
    administrator = 'administrator'
    academic_organisation = 'academic organisation'
    recruitment_organisation = 'recruitment_organisation'


    def __json__(self):
        return self.value


class JobLevel(enum.Enum):
    entry = 'entry'
    intermediate = 'intermediate'
    experienced = 'experienced'
    advanced = 'advanced'
    expert = 'expert'

    def __json__(self):
        return self.value


class EmploymentType(enum.Enum):
    part_time = 'part-time'
    full_time = 'full-time'
    contractor = 'contractor'
    freelance = 'freelance'

    def __json__(self):
        return self.value


class CourseStatus(enum.Enum):
    enrolled = 'enrolled'
    taught = 'taught'
    done = 'done'

    def __json__(self):
        return self.value


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    userPath = db.Column(db.String(), nullable=True)
    role = db.Column('role_value', db.Enum(UserRole))
    pilotId = db.Column(db.Integer())
    userName = db.Column(db.String())
    fullName = db.Column(db.String(), nullable=True)
    name = db.Column(db.String(), nullable=True)
    surname = db.Column(db.String(), nullable=True)
    gender = db.Column(db.String(), nullable=True)
    birthDate = db.Column(db.String(), nullable=True)
    country = db.Column(db.String())
    city = db.Column(db.String())
    address = db.Column(db.String())
    zipCode = db.Column(db.String(), nullable=True)
    mobilePhone = db.Column(db.String(), nullable=True)
    homePhone = db.Column(db.String(), nullable=True)
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
            'role': self.role.__json__(),
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


class AcademicOrganisation(db.Model):
    __tablename__ = 'academic_organisation'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String())
    description = db.Column(db.String())

    def __init__(self, title, description):
        self.title = title
        self.description = description

    def __repr__(self):
        return '<id: {} title: {}>'.format(self.id, self.title)

    def serialize(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
        }


class RecruitmentOrganisation(db.Model):
    __tablename__ = 'recruitment_organisation'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String())
    description = db.Column(db.String())

    def __init__(self, title, description):
        self.title = title
        self.description = description

    def __repr__(self):
        return '<id: {} title: {}>'.format(self.id, self.title)

    def serialize(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
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

class Specialization(db.Model):
    __tablename__ = 'specialization'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String())

    def __init__(self, title):
        self.title = title


    def __repr__(self):
        return '<id: {} title: {}>'.format(self.id, self.title)

    def serialize(self):
        return {
            'id': self.id,
            'title': self.title,
        }


class Thesis(db.Model):
    __tablename__ = 'thesis'

    id = db.Column(db.Integer, primary_key=True)
    professor_id = db.Column(db.ForeignKey(User.id))
    student_id = db.Column(db.ForeignKey(User.id), nullable=True)
    title = db.Column(db.String())
    status = db.Column(db.String())
    description = db.Column(db.String())
    professor = relationship('User', foreign_keys='Thesis.professor_id')
    student = relationship('User', foreign_keys='Thesis.student_id')

    def __init__(self, professor_id, title, description):
        self.professor_id = professor_id
        self.title = title
        self.description = description
        self.status = 'published'
    #     options include: published, assigned, completed

    def serialize(self):
        return {
            'id': self.id,
            'professor': self.professor.serialize(),
            'student_id': self.student_id,
            'status': self.status,
            'title': self.title,
            'description': self.description
        }


class ThesisRequest(db.Model):
    __tablename__ = 'thesis_requests'

    id = db.Column(db.Integer, primary_key=True)
    thesis_id = db.Column(db.ForeignKey(Thesis.id))
    student_id = db.Column(db.ForeignKey(User.id), nullable=True)

    thesis = relationship('Thesis', foreign_keys='ThesisRequest.thesis_id')
    student = relationship('User', foreign_keys='ThesisRequest.student_id')

    def __init__(self, thesis_id, student_id):
        self.thesis_id = thesis_id
        self.student_id = student_id

    def serialize(self):
        return {
            'id': self.id,
            'thesis': self.thesis.serialize(),
            'student': self.student.serialize(),
        }

class Job(db.Model):
    __tablename__ = 'jobs'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String())
    job_description = db.Column(db.String())
    level = db.Column('level_value', db.Enum(JobLevel), nullable=True)
    country = db.Column(db.String())
    state = db.Column(db.String())
    city = db.Column(db.String())
    employer_id = db.Column(db.ForeignKey(RecruitmentOrganisation.id), nullable=True)
    specialization_id = db.Column(db.ForeignKey(Specialization.id), nullable=True)
    date = db.Column(db.String(), nullable=True)
    start_date = db.Column(db.String(), nullable=True)
    end_date = db.Column(db.String(), nullable=True)
    creator_id = db.Column(db.ForeignKey(User.id), nullable=True)
    employment_type = db.Column('employment_value', db.Enum(EmploymentType), nullable=True)
    date_published = db.Column(db.DateTime, server_default=db.func.now())

    creator = relationship('User', foreign_keys='Job.creator_id')
    specialization = relationship('Specialization', foreign_keys='Job.specialization_id')
    employer = relationship('RecruitmentOrganisation', foreign_keys='Job.employer_id')

    def __init__(self, title, job_description, level, date, start_date, end_date, creator_id, employment_type, country,
                 employer_id, specialization_id, state, city):
        self.title = title
        self.job_description = job_description
        self.level = level
        self.date = date
        self.start_date = start_date
        self.end_date = end_date
        self.creator_id = creator_id
        self.employment_type = employment_type
        self.country = country
        self.city = city
        self.state = state
        self.employer_id = employer_id
        self.specialization_id = specialization_id

    def __repr__(self):
        return '<id: {} job title: {}>'.format(self.id, self.title)

    def serialize(self):
        formatted_datetime = self.date_published.isoformat()

        return {
            'id': self.id,
            'title': self.title,
            'job_description': self.job_description,
            'level': self.level.__json__(),
            'date': self.date,
            'start_date': self.start_date,
            'end_date': self.end_date,
            'creator_id': self.creator_id,
            'employment_type': self.employment_type.__json__(),
            'country': self.country,
            'state': self.state,
            'city': self.city,
            'employer_id': self.employer_id,
            'specialization': self.specialization_id,
            'date_published': formatted_datetime
        }




class UserAcademicOrganisation(db.Model):
        __tablename__ = 'user_academic_organisations'

        id = db.Column(db.Integer, primary_key=True)
        user_id = db.Column(db.ForeignKey(User.id))
        organisation_id = db.Column(db.ForeignKey(AcademicOrganisation.id))

        user = relationship('User', foreign_keys='UserAcademicOrganisation.user_id')
        academic_organisation = relationship('AcademicOrganisation', foreign_keys='UserAcademicOrganisation.organisation_id')

        def __repr__(self):
            return '<user_id: {} academic_organisation_id: {}>'.format(self.user_id, self.organisation_id)

        def __init__(self, user_id, organisation_id):
            self.user_id = user_id
            self.organisation_id = organisation_id


        def serialize(self):
            return {
                'id': self.id,
                'user_id': self.user.serialize(),
                'academic_organisation': self.academic_organisation.serialize()
            }


class UserRecruitmentOrganisation(db.Model):
    __tablename__ = 'user_recruitment_organisations'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.ForeignKey(User.id))
    organisation_id = db.Column(db.ForeignKey(RecruitmentOrganisation.id))

    user = relationship('User', foreign_keys='UserRecruitmentOrganisation.user_id')
    recruitment_organisation = relationship('RecruitmentOrganisation',
                                         foreign_keys='UserRecruitmentOrganisation.organisation_id')

    def __repr__(self):
        return '<user_id: {} recruitment_organisation_id: {}>'.format(self.user_id, self.organisation_id)

    def __init__(self, user_id, organisation_id):
        self.user_id = user_id
        self.organisation_id = organisation_id

    def serialize(self):
        return {
            'id': self.id,
            'user_id': self.user.serialize(),
            'recruitment_organisation': self.recruitment_organisation.serialize()
        }



class Skill(db.Model):
    __tablename__ = 'skills'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    type = db.Column(db.String())
    alt_label = db.Column(db.String())
    hard_skill = db.Column(db.Boolean())

    def __init__(self, name, type, hard_skill, alt_label):
        self.type = type
        self.name = name
        self.hard_skill = hard_skill
        self.alt_label = alt_label

    def __repr__(self):
        return '<id: {} name: {}>'.format(self.id, self.name)

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'hard_skill': self.hard_skill,
            'type': self.type,
            'alt_label': self.alt_label
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
    events = db.Column(db.JSON(), nullable=True)
    academic_organisation_id = db.Column(db.ForeignKey(AcademicOrganisation.id), nullable=True)

    academic_org = relationship('AcademicOrganisation', foreign_keys='Course.academic_organisation_id')

    def __init__(self, name, description, semester, updatedDate, events, academic_organisation_id):
        self.name = name
        self.description = description
        self.semester = semester
        self.updatedDate = updatedDate
        self.events = events
        self.academic_organisation_id = academic_organisation_id

    def __repr__(self):
        return '<id: {} name: {}>'.format(self.id, self.name)

    def serialize(self):
        return {
            'courseid': self.id,
            'name': self.name,
            'description': self.description,
            'semester': self.semester,
            'updatedDate': self.updatedDate,
            'events': self.events,
            'academic_organisation': self.academic_organisation_id
        }


class UserCourse(db.Model):
    __tablename__ = 'user_courses'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.ForeignKey(User.id))
    course_id = db.Column(db.ForeignKey(Course.id))
    course_status = db.Column('status_value', db.Enum(CourseStatus))
    grade = db.Column(db.Integer, default=0)

    user = relationship('User', foreign_keys='UserCourse.user_id')
    course = relationship('Course', foreign_keys='UserCourse.course_id')

    def __repr__(self):
        return '<user_id: {} course_id: {}>'.format(self.user_id, self.course_id)

    def __init__(self, user_id, course_id, course_status, grade):
        self.user_id = user_id
        self.course_id = course_id
        self.course_status = course_status
        self.grade = grade

    def serialize(self):
        return {
            'id': self.id,
            'user_id': self.user.serialize(),
            'course_status': self.course_status.__json__(),
            'grade': self.grade,
            'course': self.course.serialize()
        }

    def serialize_usersofacourse(self):
        return {
            'id': self.id,
            'user': self.user.serialize(),
            'course_status': self.course_status.__json__(),
            'course_grade': self.grade
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
    skill_id = db.Column(db.ForeignKey(Skill.id, ondelete='CASCADE'))
    course_id = db.Column(db.ForeignKey(Course.id, ondelete='CASCADE'))

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

    def serialize_skillsofacourse(self):
        return {
            'id': self.id,
            'skill': self.skill.serialize(),
            'course_id': self.course_id
        }


class UserSkillRecommendation(db.Model):
    __tablename__ = 'user_skill_recommendations'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.ForeignKey(User.id, ondelete='CASCADE'))
    skill_id = db.Column(db.ForeignKey(Skill.id, ondelete='CASCADE'))
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
    user_id = db.Column(db.ForeignKey(User.id, ondelete='CASCADE'))
    job_id = db.Column(db.ForeignKey(Job.id, ondelete='CASCADE'))

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
    user_id = db.Column(db.ForeignKey(User.id, ondelete='CASCADE'))
    target_sector = db.Column(db.String())
    description = db.Column(db.String())
    work_history = db.Column(db.JSON())
    education = db.Column(db.JSON())

    user = relationship('User', foreign_keys='CV.user_id')

    def __repr__(self):
        return '<user_id: {}, CV id: {}>'.format(self.user_id, self.id)

    def __init__(self, user_id, target_sector, description, work_history,
                 education):
        self.user_id = user_id
        self.target_sector = target_sector
        self.description = description
        self.work_history = work_history
        self.education = education

    def serialize(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'target_sector': self.target_sector,
            'description': self.description,
            'work_history': self.work_history,
            'education': self.education,
            'user': self.user.serialize()
        }


class CVSkill(db.Model):
    __tablename__ = 'cv_skills'

    id = db.Column(db.Integer, primary_key=True)
    cv_id = db.Column(db.ForeignKey(CV.id, ondelete='CASCADE'))
    skill_id = db.Column(db.ForeignKey(Skill.id, ondelete='CASCADE'))
    skil_level = db.Column(db.Integer, default=0)

    cv = relationship('CV', foreign_keys='CVSkill.cv_id')
    skill = relationship('Skill', foreign_keys='CVSkill.skill_id')

    def __repr__(self):
        return '<cv_id: {} skill_id: {}>'.format(self.cv_id, self.skill_id)

    def __init__(self, cv_id, skill_id, skill_level):
        self.cv_id = cv_id
        self.skill_id = skill_id
        self.skil_level = skill_level

    def serialize(self):
        return {
            'id': self.id,
            'cv_id': self.cv_id,
            'skill_level': self.skil_level,
            'skill': self.skill.serialize()
        }


class Notification(db.Model):
    __tablename__ = 'notifications'

    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String())
    read = db.Column(db.Boolean())
    user_id = db.Column(db.ForeignKey(User.id, ondelete='CASCADE'))
    date_created = db.Column(db.DateTime, server_default=db.func.now())

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


class UserNotificationPreference(db.Model):
    __tablename__ = 'user_notification_preference'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.ForeignKey(User.id, ondelete='CASCADE'))
    locations = db.Column(db.String())
    specializations = db.Column(db.String())
    internal_reallocation_availability = db.Column(db.Boolean(), default=False)

    def __repr__(self):
        return '<preference_id: {}, user_id: {}>'.format(self.id, self.user_id)

    def __init__(self, user_id, locations, specializations, internal_reallocation_availability):
        self.user_id = user_id
        self.locations = locations
        self.specializations = specializations
        self.internal_reallocation_availability= internal_reallocation_availability
    def serialize(self):
        return {
            'id': self.id,
            'locations': self.locations,
            'specializations': self.specializations,
            'internal_reallocation_availability': self.internal_reallocation_availability,
            'user_id': self.user_id,
        }


class UserJobVacancy(db.Model):
    __tablename__ = 'user_job_vacancy'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.ForeignKey(User.id))
    job_id = db.Column(db.ForeignKey(Job.id))

    def __repr__(self):
        return '<user_job_vacancy_id: {}, user_id: {}, job_id: {}>'.format(self.id, self.user_id, self.job_id)

    def __init__(self, user_id, job_id):
        self.user_id = user_id
        self.job_id = job_id

    def serialize(self):
        return {
            'id': self.id,
            'job_id': self.job_id,
            'user_id': self.user_id,
        }


class SmartBadge(db.Model):
    __tablename__ = 'smart_badges'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    issuer = db.Column(db.String())
    description = db.Column(db.String())
    type = db.Column(db.String())
    oubadge = db.Column(db.JSON(), nullable=False)

    def __init__(self, name, issuer, description, type, oubadge):
        self.name = name
        self.issuer = issuer
        self.description = description
        self.type = type
        self.oubadge = oubadge

    def __repr__(self):
        return '<id: {} name: {}>'.format(self.id, self.name)

    def serialize(self):
        return {
            'id': self.id,
            'issuer': self.issuer,
            'name': self.name,
            'description': self.description,
            'type': self.type,
            'oubadge': self.oubadge
        }


class BadgeCourseRelation(db.Model):
    __tablename__ = 'badge_course_relation'

    id = db.Column(db.Integer, primary_key=True)
    badge_id = db.Column(db.ForeignKey(SmartBadge.id, ondelete='CASCADE'))
    course_id = db.Column(db.ForeignKey(Course.id, ondelete='CASCADE'))

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
    __table_args__ = (
        db.UniqueConstraint('badge_id', 'user_id'),
      )
    id = db.Column(db.Integer, primary_key=True)
    badge_id = db.Column(db.ForeignKey(SmartBadge.id, ondelete='CASCADE'))
    user_id = db.Column(db.ForeignKey(User.id, ondelete='CASCADE'))
    oubadge_user = db.Column(db.JSON(), nullable=False)
    ou_metadata = db.Column(db.JSON(), nullable=True)

    badge = relationship('SmartBadge', foreign_keys='UserBadgeRelation.badge_id')
    user = relationship('User', foreign_keys='UserBadgeRelation.user_id')

    def __repr__(self):
        return '<badge_id: {} user_id: {}>'.format(self.badge_id, self.user_id)

    def __init__(self, badge_id, user_id, oubadge_user, ou_metadata):
        self.badge_id = badge_id
        self.user_id = user_id
        self.oubadge_user = oubadge_user
        self.ou_metadata = ou_metadata

    def serialize(self):
        return {
            'id': self.id,
            'badge': self.badge.serialize(),
            'user': self.user.serialize(),
            'oubadge_user': self.oubadge_user,
            'ou_metadata': self.ou_metadata
        }


class KpiTime(db.Model):
    __tablename__ = 'kpi_time'
    id = db.Column(db.Integer, primary_key=True)
    kpi_name = db.Column(db.String())
    time = db.Column(db.Integer, default=0)

    def __repr__(self):
        return '<kpi: {} seconds: {}>'.format(self.kpi_name, self.time)

    def __init__(self, kpi_name, time):
        self.kpi_name = kpi_name
        self.time = time

    def serialize(self):
        return {
            'id': self.id,
            'kpi_name': self.kpi_name,
            'time': self.time
        }

class Kpi(db.Model):
    __tablename__ = 'kpi'
    id = db.Column(db.Integer, primary_key=True)
    kpi_name = db.Column(db.String())
    count = db.Column(db.Integer, default=0)

    def __repr__(self):
        return '<kpi: {} count: {}>'.format(self.kpi_name, self.count)

    def __init__(self, kpi_name, count):
        self.kpi_name = kpi_name
        self.count = count

    def serialize(self):
        return {
            'id': self.id,
            'kpi_name': self.kpi_name,
            'count': self.count
        }


class Questionnaire(db.Model):
    __tablename__ = 'questionnaire'
    id = db.Column(db.Integer, primary_key=True)
    satisfaction_level = db.Column(db.Integer, default=5)
    feedback = db.Column(db.String())

    def __repr__(self):
        return '<satisfaction: {} feedback: {}>'.format(self.satisfaction_level, self.feedback)

    def __init__(self, satisfaction_level, feedback):
        self.satisfaction_level = satisfaction_level
        self.feedback = feedback

    def serialize(self):
        return {
            'id': self.id,
            'satisfaction_level': self.satisfaction_level,
            'feedback': self.feedback
        }

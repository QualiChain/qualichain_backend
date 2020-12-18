from flask import Flask
from flask_cors import CORS

from application.badges import badge_blueprint
from application.courses import course_blueprint
from application.cvs import cv_blueprint
from application.database import db, mail
from application.jobs import job_blueprint
from application.mediator import mediator_blueprint
from application.notifications import notification_blueprint
from application.recommendations import recommendation_blueprint
from application.kpis_questionnaire import kpis_questionnaire_blueprint
from application.settings import APP_SETTINGS, UPLOAD_FOLDER, MAIL_SERVER, MAIL_PORT, MAIL_USERNAME, MAIL_PASSWORD, \
    MAIL_USE_TLS, \
    MAIL_USE_SSL
from application.skills import skill_blueprint
from application.users import user_blueprint


# Globally accessible libraries


def create_app():
    """Initialize the core application."""
    app = Flask(__name__)

    app.config.from_object(APP_SETTINGS)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

    app.config['MAIL_SERVER'] = MAIL_SERVER
    app.config['MAIL_PORT'] = MAIL_PORT
    app.config['MAIL_USERNAME'] = MAIL_USERNAME
    app.config['MAIL_PASSWORD'] = MAIL_PASSWORD
    app.config['MAIL_USE_TLS'] = MAIL_USE_TLS
    app.config['MAIL_USE_SSL'] = MAIL_USE_SSL

    CORS(app)

    # Initialize Plugins
    db.init_app(app)
    mail.init_app(app)

    # Register Blueprints
    app.register_blueprint(user_blueprint)
    app.register_blueprint(skill_blueprint)
    app.register_blueprint(job_blueprint)
    app.register_blueprint(course_blueprint)
    app.register_blueprint(cv_blueprint)
    app.register_blueprint(notification_blueprint)
    app.register_blueprint(recommendation_blueprint)
    app.register_blueprint(badge_blueprint)
    app.register_blueprint(mediator_blueprint)
    app.register_blueprint(kpis_questionnaire_blueprint)

    return app

import logging
import sys
from application.database import db
from application.models import Job, UserApplication, User, Notification, UserNotificationPreference, UserJobVacancy
from datetime import datetime, timedelta
from sqlalchemy import desc

from sqlalchemy import create_engine
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import sessionmaker

sys.path.append('../')
from application.settings import ENGINE_STRING, CURRICULUM_DB_ENGINE, STR_CURRENT_TIME

logging.basicConfig(stream=sys.stdout, level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
log = logging.getLogger(__name__)

from application.models import Job, UserApplication, User, Notification, UserNotificationPreference, UserJobVacancy

class JobVacancySearchObject(object):
    """
    This is a Python Object that searches for Job Vacancies utilising Elastic Search
    """

    def __init__(self):
        self.engine = create_engine(ENGINE_STRING)
        self.Base = automap_base()
        self.base = self.Base.prepare(self.engine, reflect=True)

        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()


        self.Users = self.Base.classes.users
        self.Courses = self.Base.classes.courses
        self.Skills = self.Base.classes.skills
        self.SkillToCourse = self.Base.classes.skills_courses

    def load_all_users(self):
        users = User.query.all()
        if len(users) > 0:
            log.info(users)
            return users

    def query_elastic_for_job_vacancies(self, pref):
    #     TODO: create the query for elastic using location and specialisation preferences and Analyzer?
        results = []
        if len(results) == 0:
            # TODO: create query using state instead of city
            results = []
        if len(results) == 0:
            # TODO: crete query using country
            results = []
        return []


    def user_active(self, user_id):
        current_time = datetime.now()
        last_notification = Notification.query.filter(user_id=user_id).order_by(desc(Notification.date_created)).first()
        if current_time - timedelta(days=10) > last_notification.date_created:
            return True
        else:
            return False

    def save_job_vacancies_per_user(self):
        users = self.load_all_users()
        for user in users:
            if self.user_active(user.id):
                pref = UserNotificationPreference.query.filter(user_id=user.id)
                list_of_jobs = self.query_elastic_for_job_vacancies(pref)
                for job in list_of_jobs:
                    job_vacancy = UserJobVacancy(user_id=user.id, job_id=job)
                    db.session.add(job_vacancy)
                    db.session.commit()


def main():
    """Run this script to save all related job vacancy Information to Qualichain DB for all active users"""
    job_vacancy_search = JobVacancySearchObject()
    job_vacancy_search.save_job_vacancies_per_user()



if __name__ == "__main__":
    main()

import logging
import sys
import json

from datetime import datetime, timedelta
from sqlalchemy import desc

from sqlalchemy import create_engine
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import sessionmaker

sys.path.append('../../')
from application.settings import ENGINE_STRING
from application.clients.qualichain_analyzer import QualiChainAnalyzer

logging.basicConfig(stream=sys.stdout, level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
log = logging.getLogger(__name__)


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

        self.User = self.Base.classes.users
        self.Notification = self.Base.classes.notifications
        self.UserNotificationPreference = self.Base.classes.user_notification_preference
        self.UserJobVacancy = self.Base.classes.user_job_vacancy

    def load_all_users(self):
        users = self.session.query(self.User).all()
        if len(users) > 0:
            return users

    def query_elastic_for_job_vacancies(self, pref):
        locations = pref.locations
        specializations = pref.specializations
        anal_object = QualiChainAnalyzer()
        results = anal_object.search_job_according_to_preference(country=locations,
                                                                 state=locations,
                                                                 city=locations,
                                                                 specialization=specializations)
        log.info(results)
        results = results.json()
        return results

    def user_active(self, user_id):
        current_time = datetime.now()
        last_notification = self.session.query(self.Notification).filter(self.Notification.user_id == user_id).order_by(
            desc(self.Notification.date_created))
        if last_notification:
            last_notification = last_notification.first()
            if current_time - timedelta(days=10) > last_notification.date_created:
                return True
            else:
                return False
        return True

    def save_job_vacancies_per_user(self):
        users = self.load_all_users()
        for user in users:
            if self.user_active(user.id):
                pref = self.session.query(self.UserNotificationPreference).filter(
                    self.UserNotificationPreference.user_id == user.id).first()
                list_of_jobs = self.query_elastic_for_job_vacancies(pref)
                for job in list_of_jobs:
                    try:
                        if '_source' in job.keys():
                            if 'id' in job['_source'].keys():
                                job_id = (job['_source'])['id']
                                job_vacancy = self.UserJobVacancy(user_id=user.id, job_id=job_id)
                                self.session.add(job_vacancy)
                                self.session.commit()
                                log.info(
                                    'New Record for Job Vacancy concerning user_id {} has been added'.format(user.id))

                    except Exception as ex:
                        log.error(ex)
                        return ex, 400


def main():
    """Run this script to save all related job vacancy Information to Qualichain DB for all active users"""
    job_vacancy_search = JobVacancySearchObject()
    job_vacancy_search.save_job_vacancies_per_user()


if __name__ == "__main__":
    main()

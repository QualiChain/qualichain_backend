import logging
import sys
import json

from datetime import datetime, timedelta
from sqlalchemy import desc

from sqlalchemy import create_engine
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import sessionmaker

sys.path.append('../../')
from application.settings import ENGINE_STRING, ACTIVE_USER_PERIOD
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
        """loads all users"""
        users = self.session.query(self.User).all()
        if len(users) > 0:
            log.info("Found {} users".format(len(users)))
            return users

    @staticmethod
    def query_elastic_for_job_vacancies(pref):
        """passes the necessary parameters to the analyzer client object"""
        locations = pref.locations
        specializations = pref.specializations

        anal_object = QualiChainAnalyzer()
        if locations == "" and specializations == "":
            results = {}
        else:
            results = anal_object.search_job_according_to_preference(location=locations,
                                                                     specialization=specializations)
            results = results.json()
        log.info(results)
        return results

    def user_active(self, user_id):
        """checks if user has seen his notifications. If he doesn't have any notifications returns True"""

        current_time = datetime.now()
        last_notification = self.session.query(self.Notification).filter(self.Notification.user_id == user_id).order_by(
            desc(self.Notification.date_created))

        if last_notification.count() > 0:
            last_notification = last_notification.first()
            notify_period = current_time - timedelta(days=ACTIVE_USER_PERIOD)

            if notify_period > last_notification.date_created:
                return True
            else:
                return False
        return True

    def save_job_vacancies_per_user(self):
        """creates and saves the related job vacancies for each user"""
        users = self.load_all_users()
        for user in users:
            log.info("Process preferences for user with ID: {}".format(user.id))

            pref = self.session.query(self.UserNotificationPreference).filter(
                self.UserNotificationPreference.user_id == user.id)

            if pref.count() > 0 and self.user_active(user.id):

                self.session.query(self.UserJobVacancy).filter(self.UserJobVacancy.user_id == user.id).delete()
                self.session.commit()
                pref = pref.first()

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
                        self.session.close()

                    except Exception as ex:
                        log.error(ex)
                        return ex, 400

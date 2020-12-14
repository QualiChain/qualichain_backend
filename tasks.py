import logging
import sys


from celery import Celery

from application.loaders.job_vacancies_notifications import JobVacancySearchObject

logging.basicConfig(stream=sys.stdout, level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")

log = logging.getLogger(__name__)

app = Celery("backend")
app.config_from_object('application.settings', namespace="CELERY_")


@app.task
def job_vacancy_notifications():
    """This is a periodic task that is executed every minute to give job notifications to users"""
    job_vacancy_search = JobVacancySearchObject()
    job_vacancy_search.save_job_vacancies_per_user()
    job_vacancy_search.engine.dispose()
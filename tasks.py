import logging
import sys

from celery import Celery

logging.basicConfig(stream=sys.stdout, level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")

log = logging.getLogger(__name__)

app = Celery("backend")
app.config_from_object('application.settings', namespace="CELERY_")


# from application.loaders.job_vacancies_notifications import JobVacancySearchObject
#
# job_vacancy_search = JobVacancySearchObject()
# job_vacancy_search.save_job_vacancies_per_user()

@app.task
def hello():
    print("hello world", flush=True)
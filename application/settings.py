import os

# APP SETTINGS
from datetime import datetime

MY_ENV_VAR = os.environ.get('MY_ENV_VAR', 'this_variable')
API_PORT = os.environ.get('API_PORT', 5000)

FUSEKI_CLIENT_HOST = os.environ.get('FUSEKI_CLIENT_HOST', 'qualichain.epu.ntua.gr')
FUSEKI_CLIENT_PORT = os.environ.get('FUSEKI_CLIENT_PORT', 3030)
FUSEKI_CLIENT_DATASET = os.environ.get('FUSEKI_CLIENT_DATASET', 'saro')

RABBITMQ_HOST = os.environ.get('RABBITMQ_HOST', 'qualichain.epu.ntua.gr')
RABBITMQ_PORT = os.environ.get('RABBITMQ_PORT', 5672)
RABBITMQ_VHOST = os.environ.get('RABBITMQ_VHOST', '/')
RABBITMQ_USER = os.environ.get('RABBITMQ_USER', 'rabbitmq')
RABBITMQ_PASSWORD = os.environ.get('RABBITMQ_PASSWORD', 'rabbitmq')
RABBITMQ_BEAT_VHOST = os.environ.get('RABBITMQ_BEAT_VHOST', 'backend')

# =================================
#   APPLICATION SETTINGS
# =================================
APP_QUEUE = os.environ.get('APP_QUEUE', "mediator_queue")
BEAT_INTERVAL = int(os.getenv('BEAT_INTERVAL', default=1800))
UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER', '/opt/mediator_api/uploads')
APP_ROOT_PATH = "/opt/mediator_api"
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

DATABASE_HOST = os.environ.get('POSTGRES_HOST', 'localhost')
DATABASE_USER = os.environ.get('POSTGRES_USER', 'admin')
DATABASE_PASSWORD = os.environ.get('POSTGRES_PASSWORD', 'admin')
DATABASE = os.environ.get('POSTGRES_DB', 'qualichain_db')

ENGINE_STRING = 'postgresql+psycopg2://{}:{}@{}/{}'.format(
    DATABASE_USER,
    DATABASE_PASSWORD,
    DATABASE_HOST,
    DATABASE
)

APP_SETTINGS = os.environ.get("APP_SETTINGS", "config.DevelopmentConfig")
SECRET_KEY = os.environ.get("SECRET_KEY", "SECRET_KEY")
CURRENT_TIME = datetime.now()
STR_CURRENT_TIME = CURRENT_TIME.strftime("%b %d %Y, %H:%M:%S")
TOKEN_EXPIRATION = 30  # MINUTES

# =================================
#   EMAIL SERVER SETTINGS
# =================================
MAIL_SERVER = os.environ.get('smtp.gmail.com', 'MAIL_SERVER')
MAIL_PORT = os.environ.get('465', 'MAIL_PORT')
MAIL_USERNAME = os.environ.get('qualichain@gmail.com', 'MAIL_USERNAME')
MAIL_PASSWORD = os.environ.get('qualichain123#', 'MAIL_PASSWORD')
MAIL_USE_TLS = False
MAIL_USE_SSL = True

# =================================
#   CURRICULUM DB SETTINGS
# =================================
CURRICULUM_DB = {
    "USER": "admin",
    "PASSWORD": "admin",
    "HOST": 'qualichain.epu.ntua.gr',
    "DATABASE": 'api_db'
}
CURRICULUM_DB_ENGINE = "postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}/{DATABASE}".format(**CURRICULUM_DB)

# =================================
#   UNIVERSAL API SETTINGS
# =================================
API_TOKEN = '7XQHHkrwaMDDH87O6madXEtNPZAB6gszmIG6z_qQYuNq-_p5fBZZvoqK8pJn9MoPlUk'
UNIVERSAL_BASE_URL = 'https://www.universal-tutorial.com/api/'
UNIVERSAL_URLS = {
    "AUTH": "{}{}".format(UNIVERSAL_BASE_URL, 'getaccesstoken'),
    "COUNTRIES": "{}/{}".format(UNIVERSAL_BASE_URL, 'countries/'),
    "STATES": "{}/{}".format(UNIVERSAL_BASE_URL, 'states'),
    "CITIES": "{}/{}".format(UNIVERSAL_BASE_URL, 'cities')
}
# =================================
#   QualiChain Analyzer SETTINGS
# =================================
ANALYZER_HOST = os.environ.get('ANALYZER_HOST', 'qualichain.epu.ntua.gr')
ANALYZER_PORT = os.environ.get('ANALYZER_PORT', 5002)
ANALYZER_ENDPOINT = os.environ.get('ANALYZER_ENDPOINT', 'ask/storage')

JOB_INDEX = os.environ.get('JOB_INDEX', 'qc_job_index')
JOB_PROPERTIES = {
    "title": {"type": "text"},
    "job_description": {"type": "text"},
    "level": {"type": "text"},
    "country": {"type": "text"},
    "state": {"type": "text"},
    "city": {"type": "text"},
    "employer": {"type": "text"},
    "specialization": {"type": "text"},
    "employment_type": {"type": "text"},
    "required_skills": {"type": "text"}
}

# =================================
#   CELERY SETTINGS
# =================================
CELERY_BROKER_URL = 'pyamqp://{}:{}@{}:{}/{}'.format(
    RABBITMQ_USER, RABBITMQ_PASSWORD, RABBITMQ_HOST, RABBITMQ_PORT, RABBITMQ_BEAT_VHOST)

CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'UTC'
CELERY_TASK_ACKS_LATE = True
CELERY_TASK_ALWAYS_EAGER = True


# =================================
#   CELERY BEAT SETTINGS
# =================================
CELERY_BEAT_SCHEDULE = {
    # 'find_inactive_users_last_40hours_engine': {
    #     'task': 'tasks.find_inactive_users_last_40hours',
    #     'schedule': BEAT_INTERVAL  # RUN HALF HOUR
    # },
    # 'inactive_users_for_24hours_with_tot_followees_engine': {
    #     'task': 'tasks.inactive_users_for_24hours_with_tot_followees',
    #     'schedule': BEAT_INTERVAL  # RUN HALF HOUR
    # },
    # 'inactive_users_for_60hours_with_tot_followees_engine': {
    #     'task': 'tasks.inactive_users_for_60hours_with_tot_followees',
    #     'schedule': BEAT_INTERVAL  # RUN HALF HOUR
    # },
}
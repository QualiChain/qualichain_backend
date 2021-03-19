import os

from datetime import datetime

# =================================
#   APPLICATION SETTINGS
# =================================
API_PORT = os.environ.get('API_PORT', 5000)
APP_QUEUE = os.environ.get('APP_QUEUE', "mediator_queue")
BEAT_INTERVAL = int(os.getenv('BEAT_INTERVAL', default=60))
ACTIVE_USER_PERIOD = 2  # DAYS
UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER', '/opt/qualichain_backend/uploads')
APP_ROOT_PATH = "/opt/qualichain_backend"
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

APP_SETTINGS = os.environ.get("APP_SETTINGS", "config.DevelopmentConfig")
SECRET_KEY = os.environ.get("SECRET_KEY", "SECRET_KEY")
CURRENT_TIME = datetime.now()
STR_CURRENT_TIME = CURRENT_TIME.strftime("%b %d %Y, %H:%M:%S")
TOKEN_EXPIRATION = 30  # MINUTES

IAM_API_KEYS = {
    'localhost': '0062fdb4-f50b-42f2-a5e6-c380a80cfea4',
    'qualichain.herokuapp.com': 'e64663b9-f12e-484a-ad72-43778bcbef96'
}
IAM_PASSWORD = 'iam_f563b972ad'

# =================================
#   POSTGRES SETTINGS
# =================================
DATABASE_HOST = os.environ.get('POSTGRES_HOST', 'qualichain.epu.ntua.gr')
DATABASE_USER = os.environ.get('POSTGRES_USER', 'admin')
DATABASE_PASSWORD = os.environ.get('POSTGRES_PASSWORD', 'admin')
DATABASE = os.environ.get('POSTGRES_DB', 'qualichain_db')
DATABASE_PORT = os.environ.get('POSTGRESS_PORT', 5435)


ENGINE_STRING = 'postgresql+psycopg2://{}:{}@{}:{}/{}'.format(
    DATABASE_USER,
    DATABASE_PASSWORD,
    DATABASE_HOST,
    DATABASE_PORT,
    DATABASE
)

# =================================
#   CURRICULUM DB SETTINGS
# =================================
CURRICULUM_DB = {
    "USER": os.environ.get('CDB_USER', "admin"),
    "PASSWORD": os.environ.get('CDB_PASSWORD', "admin"),
    "HOST": os.environ.get('CDB_HOST', 'qualichain.epu.ntua.gr'),
    "DATABASE": os.environ.get('CDB_DATABASE', 'api_db')
}
CURRICULUM_DB_ENGINE = "postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}/{DATABASE}".format(**CURRICULUM_DB)

# =================================
#   FUSEKI SETTINGS
# =================================
FUSEKI_CLIENT_HOST = os.environ.get('FUSEKI_CLIENT_HOST', 'qualichain.epu.ntua.gr')
FUSEKI_CLIENT_PORT = os.environ.get('FUSEKI_CLIENT_PORT', 3030)
FUSEKI_CLIENT_DATASET = os.environ.get('FUSEKI_CLIENT_DATASET', 'saro')

# =================================
#   RABBITMQ SETTINGS
# =================================
RABBITMQ_HOST = os.environ.get('RABBITMQ_HOST', 'qualichain.epu.ntua.gr')
RABBITMQ_PORT = os.environ.get('RABBITMQ_PORT', 5672)
RABBITMQ_MNG_PORT = os.environ.get('RABBITMQ_MNG_PORT', 15672)
RABBITMQ_VHOST = os.environ.get('RABBITMQ_VHOST', '/')
RABBITMQ_USER = os.environ.get('RABBITMQ_USER', 'rabbitmq')
RABBITMQ_PASSWORD = os.environ.get('RABBITMQ_PASSWORD', 'rabbitmq')
RABBITMQ_BEAT_VHOST = os.environ.get('RABBITMQ_BEAT_VHOST', 'backend')

# =================================
#   EMAIL SERVER SETTINGS
# =================================
MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
MAIL_PORT = os.environ.get('MAIL_PORT', '465')
MAIL_USERNAME = os.environ.get('MAIL_USERNAME', 'qualichain@gmail.com')
MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD', 'qualichain123#')
MAIL_USE_TLS = False
MAIL_USE_SSL = True

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
    'job_vacancy_scheduler_for_active_users': {
        'task': 'tasks.job_vacancy_notifications',
        'schedule': BEAT_INTERVAL  # RUN every 1 min
    },
}

# =================================
#  COURSE RECOMMENDATION SETTINGS
# =================================
CR_HOST = os.environ.get('CR_HOST', 'qualichain.epu.ntua.gr')
CR_PORT = os.environ.get('CR_PORT', 7000)

# =================================
#  CURRICULUM RECOMMENDATION SETTINGS
# =================================
CD_HOST = os.environ.get('CD_HOST', 'qualichain.epu.ntua.gr')
CD_PORT = os.environ.get('CR_PORT', 8080)

# ==================================
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r"C:\Users\vkarakolis.EPU\Downloads\qualichain-translation-26d081738c31.json"

import os

# APP SETTINGS
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

# =================================
#   APPLICATION SETTINGS
# =================================
APP_QUEUE = os.environ.get('APP_QUEUE', "mediator_queue")
UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER', 'C:/Users/user/Documents/uploads')
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

DATABASE_HOST = os.environ.get('POSTGRES_HOST', 'localhost')
DATABASE_USER = os.environ.get('POSTGRES_USER', 'admin')
DATABASE_PASSWORD = os.environ.get('POSTGRES_PASSWORD', 'admin')
DATABASE = os.environ.get('POSTGRES_DB', 'api_db')

DATABASE_URL = "postgresql://{}:{}@{}/{}".format(
    DATABASE_USER,
    DATABASE_PASSWORD,
    DATABASE_HOST,
    DATABASE
)

ENGINE_STRING = 'postgresql+psycopg2://{}:{}@{}/{}'.format(
    DATABASE_USER,
    DATABASE_PASSWORD,
    DATABASE_HOST,
    DATABASE
)

APP_SETTINGS = os.environ.get("APP_SETTINGS", "config.DevelopmentConfig")
SECRET_KEY = os.environ.get("SECRET_KEY", "SECRET_KEY")
TOKEN_EXPIRATION = 30  # MINUTES

# =================================
#   EMAIL SERVER SETTINGS
# =================================
MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 465
MAIL_USERNAME = 'yourID@gmail.com'
MAIL_PASSWORD = '****************'
MAIL_USE_TLS = False
MAIL_USE_SSL = True
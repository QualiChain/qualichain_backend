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
DATABASE_URL = os.environ.get('DATABASE_URL', "postgresql://admin:admin@localhost/api_db")
APP_SETTINGS = os.environ.get("APP_SETTINGS", "config.DevelopmentConfig")
SECRET_KEY = os.environ.get("SECRET_KEY", "SECRET_KEY")

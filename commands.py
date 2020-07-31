"""
This Python script is used to execute admin commands for QualiChain Backend
"""
import logging
import sys

from application.settings import RABBITMQ_BEAT_VHOST
from application.utils import create_vhost


from application.clients.qualichain_analyzer import QualiChainAnalyzer

logging.basicConfig(stream=sys.stdout, level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")

log = logging.getLogger(__name__)

log.info("Initialize Index for Jobs")
analyzer = QualiChainAnalyzer()
analyzer.create_job_index()

log.info("Initialize Vhost for Backend Periodical and Async Tasks")
response = create_vhost(RABBITMQ_BEAT_VHOST)
if response.status_code != 201:
    log.error(response.reason)
else:
    log.info("{} added to RabbitMQ".format(RABBITMQ_BEAT_VHOST))
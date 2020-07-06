from application.clients.rabbitmq_client import RabbitMQClient
import json

from application.settings import APP_QUEUE


def add_to_queue(job_description):
    rabbit_mq = RabbitMQClient()

    payload = {
        "component": "DOBIE",
        "message": {
            "tasks": [
                {
                    "label": "95671c903a5b97a9",
                    "jobDescription": job_description
                }
            ]
        }
    }

    rabbit_mq.producer(queue=APP_QUEUE, message=json.dumps(payload))

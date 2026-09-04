import json
import os

import pika


def send_task(job_id: str, filename: str):
    rabbitmq_host = os.getenv("RABBITMQ_HOST", "localhost")

    connection = pika.BlockingConnection(
        pika.ConnectionParameters(rabbitmq_host)
    )

    channel = connection.channel()

    channel.queue_declare(
        queue="tasks",
        durable=True
    )

    message = {
        "job_id": job_id,
        "filename": filename
    }

    channel.basic_publish(
        exchange="",
        routing_key="tasks",
        body=json.dumps(message)
    )

    connection.close()
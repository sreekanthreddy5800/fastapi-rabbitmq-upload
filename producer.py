import json
import pika


def send_task(job_id: str, filename: str):

    connection = pika.BlockingConnection(
        pika.ConnectionParameters("rabbitmq")
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
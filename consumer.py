import json
import time
from pathlib import Path

import pika

while True:
    try:
        connection = pika.BlockingConnection(
            pika.ConnectionParameters("rabbitmq")
        )
        break
    except pika.exceptions.AMQPConnectionError:
        print(
            "RabbitMQ is not ready. Retrying in 5 seconds...",
            flush=True
        )
        time.sleep(5)


channel = connection.channel()

channel.queue_declare(
    queue="tasks",
    durable=True
)


def process_message(ch, method, properties, body):
    message = json.loads(body)

    job_id = message["job_id"]
    filename = message["filename"]

    print(f"Job ID: {job_id}", flush=True)
    print(f"Processing file: {filename}", flush=True)

    # Simulate file processing
    time.sleep(5)

    print(f"Completed file: {filename}", flush=True)

    file_path = Path("uploads") / filename

    if file_path.exists():
        file_path.unlink()
        print(f"Deleted file: {filename}", flush=True)

    ch.basic_ack(
        delivery_tag=method.delivery_tag
    )


channel.basic_consume(
    queue="tasks",
    on_message_callback=process_message,
    auto_ack=False
)

print(
    "Worker started. Waiting for tasks...",
    flush=True
)

channel.start_consuming()
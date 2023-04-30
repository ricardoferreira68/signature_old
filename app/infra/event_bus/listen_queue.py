from asyncio import run
from logging import info
from os import getenv
from pika import BlockingConnection, ConnectionParameters, PlainCredentials

from configuration import start_setting_env_vars_and_log_file


start_setting_env_vars_and_log_file()

if not getenv("READ_EMAIL_MESSAGE_RUN_CONTAINER"):
    from app.config_app import load_env_vars
    load_env_vars()

message = None

def minha_callback(ch, method, properties, body):
    global message
    message = body
    if not getenv("READ_EMAIL_MESSAGE_RUN_CONTAINER"):
        ch.stop_consuming()


async def connect():
    try:
        connection_parameters = ConnectionParameters(
            host=getenv("RABBITMQ_SERVER_URL"),
            port=getenv("RABBITMQ_SERVER_PORT"),
            credentials=PlainCredentials(
                username=getenv("RABBITMQ_USER"),
                password=getenv("RABBITMQ_PASSWORD")
            )
        )
        connection = BlockingConnection(connection_parameters)
        return connection
    except:
        raise Exception(f'Error connect RabbitMQ!')


async def rabbitmq_read_email():
    try:
        connection = await connect()
        channel = connection.channel()
    except:
        raise Exception(f'Error create channel')    

    try:
        channel.queue_declare(
            queue=getenv("RABBITMQ_READ_EMAIL_QUEUE"),
            durable=True
        )
    except:
        raise Exception(f'Error queue declare')    

    try:
        channel.basic_consume(
            queue=getenv("RABBITMQ_READ_EMAIL_QUEUE"),
            auto_ack=True,
            on_message_callback=minha_callback
        )
        channel.start_consuming()
        if not getenv("READ_EMAIL_MESSAGE_RUN_CONTAINER"):
            channel.close()
            connection.close()
        return message
    except:
        raise Exception(f'Error connect RabbitMQ!')    


if getenv("READ_EMAIL_MESSAGE_RUN_CONTAINER"):
    message = run(rabbitmq_read_email())
    info(f'message: {message}')

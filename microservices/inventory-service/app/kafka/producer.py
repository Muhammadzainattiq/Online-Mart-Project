import json
from typing import Annotated

from fastapi import Depends
from aiokafka import AIOKafkaProducer, AIOKafkaConsumer
from app.settings import KAFKA_BOOTSTRAP_SERVER

async def get_kafka_producer():
    producer = AIOKafkaProducer(bootstrap_servers = KAFKA_BOOTSTRAP_SERVER)
    await producer.start()
    try:
        yield producer
    finally:
        await producer.stop()


KAFKA_PRODUCER = Annotated[AIOKafkaProducer, Depends(get_kafka_producer)]

async def produce_message(topic:str, message:dict, producer:KAFKA_PRODUCER):
    json_message = json.dumps(message).encode('utf-8')
    await producer.send_and_wait(topic, json_message)
    print(">>>>>>>>>>>: produced_message", json_message)
    return message


#the fucntion specially written to be used to get producer in the lifespan to pass it to the consumer
async def init_kafka_producer():
    producer = AIOKafkaProducer(bootstrap_servers=KAFKA_BOOTSTRAP_SERVER)
    await producer.start()
    return producer


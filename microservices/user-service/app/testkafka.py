import json
from aiokafka import AIOKafkaProducer

async def get_kafka_producer():
    producer = AIOKafkaProducer(bootstrap_servers="broker:19092")
    await producer.start()
    try:
        yield producer
    finally:
        await producer.stop()

async def produce_message(topic: str, message: dict, producer: AIOKafkaProducer):
    json_message = json.dumps(message).encode('utf-8')
    await producer.send_and_wait(topic, json_message)
    print(">>>>>>>>>>>: produced_message", json_message)
    return message

message = "zain"

async def main():
    producer = AIOKafkaProducer(bootstrap_servers="localhost:9092")
    await producer.start()
    try:
        await produce_message("testing", message, producer)
    finally:
        await producer.stop()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())

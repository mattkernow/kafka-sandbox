from aiokafka import AIOKafkaProducer
import asyncio
import json

loop = asyncio.get_event_loop()


class KafkaDemoProducerError(Exception):
    pass


def serializer(value):
    try:
        return json.dumps(value).encode()
    except TypeError:
        raise KafkaDemoProducerError('Message must be dict type')


async def send_one():
    producer = AIOKafkaProducer(
        loop=loop, 
        bootstrap_servers='localhost:9092',
        # Wait only the broker leader to succeed
        acks=0,
        value_serializer=serializer,
        compression_type="gzip",)
    # Get cluster layout and initial topic/partition leadership information
    await producer.start()
    try:
        # Produce message
        response = await producer.send_and_wait("first_topic", {"ping": "pong"})
        print(f'\nRecieved new metadata...\nTopic: {response.topic}\nPartition: {response.partition}\nOffset: {response.offset}\nTimestamps: {response.timestamp}')
    finally:
        # Wait for all pending messages to be delivered or expire.
        await producer.stop()

def main():
    print('Starting...')
    loop.run_until_complete(send_one())
    print('Finishing...')

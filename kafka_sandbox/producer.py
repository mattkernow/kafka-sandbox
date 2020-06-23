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


async def send_one(num):
    producer = AIOKafkaProducer(
        loop=loop, 
        bootstrap_servers='localhost:9092',
        # Wait only the broker leader to succeed
        acks=1,
        value_serializer=serializer,
        compression_type="gzip",)
    # Get cluster layout and initial topic/partition leadership information
    await producer.start()
    try:
        # Produce message
        response = await producer.send_and_wait("first_topic", {"ping": "pong", "number": num})
        print(f'\nRecieved new metadata...\nTopic: {response.topic}\nPartition: {response.partition}\nOffset: {response.offset}\nTimestamps: {response.timestamp}')
    finally:
        # Wait for all pending messages to be delivered or expire.
        await producer.stop()


async def send_many():
    print('Starting...')
    all_msgs = [send_one(x) for x in range(100)]
    gather_all_msgs = await asyncio.gather(*all_msgs)
    print('Finishing...')


def main():
    loop.run_until_complete(send_many())

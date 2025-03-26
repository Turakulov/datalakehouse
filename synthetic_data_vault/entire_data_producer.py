import json
import pickle
import uuid
import logging
import asyncio
from aiokafka import AIOKafkaProducer
from confluent_kafka.admin import AdminClient, NewTopic

# from sdv.datasets.demo import get_available_demos, download_demo

log = logging.getLogger()
logging.basicConfig()

CONFIG = {
    "bootstrap.servers": "localhost:9092",
    # 'group.id': ''
}
TOPICS = [
    # "employees",
    #  "customers",
    # "products",
    "sales"
]
SEMAPHORE_LIMIT = 10000


async def delivery_report(err, msg):
    if err is not None:
        print(f"Error with message: {err}")
    else:
        print(
            f"Message sent to topic: {msg.topic} ; partition:[{msg.partition}] ; offset: {msg.offset}"
        )


async def execute_producer(producer, topic: str, data: str):
    try:
        key = str(uuid.uuid4()).encode("utf-8")
        value = data.encode("utf-8")
        await producer.send_and_wait(topic, key=key, value=value)
    except Exception as e:
        print(f"Failed to send message: {e}")


def check_topic_existence(topic_name):
    # Определить конфигурацию темы
    topic_config = {
        "cleanup.policy": "delete",
        "retention.ms": "2419200000",  # 4 недели
    }
    admin_client = AdminClient(CONFIG)
    topic_metadata = admin_client.list_topics()
    if topic_metadata.topics.get(topic_name) is None:
        # Создать экземпляр NewTopic
        new_topic = NewTopic(
            topic=topic_name,
            num_partitions=1,
            replication_factor=1,
            config=topic_config,
        )
        # Создать топик с помощью AdminClient
        admin_client.create_topics([new_topic])


async def produce_data():
    # data, metadata = download_demo(
    #     modality='multi_table',
    #     dataset_name= 'world_v1' #'SalesDB_v1'
    # )
    # print(data, data.keys(), type(data))
    # with open('data.pickle', 'wb') as handle:
    #     pickle.dump(data, handle, protocol=pickle.HIGHEST_PROTOCOL)
    #
    # print(metadata, metadata.keys(), type(metadata))
    # with open('metadata.json', 'w') as handle:
    #     json.dump(metadata, handle)

    with open("data.pickle", "rb") as handle:
        data = pickle.load(handle)

    for topic in TOPICS:
        check_topic_existence(topic)

    producer = AIOKafkaProducer(bootstrap_servers=CONFIG["bootstrap.servers"])
    await producer.start()

    # semaphore = asyncio.Semaphore(SEMAPHORE_LIMIT)

    # async def limited_produce(topic_name, json_data):
    #     async with semaphore:
    #         await execute_producer(producer, topic_name, json_data)

    try:
        tasks = []
        for t in TOPICS:
            for i in range(data[t.capitalize()].shape[0]):
                await execute_producer(
                    producer, t, data[t.capitalize()].iloc[i].to_json()
                )
                # tasks.append(
                #     limited_produce(
                #         topic_name=t, json_data=
                #     )
                # )

        # await asyncio.gather(*tasks)
    finally:
        await producer.stop()


if __name__ == "__main__":
    asyncio.run(produce_data())

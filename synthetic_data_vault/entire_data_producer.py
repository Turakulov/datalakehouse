import json
import pickle
import uuid
import logging
from confluent_kafka import Producer
from confluent_kafka.admin import AdminClient, NewTopic

# from sdv.datasets.demo import get_available_demos, download_demo
from confluent_kafka import Consumer, TopicPartition

CONFIG = {
    "bootstrap.servers": "localhost:9092",
    # 'group.id': ''
}


def delivery_report(err, msg):
    if err is not None:
        print(f"Error with message: {err}")
    else:
        print(
            f"Message sent to topic: {msg.topic()} ; partition:[{msg.partition()}] ; offset: {msg.offset()}"
        )


def execute_producer(producer, topic: str, data: str):
    producer.produce(topic, key=str(uuid.uuid4()), value=data, callback=delivery_report)
    producer.poll(0)
    producer.flush()


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


def check_topic_existance(topic_name):
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
            topic_name, num_partitions=1, replication_factor=1, config=topic_config
        )
        # Создать топик с помощью AdminClient
        admin_client.create_topics([new_topic])


with open("data.pickle", "rb") as handle:
    data = pickle.load(handle)


check_topic_existance("employees")
check_topic_existance("customers")
check_topic_existance("products")
check_topic_existance("sales")

producer = Producer(CONFIG)
for i in range(data["Employees"].shape[0]):
    execute_producer(
        producer=producer, topic="employees", data=data["Employees"].iloc[i].to_json()
    )

for i in range(data["Customers"].shape[0]):
    execute_producer(
        producer=producer, topic="customers", data=data["Customers"].iloc[i].to_json()
    )

for i in range(data["Products"].shape[0]):
    execute_producer(
        producer=producer, topic="products", data=data["Products"].iloc[i].to_json()
    )

# for i in range(data['Sales'].shape[0]):
#     execute_producer(producer=producer, topic='sales', data=data['Sales'].iloc[i].to_json())

import json
import pickle
from confluent_kafka import Producer
import logging
import uuid
from sdv.datasets.demo import get_available_demos, download_demo
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

with open("data.pickle", "rb") as handle:
    data = pickle.load(handle)

producer = Producer(CONFIG)
for i in range(data["Employees"].shape[0]):
    execute_producer(
        producer=producer, topic="employees", data=data["Employees"].iloc[i].to_json()
    )

# for i in range(data['Customers'].shape[0]):
#     execute_producer(producer=producer, topic='customers', data=data['Customers'].iloc[i].to_json())
#
# for i in range(data['Products'].shape[0]):
#     execute_producer(producer=producer, topic='products', data=data['Products'].iloc[i].to_json())
#
# for i in range(data['Sales'].shape[0]):
#     execute_producer(producer=producer, topic='sales', data=data['Sales'].iloc[i].to_json())

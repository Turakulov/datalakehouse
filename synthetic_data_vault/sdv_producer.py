import pickle
import json
import random
from confluent_kafka import Producer
from faker import Faker
import time
import logging
import uuid
import string

from confluent_kafka import Consumer, TopicPartition


CONFIG = {"bootstrap.servers": "localhost:9092", "group.id": ""}
AVAILABLE_CUSTOMERS = range(1, 1000)
AVAILABLE_EMPLOYEES = range(1, 100)
AVAILABLE_PRODUCTS = range(1, 100)
SLEEP_TIME = 60
fake = Faker(["en_US", "en_PH"])


class Customer:

    def __init__(self):
        self.CustomerID = random.choice(AVAILABLE_CUSTOMERS)
        self.MiddleInitial = random.choice(string.ascii_letters).upper()
        self.FirstName = fake.first_name()
        self.LastName = fake.last_name()

    def get_row(self) -> dict:
        return {
            "CustomerID": self.CustomerID,
            "MiddleInitial": self.MiddleInitial,
            "FirstName": self.FirstName,
            "LastName": self.LastName,
        }


class Employee:
    def __init__(self):
        self.EmployeeID = random.choice(AVAILABLE_EMPLOYEES)
        self.MiddleInitial = random.choice(string.ascii_letters).upper()
        self.FirstName = fake.first_name()
        self.LastName = fake.last_name()

    def get_row(self) -> dict:
        return {
            "EmployeeID": self.EmployeeID,
            "MiddleInitial": self.MiddleInitial,
            "FirstName": self.FirstName,
            "LastName": self.LastName,
        }


class Product:
    def __init__(self):
        self.EmployeeID = random.choice(AVAILABLE_PRODUCTS)
        self.Name = fake.random_company_product()
        self.Price = round(random.uniform(1, 10000), 2)

    def get_row(self) -> dict:
        return {"EmployeeID": self.EmployeeID, "Name": self.Name, "Price": self.Price}


class Sale:
    def __init__(self):
        self.CustomerID = random.choice(AVAILABLE_CUSTOMERS)
        self.SalesPersonID = random.choice(AVAILABLE_EMPLOYEES)
        self.SalesID = int(time.time())
        self.ProductID = random.choice(AVAILABLE_PRODUCTS)
        self.Quantity = random.randint(1, 50)

    def get_row(self) -> dict:
        return {
            "CustomerID": self.CustomerID,
            "SalesPersonID": self.SalesPersonID,
            "SalesID": self.SalesID,
            "ProductID": self.ProductID,
            "Quantity": self.Quantity,
        }


def delivery_report(err, msg):
    if err is not None:
        print(f"Error with message: {err}")
    else:
        print(f"Message sent to topic: {msg.topic()} [{msg.partition()}]")


def execute_producer(topic: str, data: dict):
    producer = Producer(CONFIG)
    producer.produce(
        topic, key=str(uuid.uuid4()), value=json.dumps(data), callback=delivery_report
    )
    producer.poll(0)
    producer.flush()


def get_kafka_topics_cnt(topic_name: str, partition_key: int = 0):
    consumer = Consumer(CONFIG)
    topic_partition = TopicPartition(topic_name, partition_key)
    low_offset, high_offset = consumer.get_watermark_offsets(topic_partition)
    partition_size = high_offset - low_offset
    return partition_size


# with open('C:\\Users\\akram\\PycharmProjects\\datalakehouse\\synthetic_data_vault\\data.pickle', 'rb') as handle:
#     data = pickle.load(handle)


i = 0
while True:

    cnt_kafka = get_kafka_topics_cnt("employees")
    print(cnt_kafka)
    break
    # if cnt_kafka:
    # c1 = Customer()
    # e1 = Employee()
    # p1 = Product()
    # s1 = Sale()
    #
    # # execute_producer(topic='customers', data=c1.get_row())
    # execute_producer(topic='employees', data=e1.get_row())
    # # execute_producer(topic='products', data=p1.get_row())
    # # execute_producer(topic='sales', data=s1.get_row())
    #
    # # print(f'Sleeping {SLEEP_TIME} seconds!')
    # # time.sleep(SLEEP_TIME)
    # i += 1
    # if i > 10:
    #
    #     break

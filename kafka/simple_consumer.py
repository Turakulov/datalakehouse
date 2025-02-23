from confluent_kafka import Consumer, KafkaException

conf = {
    "bootstrap.servers": "localhost:9092",
    "group.id": "0",
    "auto.offset.reset": "earliest",
}

consumer = Consumer(conf)

topic = "demo"
consumer.subscribe([topic])

try:
    while True:
        msg = consumer.poll(timeout=1.0)
        if msg is None:
            continue
        if msg.error():
            if msg.error().code() == KafkaError._PARTITION_EOF:
                print(f"Конец раздела {msg.topic()} [{msg.partition()}]")
            elif msg.error():
                raise KafkaException(msg.error())
        else:
            print(
                f'Получено сообщение: {msg.value().decode("utf-8")}  , {msg.timestamp()}'
            )
finally:
    consumer.close()

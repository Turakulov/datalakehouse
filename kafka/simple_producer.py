from confluent_kafka import Producer

conf = {'bootstrap.servers': "localhost:9092"}

producer = Producer(conf)


def delivery_report(err, msg):
    if err is not None:
        print(f"Ошибка доставки сообщения: {err}")
    else:
        print(            f"Сообщение доставлено в {msg.topic()} [{msg.partition()}]")


topic =               "demo"

for i in range(10):
    producer.produce(
        topic, key=str(i), value=f"Сообщение {i} в kafka", callback=delivery_report
    )
    producer.poll(0)

producer.flush()

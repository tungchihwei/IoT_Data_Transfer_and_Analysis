from confluent_kafka import Consumer, KafkaError
from hdfs import InsecureClient
import json
import time


HDFS_CONFIG = {
    "host": "127.0.1.1",
    "port": 9870,
    "user": "hadoop"
}
HDFS_PATH = "/test/"

def consume_kafka_messages(bootstrap_servers, group_id, topic, hdfs_client):
    consumer_conf = {
        'bootstrap.servers': bootstrap_servers,
        'group.id': group_id,
        'auto.offset.reset': 'latest'
    }

    consumer = Consumer(consumer_conf)
    consumer.subscribe([topic])

    try:
        while True:
            msg = consumer.poll(1.0)

            if msg is None:
                continue
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    continue
                else:
                    print(msg.error())
                    break
            iot_data = msg.value().decode('utf-8')
            # print(iot_data)
            file = HDFS_PATH + str(round(time.time())) + "_test.json"
            with hdfs_client.write(file, overwrite=True) as writer:
                writer.write(iot_data)

    except KeyboardInterrupt:
        consumer.close()
    finally:
        consumer.close()

if __name__ == '__main__':
    bootstrap_servers = 'localhost:9092/'
    consumer_group_id = 'iot'
    kafka_topic = 'iot'

    hdfs_client = InsecureClient(
        f"http://{HDFS_CONFIG['host']}:{HDFS_CONFIG['port']}",
        user=HDFS_CONFIG["user"]
    )
    consume_kafka_messages(bootstrap_servers, consumer_group_id, kafka_topic, hdfs_client)

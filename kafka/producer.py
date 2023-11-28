from confluent_kafka import Producer
import threading
from datetime import datetime
import random
import json, time

SUCCESS = [
    {
        "type": "transfer_in",
        "detail": "",
        "delay": 1,
    },
    {
        "type": "testing",
        "detail": "",
        "delay": 2
    },
    {
        "type": "test_result",
        "detail": "pass",
        "delay": 0
    },
    {
        "type": "transfer_out",
        "detail": "",
        "delay": 1
    }
]

FAILED = [
    {
        "type": "transfer_in",
        "detail": "",
        "delay": 1,
    },
    {
        "type": "testing",
        "detail": "",
        "delay": 2
    },
    {
        "type": "test_result",
        "detail": "failed",
        "delay": 0
    },
    {
        "type": "transfer_bin",
        "detail": "",
        "delay": 1
    }
]

IOT_DATA = [FAILED, SUCCESS]
KAFKA_IP = "127.0.1.1:9092"
KAFKA_TOPIC = "iot"

def delivery_report(err, msg):
    if err is not None:
        print("Message delivery failed: {}".format(err))
    # else:
    #     print("Message delivered to {} [{}]".format(msg.topic(), msg.partition()))

def produce_kafka_message(ip, topic, message):
    producer = Producer({'bootstrap.servers': ip})
    producer.produce(topic, value=message, callback=delivery_report)
    producer.flush()

def iot_process_job(num):
    while True:
        product_id = f"{num}_{str(round(time.time()))}"
        choices = [0, 1]
        probability_of_one = random.randint(60, 80) / 100
        weights = [1 - probability_of_one, probability_of_one]
        i = random.choices(choices, weights=weights, k=1)[0]
        for iot in IOT_DATA[i]:
            send_data = {
                "type": iot["type"],
                "detail": iot["detail"],
                "product_id": product_id,
                "action_timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            send_data = json.dumps(send_data)
            produce_kafka_message(KAFKA_IP, KAFKA_TOPIC, send_data)
            time.sleep(iot["delay"])

if __name__ == '__main__':
    iot_process = [threading.Thread(target=iot_process_job, args=(i,)) for i in range(3)]
    for p in iot_process:
        p.start()
        time.sleep(1)

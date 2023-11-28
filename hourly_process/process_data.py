import json
import time
import math
import redis
import paramiko
from pyhive import hive
from datetime import datetime
from apscheduler.schedulers.blocking import BlockingScheduler

SSH_IP = "127.0.1.1"
SSH_USERNAME = "hadoop"
SSH_PASSWORD = "hadoop"

HIVE_CONFIG = {
    "host": "127.0.1.1",
    "port": 10000,
    "database": "test",
    "username": "hive"
}

UPH = """
SELECT type FROM iot
WHERE type = 'transfer_out'
AND action_timestamp >= current_timestamp - interval 1 hour
"""

YIELD = """
SELECT detail FROM iot
WHERE type = 'test_result'
AND action_timestamp >= current_timestamp - interval 1 hour
"""

REDIS_CONFIG = {
    "host": "127.0.1.1",
    "port": 6379,
    "password": "test"
}



def execute_ssh_command(ssh, command):
    stdin, stdout, stderr = ssh.exec_command(command)
    return stdout.readlines(), stderr.readlines()

def load_to_hive():
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(hostname=SSH_IP, username=SSH_USERNAME, password=SSH_PASSWORD)

    load_data_command = '/home/hadoop/apache-hive-3.1.2-bin/bin/hive -e "load data inpath \'/test\' into table test.iot;"'
    output, error = execute_ssh_command(ssh_client, load_data_command)
    # for out in output:
    #     print(out)
    print(error)
    ssh_client.close()

def execute_hive_query(query):
    conn = hive.Connection(
        host=HIVE_CONFIG["host"],
        port=HIVE_CONFIG["port"],
        username=HIVE_CONFIG["username"],
        # password=HIVE_CONFIG['password'],
        database=HIVE_CONFIG["database"]
    )
    results = []
    cursor_description = []
    cursor = conn.cursor()
    try:
        cursor.execute(query)

        results = cursor.fetchall()
        cursor_description= cursor.description
    except Exception as e:
        print(f"Error executing Hive query: {str(e)}")

    finally:
        cursor.close()
        conn.close()
    return results, [desc[0] for desc in cursor_description]

def save_to_redis(data, current_time):
    redis_client = redis.StrictRedis(
        host=REDIS_CONFIG["host"],
        port=REDIS_CONFIG["port"],
        password=REDIS_CONFIG["password"],
        decode_responses=True
    )
    json_data = json.dumps(data)
    key = math.floor(current_time.timestamp())
    redis_client.set(key, json_data)

    stored_data = redis_client.get('iot')
    print(stored_data)

def drop_and_create():
    drop_command = "drop table iot"
    create_command = """
    CREATE TABLE iot (
        type string,
        detail string,
        product_id string,
        action_timestamp timestamp
    )
    ROW FORMAT SERDE 'org.apache.hive.hcatalog.data.JsonSerDe'
    WITH SERDEPROPERTIES ('timestamp.formats'='yyyy-MM-dd HH:mm:ss')
    """
    execute_hive_query(drop_command)
    execute_hive_query(create_command)

def job():
    drop_and_create()
    load_to_hive()
    uph_data, _ = execute_hive_query(UPH)
    uph_value = len(uph_data)
    yield_data, _ = execute_hive_query(YIELD)
    yield_value = 0
    if len(yield_data) > 0:
        yield_value = len(list(filter(lambda x: x[0] == "pass", yield_data))) / len(yield_data)
    current_time = datetime.now()
    iot_analyze = {
        "timestamp": current_time.strftime('%Y-%m-%d %H:%M:%S'),
        "uph": uph_value,
        "yield": yield_value,
    }
    # print(iot_analyze)
    save_to_redis(iot_analyze, current_time)

if __name__ == '__main__':
    # Asia/Taipei
    job()
    scheduler = BlockingScheduler(timezone="Asia/Taipei")
    scheduler.add_job(job, 'interval', hours=1)
    scheduler.start()

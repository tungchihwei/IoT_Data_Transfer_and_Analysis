import uvicorn
from fastapi import FastAPI
import json
import redis
from datetime import datetime

app = FastAPI()
REDIS_CLIENT = redis.StrictRedis(
    host="localhost",
    port=6379,
    password="test",
    decode_responses=True
)

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/iot_data/")
async def index(start_time: int, end_time: int):
    keys_in_range = REDIS_CLIENT.keys('*')
    data_in_range = []

    for key in keys_in_range:
        try:
            timestamp = int(key)
        except:
            continue
        if start_time <= timestamp <= end_time:
            data = REDIS_CLIENT.get(key)
            if data:
                row_data = json.loads(data)
                row_data["timestamp"] = datetime.strptime(row_data["timestamp"], '%Y-%m-%d %H:%M:%S').timestamp()
                row_data["yield"] = round(row_data["yield"] * 100, 2)
                data_in_range.append(row_data)
    return data_in_range

if __name__ == "__main__":
   uvicorn.run("main:app", host="127.0.0.1", port=5000, reload=True)


# import redis
# from datetime import datetime

# def filter_data_by_timestamp(redis_client, key_pattern, start_timestamp, end_timestamp):
#     cursor = 0
#     keys = []

#     while True:
#         cursor, partial_keys = redis_client.scan(cursor, match=f'*{key_pattern}*', count=10)
#         keys.extend(partial_keys)

#         if cursor == 0:
#             break

#     filtered_data = {}

#     for key in keys:
#         data = redis_client.get(key)
#         print(data)
#         if data:
#             # data = data.decode('utf-8')
#             data_dict = eval(data)  # Convert the string to a dictionary
#             action_timestamp_str = data_dict.get('timestamp')
            
#             if action_timestamp_str:
#                 action_timestamp = datetime.strptime(action_timestamp_str, '%Y-%m-%d %H:%M:%S')
#                 if start_timestamp <= action_timestamp <= end_timestamp:
#                     filtered_data[key] = data_dict

#     return filtered_data

# # Example usage
# redis_host = 'localhost'
# redis_port = 6379
# redis_client = redis.StrictRedis(host=redis_host, port=redis_port, password="test", decode_responses=True)

# key_pattern = 'iot'
# start_timestamp = datetime.strptime('2023-11-26 15:00:00', '%Y-%m-%d %H:%M:%S')
# end_timestamp = datetime.strptime('2023-11-26 20:00:00', '%Y-%m-%d %H:%M:%S')

# filtered_data = filter_data_by_timestamp(redis_client, key_pattern, start_timestamp, end_timestamp)

# print("Filtered Data:")
# print(filtered_data)


# import json
# import redis
# from datetime import datetime

# def get_data_in_time_range(redis_client, start_timestamp, end_timestamp):
#     keys_in_range = redis_client.keys('*')
#     data_in_range = []

#     for key in keys_in_range:
#         try:
#             timestamp = int(key)
#         except:
#             continue
#         if start_timestamp.timestamp() <= timestamp <= end_timestamp.timestamp():
#             data = redis_client.get(key)
#             if data:
#                 row_data = json.loads(data)
#                 row_data["timestamp"] = datetime.strptime(row_data["timestamp"], '%Y-%m-%d %H:%M:%S').timestamp()
#                 row_data["yield"] = round(row_data["yield"] * 100, 2)
#                 data_in_range.append(row_data)
#     return data_in_range


# # Example usage
# redis_host = 'localhost'
# redis_port = 6379
# redis_client = redis.StrictRedis(host=redis_host, port=redis_port, password="test", decode_responses=True)

# start_timestamp = datetime.strptime('2023-11-26 18:00:00', '%Y-%m-%d %H:%M:%S')
# end_timestamp = datetime.strptime('2023-11-26 20:00:00', '%Y-%m-%d %H:%M:%S')

# data_in_range = get_data_in_time_range(redis_client, start_timestamp, end_timestamp)

# print("Data in Time Range:")
# print(data_in_range)
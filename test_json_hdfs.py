from hdfs import InsecureClient
import pyarrow as pa
import pyarrow.parquet as pq
import pandas as pd
import json
from pyarrow.fs import HadoopFileSystem
import time

HDFS_CONFIG = {
    "host": "localhost",
    "port": 9870,
    "user": "hadoop"
}

HDFS_PATH = "/test/"

def store_dict_in_hdfs(dictionary, hdfs_path):
    # Connect to HDFS
    hdfs_client = InsecureClient(
        f"http://{HDFS_CONFIG['host']}:{HDFS_CONFIG['port']}",
        user=HDFS_CONFIG["user"]
    )

    # Convert dictionary to JSON string
    json_data = json.dumps(dictionary)
    # print(json_data.values())

    # data = pd.DataFrame([dictionary])
    # table = pa.Table.from_pandas(data, schema=None)

    # df = pd.DataFrame([my_dict])
    # table = pa.Table.from_pandas(df)
    # hdfs_filesystem = HadoopFileSystem(host=HDFS_CONFIG['host'], port=HDFS_CONFIG['port'], user=HDFS_CONFIG["user"])

    # # pq.write_to_dataset(table, root_path=hdfs_path, compression='snappy')
    # with pq.ParquetWriter(hdfs_path, table.schema, filesystem=hdfs_filesystem) as writer:
    #     writer.write_table(table)

    print(str(round(time.time())))
    file = HDFS_PATH + str(round(time.time())) + "_test.json"
    with hdfs_client.write(file, overwrite=True) as writer:
            writer.write(json_data)

    # file_exists = hdfs_client.status(file, strict=False) is not None

    # if not file_exists:
    #     with hdfs_client.write(file, overwrite=True) as writer:
    #         writer.write(json_data)
    # else:
    #     # Write JSON data to HDFS
    #     with hdfs_client.write(HDFS_PATH, append=True) as writer:
    #         writer.write(json_data + "\n")

if __name__ == '__main__':
    # Example dictionary
    my_dict = {'name': 'John Doe', 'age': 30, 'city': 'New York'}

    # Specify the HDFS path where you want to store the dictionary
    hdfs_path = f"{HDFS_PATH}/test.json"

    # Store the dictionary in HDFS
    store_dict_in_hdfs(my_dict, hdfs_path)

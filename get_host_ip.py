# from pyhive import hive
# # import pyarrow.parquet as pq
# import pandas as pd
# from TCLIService.ttypes import TOperationState

# HIVE_CONFIG = {
#     "host": "127.0.1.1",
#     "port": 10000,
#     "database": "test",
#     "username": "hive"
# }


# UPH = "select type from iot where type in ('transfer_in', 'transfer_out') and action_timestamp >= current_timestamp - interval 1 hour"

# def execute_hive_query(query):
#     # Connect to Hive
#     conn = hive.Connection(
#         host=HIVE_CONFIG['host'],
#         port=HIVE_CONFIG['port'],
#         username=HIVE_CONFIG['username'],
#         # password=HIVE_CONFIG['password'],
#         # database=HIVE_CONFIG['database']
#     )

#     # Create a Hive cursor
#     cursor = conn.cursor()

#     try:
#         # Execute the Hive query
#         cursor.execute(query)

#         results = cursor.fetchall()

#         # # Check the operation status
#         # status = cursor.poll().operationState
#         # while status in (TOperationState.INITIALIZED_STATE, TOperationState.RUNNING_STATE):
#         #     # Poll for the operation to complete
#         #     status = cursor.poll().operationState

#         # if status == TOperationState.FINISHED_STATE:
#         #     print("Hive query executed successfully.")
#         # else:
#         #     print(f"Hive query failed with status: {status}")

#         # # Fetch the results
#         results = cursor.fetchall()

#         # # Convert the results to a Pandas DataFrame for easy manipulation
#         # df = pd.DataFrame(results, columns=[desc[0] for desc in cursor.description])

#         # return df
#         return results
    
#     except Exception as e:
#         print(f"Error executing Hive query: {str(e)}")

#     finally:
#         # Close the Hive cursor and connection
#         cursor.close()
#         conn.close()

# if __name__ == '__main__':
#     # Example Hive query to process data in MySQL via Hive

#     hive_query = [
#         # "show databases",
#         # "use test",
#         # "show tables",
#         "load data inpath '/test' into table test.json_data"]

#     # Execute the Hive query and get the results
#     for q in hive_query:
#         print(q)
#         processed_data = execute_hive_query(q)

#     # Print the processed data
#         print(processed_data)


import socket

def get_user_ip(username):
    try:
        # Get the hostname associated with the user
        hostname = socket.gethostname()

        # Get the IP address associated with the hostname
        ip_address = socket.gethostbyname(hostname)

        return ip_address
    except Exception as e:
        print(f"Error: {e}")
        return None

# Replace "hadoop" with the username for which you want to get the IP
target_user = "test"
ip_address = get_user_ip(target_user)

if ip_address:
    print(f"The IP address of user '{target_user}' is: {ip_address}")
else:
    print(f"Failed to retrieve the IP address for user '{target_user}'")


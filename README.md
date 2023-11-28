# IoT_Data_Transfer_and_Analysis

## ETL Architecture
<img width="952" alt="image" src="https://github.com/tungchihwei/IoT_Data_Transfer_and_Analysis/assets/31777680/a6d0ea20-9bf0-44f5-b24e-3fd92682c8c8">

## HDFS Command
> ### Start the Hadoop cluster
>> start-dfs.sh

> ### Start the node manager and resource manager
>> start-yarn.sh

> ### Name node leave from safe mode
>> hadoop dfsadmin -safemode leave

> ### To verify whether the services are running
>> jps

> ### Access the Hadoop web interface
>> http://server-IP:9870

> ### Start all Hadoop services
>> start-all.sh

> ### Stop all Hadoop services
>> stop-all.sh

> ### Create Directory
> Create a directory within the HDFS storage layer.
>> hdfs dfs -mkdir /name

> ### Add write and execute permissions to "name" group members:
>> hdfs dfs -chmod g+w /name

> ### Check permissions
>> hdfs dfs -ls /


## HDFS Command
> ### Start Hive service
>> nohup hive --service hiveserver2 > hiveserver2.log 2>&1 &


## Kafka Monitoring
![Kafka_Monitor](https://github.com/tungchihwei/IoT_Data_Transfer_and_Analysis/assets/31777680/43ecb770-0c2e-4cee-ad6a-d13e5f19ee18)

## Redis Monitoring
![Redis_Monitor](https://github.com/tungchihwei/IoT_Data_Transfer_and_Analysis/assets/31777680/a4052057-8a82-445d-a304-2a90b6193089)

## Final Visualization
![Visual](https://github.com/tungchihwei/IoT_Data_Transfer_and_Analysis/assets/31777680/9d5003b0-38e1-4470-8699-f3d3d459a07f)




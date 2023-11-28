# IoT_Data_Transfer_and_Analysis

## ETL Architecture
<img width="952" alt="image" src="https://github.com/tungchihwei/IoT_Data_Transfer_and_Analysis/assets/31777680/a6d0ea20-9bf0-44f5-b24e-3fd92682c8c8">

## HDFS Command
> ### Start the Hadoop cluster
>> start-dfs.sh

> ### Start the node manager and resource manager
>> start-yarn.sh

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

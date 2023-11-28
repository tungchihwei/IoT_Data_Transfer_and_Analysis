#!/bin/bash

start-all.sh
hadoop dfsadmin -safemode leave
nohup hive --service hiveserver2 > hiveserver2.log 2>&1 &

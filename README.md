# Ansible role for kafka

# Requirements
- Centos

# Usage
```
Simply put this role to the "roles"-folder and use the following playbook.yml:
---

- hosts: localhost
  roles:
    - kafka-centos

```

# Testing Kafka

```
root@centos7 ~]# /usr/local/kafka/bin/kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic TestTopic
Created topic "TestTopic".
[root@centos7 ~]# cd /usr/local/kafka/
[root@centos7 kafka]# echo "Hello, World" | bin/kafka-console-producer.sh --broker-list localhost:9092 --topic TestTopic > /dev/null
[root@centos7 kafka]# bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic TestTopic --from-beginning
Hello, World
^CProcessed a total of 1 messages
```

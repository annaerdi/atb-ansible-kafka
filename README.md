# Ansible role for kafka

# Requirements
- Ubuntu

# Configuration

The following defaults can be used:

```
kafka_server_template: server.properties.j2
kafka_url: http://mirror.klaus-uwe.me/apache/kafka/2.6.2/kafka_2.13-2.6.2.tgz
kafka_version: kafka_2.13-2.6.2
kafka_heapopts: '-Xmx1G -Xms1G'
kafka_keydir: '/usr/local/kafka/keydir'
kafka_ssl_serverkeystorepw: 'Enoog9queiHeecu'
kafka_ssl_serverkeypass: '{{kafka_ssl_serverkeystorepw}}'
kafka_ssl_cakeypw: 'iceDaig8Ahghija'
kafka_ssl_servertruststorepw: 'thaeFa9genguu1o'
kafka_ssl_clienttruststorepw: 'eexuongeeWah3vi'
kafka_logdir: '/var/lib/kafka'
kafka_brokerid: 0
# The minimum age of a log file to be eligible for deletion due to age (in hours)
kafka_log_retention: 96
kafka_zookeeper: localhost:2181
kafka_logsegment_bytes: 1073741824
kafka_log_retention_check_interval: 300000
kafka_listeners: 'INTERNAL://localhost:9093,EXTERNAL://:9092'
kafka_advertised_listeners: 'INTERNAL://localhost:9093,EXTERNAL://:9092'
kafka_listener_security_proto_map: 'INTERNAL:SSL,EXTERNAL:PLAINTEXT,CONTROLLER:SSL'
```

# Usage

Simply put this role to the "roles"-folder and use the following playbook.yml:
```
---

- hosts: localhost
  roles:
    - kafka

```

## Install Ansible and deploy Kafka:

Ubuntu:
```
apt install ansible git

git clone https://@git-service.ait.ac.at/ict-caiscluster/aecid/tools/ansible/kafka.git /etc/ansible/roles/kafka

cat > /etc/ansible/kafka.yml << EOF
---
- hosts: localhost
  roles:
    - kafka
EOF

cd /etc/ansible
ansible-playbook kafka.yml
```


Centos(CURRENTLY NOT WORKING WITH THIS ROLE!):
```
yum install epel-release.noarch
yum install python36 python36-devel python36-pip ansible git

git clone https://@git-service.ait.ac.at/ict-caiscluster/aecid/tools/ansible/kafka.git /etc/ansible/roles/kafka

cat > /etc/ansible/kafka.yml << EOF
---
- hosts: localhost
  roles:
    - kafka
EOF

cd /etc/ansible
ansible-playbook kafka.yml
```

### Post-Installation
```
systemctl start kafka
systemctl start zookeeper
systemctl enable kafka
systemctl enable zookeeper
```

# Testing Kafka

## Using the PLAINTEXT-Listener:

```
root@localhost ~]# /usr/local/kafka/bin/kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic TestTopic
Created topic "TestTopic".
[root@localhost ~]# cd /usr/local/kafka/
[root@localhost kafka]# echo "Hello, World" | /usr/local/kafka/bin/kafka-console-producer.sh --broker-list localhost:9092 --producer.config /usr/local/kafka/config/producer.properties --topic TestTopic > /dev/null
[root@localhost kafka]# /usr/local/kafka/bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --consumer.config /usr/local/kafka/config/consumer.properties --topic TestTopic --from-beginning
Hello, World
^CProcessed a total of 1 messages
```

## Using the SSL-Listener:

```
root@localhost ~]# /usr/local/kafka/bin/kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic TestTopic
Created topic "TestTopic".
[root@localhost ~]# cd /usr/local/kafka/
[root@localhost kafka]# echo "Hello, World" | /usr/local/kafka/bin/kafka-console-producer.sh --broker-list localhost:9093 --producer.config /usr/local/kafka/config/client-ssl.properties --topic TestTopic > /dev/null
[root@localhost kafka]# /usr/local/kafka/bin/kafka-console-consumer.sh --bootstrap-server localhost:9093 --consumer.config /usr/local/kafka/config/client-ssl.properties --topic TestTopic --from-beginning
Hello, World
^CProcessed a total of 1 messages
```

## Starting a consumer:

```
/usr/local/kafka/bin/kafka-console-consumer.sh --topic TestTopic --bootstrap-server localhost:9092
```

## Starting a producer:

```
echo "Hallo Welt" | /usr/local/kafka/bin/kafka-console-producer.sh --topic TestTopic --bootstrap-server localhost:9092
```

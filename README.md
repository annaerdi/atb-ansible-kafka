# Ansible role for kafka

# Requirements
- Centos

# Usage

Simply put this role to the "roles"-folder and use the following playbook.yml:
```
---

- hosts: localhost
  roles:
    - kafka-centos

```

## Install Ansible and deploy Kafka:

```
yum install epel-release.noarch
yum install python36 python36-devel python36-pip ansible git

git clone https://git-service.ait.ac.at/hotwagnerw/ansible-kafka-centos.git /etc/a
nsible/roles/kafka-centos

cat > /etc/ansible/kafka.yml << EOF
---
- hosts: localhost
  roles:
    - kafka-centos
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
root@centos7 ~]# /usr/local/kafka/bin/kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic TestTopic
Created topic "TestTopic".
[root@centos7 ~]# cd /usr/local/kafka/
[root@centos7 kafka]# echo "Hello, World" | /usr/local/kafka/bin/kafka-console-producer.sh --broker-list localhost:9092 --producer.config examples/kafka-client-plaintext.conf --topic TestTopic > /dev/null
[root@centos7 kafka]# /usr/local/kafka/bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --consumer.config examples/kafka-client-plaintext.conf --topic TestTopic --from-beginning
Hello, World
^CProcessed a total of 1 messages
```

## Using the SSL-Listener:

```
root@centos7 ~]# /usr/local/kafka/bin/kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic TestTopic
Created topic "TestTopic".
[root@centos7 ~]# cd /usr/local/kafka/
[root@centos7 kafka]# echo "Hello, World" | /usr/local/kafka/bin/kafka-console-producer.sh --broker-list localhost:9092 --producer.config examples/kafka-client.conf --topic TestTopic > /dev/null
[root@centos7 kafka]# /usr/local/kafka/bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --consumer.config examples/kafka-client.conf --topic TestTopic --from-beginning
Hello, World
^CProcessed a total of 1 messages
```


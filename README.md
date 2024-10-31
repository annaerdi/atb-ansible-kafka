# Ansible role for kafka

This role installs the kafka message broker. This installation 
is rather meant for testbeds and not for production use cases.

# Requirements
- Ubuntu

# Configuration

The following defaults can be used:

```
kafka_openjdk: 'openjdk-21-jdk'
kafka_server_template: server.properties.j2
kafka_url: https://downloads.apache.org/kafka/3.7.0/kafka_2.13-3.7.0.tgz
kafka_version: kafka_2.13-3.7.0
kafka_heapopts: '-Xmx1G -Xms1G'
kafka_dir: '/usr/local/kafka'
kafka_keydir: '{{kafka_dir}}/keydir'
kafka_ssl_serverkeystorepw: 'Enoog9queiHeecu'
kafka_ssl_serverkeypass: '{{kafka_ssl_serverkeystorepw}}'
kafka_ssl_cakeypw: 'iceDaig8Ahghija'
kafka_ssl_servertruststorepw: 'thaeFa9genguu1o'
kafka_ssl_clienttruststorepw: 'eexuongeeWah3vi'
kafka_logdir: '/var/lib/kafka'
kafka_zoodir: '/var/lib/zookeeper'
kafka_brokerid: 0
kafka_auto_create_topics: true
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

git clone https://github.com/ait-testbed/atb-ansible-kafka.git /etc/ansible/roles/kafka

cat > /etc/ansible/kafka.yml << EOF
---
- hosts: localhost
  roles:
    - kafka
EOF

cd /etc/ansible
ansible-playbook kafka.yml
```


# Testing Kafka

## Using the PLAINTEXT-Listener:

```
root@localhost ~]# /usr/local/kafka/bin/kafka-topics.sh --create --bootstrap-server localhost:9092 --topic TestTopic
Created topic "TestTopic".
[root@localhost ~]# cd /usr/local/kafka/
[root@localhost kafka]# echo "Hello, World" | /usr/local/kafka/bin/kafka-console-producer.sh --broker-list localhost:9092 --producer.config /usr/local/kafka/config/producer.properties --topic TestTopic > /dev/null
[root@localhost kafka]# /usr/local/kafka/bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --consumer.config /usr/local/kafka/config/consumer.properties --topic TestTopic --from-beginning
Hello, World
^CProcessed a total of 1 messages
```

## Using the SSL-Listener:

```
root@localhost ~]# /usr/local/kafka/bin/kafka-topics.sh --create --bootstrap-server localhost:9092 --topic TestTopic
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
## Example playbook:

```yaml
- name: Install Kafka Host
  hosts: all
  remote_user: ubuntu
  become: true
  tasks:
    - name: Install Reposerver Packages
      ansible.builtin.apt:
          pkg:
            - curl
            - netcat-traditional
          update_cache: yes
  roles:
          - role: hostname
            vars:
                  hostname: kafka
                  hostname_ip: 192.168.100.10
                  hostname_fqdn: kafka.aecid-testbed.local
          - role: kafka
```

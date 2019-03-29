#!/usr/bin/env  python36

# Docs: https://readthedocs.org/projects/kafka-python/downloads/pdf/master/

from kafka import KafkaProducer
from kafka.errors import KafkaError
import configparser
import sys
import json

# error-print
# def eprint(*args, **kwargs):
#     print(*args, file=sys.stderr, **kwargs)


### prepare config ###
configfile = 'kafka-client.conf'

if len(sys.argv) == 2:
    configfile = sys.argv[1]
elif len(sys.argv) == 1:
    configfile = "kafka-client.conf"
else:
    sys.exit("usage: " + sys.argv[0] + " [ config-file ]\n")

config = configparser.ConfigParser()
config.read(configfile)

options = dict(config.items("DEFAULT"))

for key, val in options.items():
    try:
        options[key] = int(val)
    except:
        pass

# print(repr(options))
### EOF prepare config ###

# THIS HAS TO BE GLOBAL SO THAT THE
# MESSAGES WILL BE SENT DURING SLEEP()
producer = None

def handle_message(topic,msg,options):
    global producer
    producer = KafkaProducer(**options,value_serializer=lambda v: json.dumps(v).encode('utf-8'))
    try:
        producer.send(topic,msg)
    except KafkaError:
        print("Error: " + e)
        producer.close()
        producer = None
        return False
    return True

handle_message('TestTopic', {"test": "blah"},options)
handle_message('TestTopic', {"test2": "blah2"},options)
import time
time.sleep(1)

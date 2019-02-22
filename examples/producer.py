#!/usr/bin/env  python36

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

# print(repr(options))
### EOF prepare config ###



def handle_message(topic,msg,options):
    producer = KafkaProducer(**options,value_serializer=lambda v: json.dumps(v).encode('utf-8'))
    future = producer.send(topic,msg)
    try:
        record_metadata = future.get(timeout=10)
    except KafkaError:
        print("Error: " + e)
        producer.close()
        producer = None
        return False
    return True

handle_message('TestTopic', {"lala": "blah"},options)

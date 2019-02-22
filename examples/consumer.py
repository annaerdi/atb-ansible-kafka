#!/usr/bin/env python36

from kafka import KafkaConsumer
import configparser
import sys
import json

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

config["DEFAULT"]['auto_offset_reset'] = "latest"
config["DEFAULT"]['enable_auto_commit'] = "True"

options = dict(config.items("DEFAULT"))

print(repr(options))
### EOF prepare config ###


consumer = KafkaConsumer('TestTopic',**options,value_deserializer=lambda m: json.loads(m.decode('utf-8')))
try:
    for msg in consumer:
        print (msg)
except KeyboardInterrupt:
    sys.exit()

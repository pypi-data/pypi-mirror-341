#!/usr/bin/env python3
from modbus_solar import get_all
import paho.mqtt.publish as publish

broker_url = "192.168.1.1"
broker_port = 1883
broker_auth = {"username":"sammy", "password":"sammy"}
broker_tls = {"ca_certs": ""}
topic = "van/solar"
client_id = "van"

try:
    publish.single(
    topic=topic,
    payload=get_all(),
    retain=True,
    hostname=broker_url,
    port=broker_port,
    auth=broker_auth,
    # tls=config.broker_tls, # ? Disable if TLS not enabled on MQTT otherwise will error
    client_id=client_id,
    qos=0
    )
except Exception as e:
    print (e)

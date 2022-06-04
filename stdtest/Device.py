import paho.mqtt.client as mqtt
from logging import getLogger
from threading import current_thread

class Device:

    def __init__(self, mqtt_host, mqtt_port, certificate):
        self.mqtt_host = mqtt_host
        self.mqtt_port = mqtt_port
        self.certificate = certificate
        self.messages = []
        self.logger = getLogger(__name__)
        
    def connect(self, username, password):
        self.mqttc = mqtt.Client()
        self.mqttc.username_pw_set(username, password)
        self.mqttc.tls_set(self.certificate, tls_version=mqtt.ssl.PROTOCOL_TLSv1_2)
        self.mqttc.enable_logger(self.logger)
        self.mqttc.on_message = self._on_message
        self.mqttc.connect(self.mqtt_host, self.mqtt_port)
        self.mqttc.loop_start()
        self.mqttc._thread.name = current_thread().name + ">" + __name__
        
    def disconnect(self):
        self.mqttc.loop_stop()
        self.mqttc.disconnect()
        
    def publish(self, topic, payload, qos=2, retain=False):
        self.mqttc.publish(topic, payload, qos, retain)
        
    def subscribe(self, topic, qos=2):
        self.mqttc.subscribe(topic, qos)
        
    def unsubscribe(self, topic):
        self.mqttc.unsubscribe(topic)
    
    def _on_message(self, client, userdata, message):
        self.messages.append(message.payload.decode("utf-8"))
    
    
    
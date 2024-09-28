# -*-coding:utf-8-*-
from umqtt.simple import MQTTClient
from machine import Pin
import network
import time
import machine
from machine import Timer
import json
import ujson
from Wifi import Wifi  # 假设已封装好的 Wi-Fi 连接函数
from Pin2Pin import variable
import uasyncio as asyncio

led = Pin(21, Pin.OUT)


class MqttManager:
    """
    连接阿里云物联网平台
    """

    def __init__(self):
        self.SERVER: str = ""
        self.CLIENT_ID: str = ""
        self.username: str = ""
        self.deviceName: str = ""
        self.password: str = ""
        self.update_topic: str = ""
        self.get_topic: str = ""
        self.post_topic: str = ""
        self.productKey: str = ""
        self.get_mqtt_info()
        self.client = MQTTClient(self.CLIENT_ID, self.SERVER, 0, self.username, self.password, 60)

    def get_mqtt_info(self):
        try:
            with open('MqttInfo.json', 'r') as f:
                data = ujson.load(f)
                self.SERVER = data["mqttHostUrl"]
                self.CLIENT_ID = data["clientId"]
                self.username = data["username"]
                self.password = data["passwd"]
                self.productKey = data["ProductKey"]
                self.deviceName = data["DeviceName"]
                self.update_topic = f'/{self.productKey}/{self.deviceName}/user/update'
                self.get_topic = f'/{self.productKey}/{self.deviceName}/user/get'
                self.post_topic = f'/sys/{self.productKey}/{self.deviceName}/thing/event/property/post'
        except Exception as e:
            print(str(e))

    def sub_cb(self, topic, msg):
        print("topic:", topic)
        print("msg:", msg)
        self.which_in_message(msg)

    def connect(self):
        self.client.set_callback(self.sub_cb)
        print(self.post_topic)

        try:
            self.client.set_callback(self.sub_cb)
            self.client.connect()
            self.client.subscribe(self.get_topic)
            self.client.subscribe(self.update_topic)
            # self.client.subscribe(self.post_topic)# 'NoneType' object has no attribute 'write'#不要妄想订阅不能订阅的
            mytimer = Timer(0)
            mytimer.init(mode=Timer.PERIODIC, period=60000, callback=self.heartbeatTimer)
        except Exception as ex_results:
            print('exception1', ex_results)

    @staticmethod
    def parse_data(data: str) -> dict:
        data_dict = json.loads(data.decode('utf-8'))
        items = data_dict['items']
        return items

    def which_in_message(self, data):
        items: dict = self.parse_data(data)
        if "LightSwitch" in items.keys():
            pass
        elif "LightBrightness" in items.keys():
            pass
        for key, value in items.items():
            print(f'key:{key},value:{value["value"]}')
            # led.value(value)

    def heartbeatTimer(self, mytimer):
        try:
            self.my_post("Temperature", variable.temperature)
            self.my_post("Humidity", variable.humidity)
        except Exception as ex_results2:
            print('exception', ex_results2)
            print('this is error')
            mytimer.deinit()

    def handle_messages(self):
        loop = asyncio.get_event_loop()
        loop.create_task(self.client.wait_msg())
        loop.run_forever()


    def disconnect(self):
        if self.client is not None:
            self.client.disconnect()

    def my_post(self, param_name: str, value):
        if type(value) == "str":
            value = '"' + value + '"'
        elif type(value) == "bool":
            value = int(value)
        info = '{"id": "123","version":"1.0.0","sys":{"ack":0},"params":{' + param_name + ':' + str(
            value) + '},"method": "thing.event.property.post"}'
        self.client.publish(topic=self.post_topic, msg=info, retain=False, qos=0)


if __name__ == "__main__":
    wifi = Wifi()
    wifi.wifi_connect()
    try:
        mqtt_manager = MqttManager()
        mqtt_manager.connect()
        mqtt_manager.handle_messages()
    except KeyboardInterrupt:
        mqtt_manager.disconnect()
    except Exception as e:
        print(str(e))


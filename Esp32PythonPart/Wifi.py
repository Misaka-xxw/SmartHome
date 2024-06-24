import time, network, ujson
from machine import SoftI2C


class Wifi:
    def __init__(self):
        self.wifi = network.WLAN(network.STA_IF)
        self.wifi_connected = False
        self.id, self.keyword = self.get_wifi_id_and_keyword()

    @staticmethod
    def get_wifi_id_and_keyword():
        try:
            with open('wifi.json', 'r') as f:
                data = ujson.load(f)
            return data['id'], data['keyword']
        except Exception as e:
            print(str(e))
            return "", ""

    def wifi_connect(self):  # wifi连接
        if not self.wifi.isconnected():
            # oled.text('wifi connecting', 0, 2)
            # oled.show()
            print('wifi连接中')
            self.wifi.active(True)
            try:
                self.wifi.connect(self.id, self.keyword)  # 账号, 密码
            except Exception as e:
                print(str(e))
                # oled.text('wifi isnot open', 0, 10)
                # oled.text('Press the key to return', 0, 18)
                # oled.show()
            count = 0
            while not self.wifi.isconnected():
                count += 1
                print(count)
                time.sleep(1)
                if count > 8:
                    print('wifi取消连接')
                    # oled.fill(0)
                    # oled.text('Wifi connect FAILED')
                    # oled.show()
                    self.wifi.active(False)
                    return
        if self.wifi.isconnected():
            self.wifi_connected = True
            print('wifi已连接')
            # oled.text('successed!', 0, 20)
            # oled.show()
            print('network config:', self.wifi.ifconfig())

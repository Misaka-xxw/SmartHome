import ssd1306
from machine import Pin,SoftI2C
from Pin2Pin import pin2pin
class Oled(ssd1306.SSD1306_I2C):
    def __init__(self):
        self.i2c = SoftI2C(scl=Pin(pin2pin.OLED_SCI), sda=Pin(pin2pin.OLED_SDA))  # 创建i2c对象,时钟->OLED_SCI，数据->OLED_SDA
        super().__init__(128, 64, self.i2c)
        self.fill(0)
        self.text('Hello,smart home!', 0, 0)
        self.show()
import uasyncio as asyncio
import machine


class MyUart(machine.UART):
    def __init__(self, tx=1, rx=2):
        super().__init__(2, 115200, tx=tx, rx=rx)

    def connect(self):
        loop = asyncio.get_event_loop()
        loop.create_task(self.handle_data())
        loop.run_forever()

    async def handle_data(self):
        while True:
            await asyncio.sleep(0)  # 小的延迟，让出控制权
            if self.any():
                data = self.read()
                print(data)


uart = MyUart()
uart.write("hello world")
uart.connect()
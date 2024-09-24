from Device import GPIODevice
import Adafruit_DHT

class DHT11(GPIODevice):
    def __init__(self, pin):
        super().__init__(pin)

    def __del__(self):
        super().__del__()

    def read(self):
        humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, self.pin)
        return humidity, temperature


if __name__ == '__main__':
    dht11 = DHT11(4)
    humidity, temperature = dht11.read()
    print(f"Humidity: {humidity}%")
    print(f"Temperature: {temperature}°C")
from Device import GPIODevice

class DHT11(GPIODevice):
    def __init__(self, pin):
        super().__init__(pin)

    def __del__(self):
        super().__del__()

    def measure(self):
        humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, self.pin)
        if humidity is None or temperature is None:
            raise RuntimeError("Failed to read data from DHT11 sensor")
        return humidity, temperature


if __name__ == '__main__':
    dht11 = DHT11(4)
    humidity, temperature = dht11.measure()
    print(f"Humidity: {humidity}%")
    print(f"Temperature: {temperature}°C")
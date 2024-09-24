import smbus2
import bme280

class BME280:
    def __init__(self, address=0x76, bus=1):
        self.address = address
        self.bus = smbus2.SMBus(bus)
        self.calibration_params = bme280.load_calibration_params(self.bus, self.address)

    def read_temperature(self):
        data = bme280.sample(self.bus, self.address, self.calibration_params)
        return data.temperature

    def read_humidity(self):
        data = bme280.sample(self.bus, self.address, self.calibration_params)
        return data.humidity

    def read_pressure(self):
        data = bme280.sample(self.bus, self.address, self.calibration_params)
        return data.pressure

    def read(self):
        data = bme280.sample(self.bus, self.address, self.calibration_params)
        return data.temperature, data.humidity, data.pressure

# Example usage
sensor = BME280()
temperature = sensor.read_temperature()
humidity = sensor.read_humidity()
pressure = sensor.read_pressure()
print(f"Temperature: {temperature} °C")
print(f"Humidity: {humidity} %")
print(f"Pressure: {pressure} hPa")
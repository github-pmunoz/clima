import time
import Adafruit_DHT
import numpy as np
import RPi.GPIO as GPIO

# Set up the GPIO using BCM numbering
GPIO.setmode(GPIO.BCM)

# Set the GPIO sensor pin number
pin = 23
sensor = Adafruit_DHT.DHT11

# Set up the LED pins
red_pin = 22
yellow_pin = 24
green_pin = 27

# Set up the LED pins as outputs
GPIO.setup(red_pin, GPIO.OUT)
GPIO.setup(yellow_pin, GPIO.OUT)
GPIO.setup(green_pin, GPIO.OUT)

# Function to turn on the red LED
def turn_on_red_led():
    GPIO.output(red_pin, GPIO.HIGH)

# Function to turn off the red LED
def turn_off_red_led():
    GPIO.output(red_pin, GPIO.LOW)

# Function to turn on the yellow LED
def turn_on_yellow_led():
    GPIO.output(yellow_pin, GPIO.HIGH)

# Function to turn off the yellow LED
def turn_off_yellow_led():
    GPIO.output(yellow_pin, GPIO.LOW)

# Function to turn on the green LED
def turn_on_green_led():
    GPIO.output(green_pin, GPIO.HIGH)

# Function to turn off the green LED
def turn_off_green_led():
    GPIO.output(green_pin, GPIO.LOW)

# Semaphore logic
semaphore_state = 0  # 0: red, 1: yellow, 2: green

# Function to toggle the semaphore light
def toggle_semaphore_light():
    global semaphore_state
    if semaphore_state == 0:
        turn_off_red_led()
        turn_on_yellow_led()
        semaphore_state = 1
    elif semaphore_state == 1:
        turn_off_yellow_led()
        turn_on_green_led()
        semaphore_state = 2
    else:
        turn_off_green_led()
        turn_on_red_led()
        semaphore_state = 0

# Add semaphore light toggle to the button callback
def button_callback(channel):
    print("Button pressed!")
    toggle_semaphore_light()

# Set up the button on the gpio
button_pin = 25
GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.add_event_detect(button_pin, GPIO.RISING, callback=button_callback)

# Set up the plot
import matplotlib
import matplotlib.pyplot as plt

# Set the plot style
plt.style.use('dark_background')

# Create a figure and axis
fig, axs = plt.subplots(2, 2, figsize=(10, 10))

# Set the title of the plot
fig.canvas.set_window_title('Temperature and Humidity Monitor')

# Set the title of the first plot
axs[0, 0].set_title('Temperature')
axs[0, 0].set_xlabel('Time (s)')
axs[0, 0].set_ylabel('Temperature (°C)')
axs[0, 0].grid(True)

# Set the title of the second plot
axs[0, 1].set_title('Humidity')
# Set the title of the second plot
axs[0, 1].set_title('Humidity')
axs[0, 1].set_xlabel('Time (s)')
axs[0, 1].set_ylabel('Humidity (%)')
axs[0, 1].grid(True)
# Set the title of the third plot
axs[1, 0].set_title('Temperature vs Humidity')
axs[1, 0].set_xlabel('Temperature (°C)')
axs[1, 0].set_ylabel('Humidity (%)')
axs[1, 0].grid(True)
# Set the title of the fourth plot
axs[1, 1].set_title('Temperature Histogram')
axs[1, 1].set_xlabel('Temperature (°C)')
axs[1, 1].set_ylabel('Frequency')
axs[1, 1].grid(True)
# Initialize the data arrays
temperature_data = []
humidity_data = []
time_data = []
# Initialize the plot lines and scatter plot
line_temp, = axs[0, 0].plot([], [], 'r-')
line_humidity, = axs[0, 1].plot([], [], 'b-')
scatter_temp_humidity = axs[1, 0].scatter([], [], c=[], cmap='cool', alpha=0.5)
# Initialize the histogram
hist_temp, bins_temp, patches_temp = axs[1, 1].hist([], bins=10, range=(0, 50), color='r', alpha=0.7)


# Add semaphore light toggle to the main loop
while True:
    # Read the sensor data
    humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)

    # check range is correct to discard outliers
    if temperature < 0 or temperature > 65 or humidity < 0 or humidity > 100:
        print("Out of range values. Discarding...")
        continue

    # Check if data was successfully retrieved
    if humidity is not None and temperature is not None:
        print(f"Temperature: {temperature:.6f}°C \t Humidity: {humidity:.6f}%")  # Print with 6 decimal accuracy
        temperature_data.append(temperature)
        humidity_data.append(humidity)
        time_data.append(time.time())  # Use current time as x-axis value

        # Update the temperature plot
        line_temp.set_data(time_data, temperature_data)
        axs[0, 0].relim()
        axs[0, 0].autoscale_view()

        # Update the humidity plot
        line_humidity.set_data(time_data, humidity_data)
        axs[0, 1].relim()
        axs[0, 1].autoscale_view()

        # Update the temperature vs humidity plot
        scatter_temp_humidity = axs[1, 0].scatter(temperature_data, humidity_data, c=time_data, cmap='cool', alpha=0.5)
        scatter_temp_humidity.set_offsets(list(zip(temperature_data, humidity_data)))
        scatter_temp_humidity.set_array(np.array(time_data))
        scatter_temp_humidity.set_cmap('cool')  # Set the colormap to 'cool'
        axs[1, 0].relim()
        axs[1, 0].autoscale_view()
        axs[1, 0].set_facecolor('black')  # Set the background color to black

        # Redraw the plot
        fig.canvas.draw()
        fig.canvas.flush_events()

        # Toggle the semaphore light
        toggle_semaphore_light()
    else:
        print("Failed to retrieve data from sensor")
        fails += 1
        if fails > 5:
            print("Too many failed attempts. Exiting...")
            break

    # Wait for 0.25 seconds before the next measurement
    time.sleep(0.01)

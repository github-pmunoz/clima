import time
import Adafruit_DHT
import numpy as np
import RPi.GPIO as GPIO

# Set the GPIO sensor pin number
pin = 16

# Set the sensor type (DHT11)
sensor = Adafruit_DHT.DHT11

# Set up the GPIO using BCM numbering
GPIO.setmode(GPIO.BCM)

# Set up the LED pins
red_pin = 15
yellow_pin = 18
green_pin = 13

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
def button_callback(channel)::
    print("Button pressed!")
    toggle_semaphore_light()

# Add semaphore light toggle to the main loop
while True:le True:
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

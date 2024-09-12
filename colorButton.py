import time

import RPi.GPIO as GPIO

# Set up GPIO pins
red_pin = 22
yellow_pin = 24
green_pin = 27
button_pin = 6

GPIO.setmode(GPIO.BCM)
GPIO.setup(red_pin, GPIO.OUT)
GPIO.setup(yellow_pin, GPIO.OUT)
GPIO.setup(green_pin, GPIO.OUT)
GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Define LED states
led_states = [
    (GPIO.HIGH, GPIO.LOW, GPIO.LOW),    # Red
    (GPIO.LOW, GPIO.HIGH, GPIO.LOW),    # Yellow
    (GPIO.LOW, GPIO.LOW, GPIO.HIGH)     # Green
]
current_state = 0

def cycle_led_state(channel):
    global current_state
    current_state = (current_state + 1) % len(led_states)
    red_state, yellow_state, green_state = led_states[current_state]
    GPIO.output(red_pin, red_state)
    GPIO.output(yellow_pin, yellow_state)
    GPIO.output(green_pin, green_state)

# Add event listener for button press
GPIO.add_event_detect(button_pin, GPIO.FALLING, callback=cycle_led_state, bouncetime=200)

try:
    while True:
        time.sleep(0.1)

except KeyboardInterrupt:
    GPIO.cleanup()
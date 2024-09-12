import time
import multiprocessing
import RPi.GPIO as GPIO

# Create a function for a thread that will monitor the buttom input and detect an a push down event
def button_monitor(func):
    button_pin = 25
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(button_pin, GPIO.IN)
    while True:
        input_state = GPIO.input(button_pin)
        if input_state == False:
            print('Button Pressed')
            func()
            time.sleep(0.2)

# Set up GPIO pins
red_pin = 22
yellow_pin = 24
green_pin = 27
button_pin = 25

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

def cycle_led_state():
    global current_state
    current_state = (current_state + 1) % len(led_states)
    red_state, yellow_state, green_state = led_states[current_state]
    GPIO.output(red_pin, red_state)
    GPIO.output(yellow_pin, yellow_state)
    GPIO.output(green_pin, green_state)

try:
    # Create a separate process for the button monitor
    button_process = multiprocessing.Process(target=button_monitor, args=(cycle_led_state,))
    button_process.start()
    button_process.join()


except KeyboardInterrupt:
    GPIO.cleanup()
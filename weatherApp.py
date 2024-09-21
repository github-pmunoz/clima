import Adafruit_DHT
import tweepy

# Set up GPIO sensor
sensor = Adafruit_DHT.DHT11
pin = 4

# Set up Twitter API credentials
consumer_key = 'YOUR_CONSUMER_KEY'
consumer_secret = 'YOUR_CONSUMER_SECRET'
access_token = 'YOUR_ACCESS_TOKEN'
access_token_secret = 'YOUR_ACCESS_TOKEN_SECRET'

# Authenticate with Twitter API
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

# Function to measure temperature and humidity
def measure_temperature_humidity():
    humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
    return humidity, temperature

# Function to post daily summaries on Twitter
def post_daily_summary(summary):
    api.update_status(summary)

# Main function
def main():
    # Measure temperature and humidity
    humidity, temperature = measure_temperature_humidity()

    # Create daily summary
    summary = f"Today's temperature: {temperature}°C\nToday's humidity: {humidity}%"

    # Post daily summary on Twitter
    post_daily_summary(summary)

if __name__ == '__main__':
    main()
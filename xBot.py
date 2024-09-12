import tweepy
import requests
import datetime

# Twitter API credentials
consumer_key = "pIXd6jzVXnsVvIzDSkRn7EJhZ"
consumer_secret = "4fBrwRdUasmgePgBWAN4VEXxNQ3DDxKZL77vLSnZ6MWm2msxfR"
bearer_token = "AAAAAAAAAAAAAAAAAAAAAPSgugEAAAAAKHh0URHPxbIaq4suuZrBiiW8OhM%3DtthPaJUgpSi0RPpE7tMo43Su8u7RmGFJck9RhTXcTmu7FkU9UA"
access_token = "1760515708310421504-AbYnEHUA0dh50h91d1lq50t2z9LHQl"
access_token_secret = "V2BpDFSvi7VR5gmxQVufimJwmocIwzJCdj2v55ft5wbXB"

# Google API key
api_key = "AIzaSyB_GgCeXB0x40ILKRR2pk0_3_7dlLXHHuA"

# Function to get weather data
def get_weather_data():
    # Mock weather data for testing
    mock_data = {
        'main': {
            'temp': 25,
            'humidity': 70
        },
        'weather': [
            {
                'description': 'Sunny'
            }
        ]
    }
    return mock_data

# Function to format weather data
def format_weather_data(data):
    # Extract relevant weather information from the data
    temperature = data['main']['temp']
    humidity = data['main']['humidity']
    description = data['weather'][0]['description']

    # Format the weather summary
    summary = f"Today's weather: {description}. Temperature: {temperature}°C. Humidity: {humidity}%."
    return summary

# Function to post weather summary on Twitter
def post_weather_summary(summary):
    # Authenticate with Twitter API
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)

    # Post the weather summary as a tweet
    api.update_status(summary)

# Get current date and time
current_date = datetime.datetime.now().strftime("%Y-%m-%d")

# Get weather data for your city
city_name = "YOUR_CITY_NAME"
weather_data = get_weather_data()

# Format the weather data
weather_summary = format_weather_data(weather_data)

# Post the weather summary on Twitter
post_weather_summary(weather_summary)
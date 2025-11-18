import openmeteo_requests
import pandas as pd
import requests_cache
from retry_requests import retry

# Ensure all floats in DataFrame are displayed with 2 decimals
pd.options.display.float_format = '{:.2f}'.format

# Setup the Open-Meteo API client with cache and retry on error
cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
openmeteo = openmeteo_requests.Client(session=retry_session)

# API request 
url = "https://api.open-meteo.com/v1/forecast"
params = {
    "latitude": 40.8499,
    "longitude": 25.8764,
    "hourly": ["temperature_2m", "rain", "wind_speed_10m", "wind_direction_10m"],
    "current": ["temperature_2m", "rain", "wind_speed_10m", "wind_direction_10m"],
    "timezone": "auto",
    "forecast_days": 3,
}

# Make API call
responses = openmeteo.weather_api(url, params=params)
response = responses[0]  

# Print location info
print(f"Coordinates: {response.Latitude():.2f}°N {response.Longitude():.2f}°E")
print(f"Elevation: {response.Elevation():.2f} m asl")
print(f"Timezone: {response.Timezone()}{response.TimezoneAbbreviation()}")
print(f"Timezone difference to GMT+0: {response.UtcOffsetSeconds()}s\n")

# Process current weather
current = response.Current()
current_temperature_2m = round(current.Variables(0).Value(), 2)
current_rain = round(current.Variables(1).Value(), 2)
current_wind_speed_10m = round(current.Variables(2).Value(), 2)
current_wind_direction_10m = round(current.Variables(3).Value(), 2)

print(f"Current time: {current.Time()}")
print(f"Current temperature_2m: {current_temperature_2m:.2f}")
print(f"Current rain: {current_rain:.2f}")
print(f"Current wind_speed_10m: {current_wind_speed_10m:.2f}")
print(f"Current wind_direction_10m: {current_wind_direction_10m:.2f}\n")

# Process hourly weather
hourly = response.Hourly()
hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy().round(2)
hourly_rain = hourly.Variables(1).ValuesAsNumpy().round(2)
hourly_wind_speed_10m = hourly.Variables(2).ValuesAsNumpy().round(2)
hourly_wind_direction_10m = hourly.Variables(3).ValuesAsNumpy().round(2)


hourly_data = {
    "date": pd.date_range(
        start=pd.to_datetime(hourly.Time(), unit="s", utc=True),
        end=pd.to_datetime(hourly.TimeEnd(), unit="s", utc=True),
        freq=pd.Timedelta(seconds=hourly.Interval()),
        inclusive="left"
    ),
    "temperature_2m": hourly_temperature_2m,
    "rain": hourly_rain,
    "wind_speed_10m": hourly_wind_speed_10m,
    "wind_direction_10m": hourly_wind_direction_10m
}

hourly_dataframe = pd.DataFrame(data=hourly_data).round(2)
print("Hourly data:\n", hourly_dataframe)

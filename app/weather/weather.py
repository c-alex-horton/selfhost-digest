# pyright: ignore
import openmeteo_requests
import pandas as pd
import requests_cache
from retry_requests import retry
from datetime import datetime

weather_codes_map = {
    0: "Clear sky",
    1: "Mainly clear",
    2: "Partly cloudy",
    3: "Overcast",
    45: "Fog",
    48: "Depositing rime fog",
    51: "Light drizzle",
    53: "Moderate drizzle",
    55: "Dense drizzle",
    56: "Light freezing drizzle",
    57: "Dense freezing drizzle",
    61: "Light rain",
    63: "Moderate rain",
    65: "Heavy rain",
    66: "Light freezing rain",
    67: "Heavy freezing rain",
    71: "Light snowfall",
    73: "Moderate snowfall",
    75: "Heavy snowfall",
    77: "Snow grains",
    80: "Light rain showers",
    81: "Moderate rain showers",
    82: "Violent rain showers",
    85: "Light snow showers",
    86: "Heavy snow showers",
    95: "Thunderstorm",
    96: "Thunderstorm w/ slight hail",
    99: "Thunderstorm w/ heavy hail",
}

# Setup the Open-Meteo API client with cache and retry on error
cache_session = requests_cache.CachedSession(".cache", expire_after=3600)
retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
openmeteo = openmeteo_requests.Client(session=retry_session)

# Make sure all required weather variables are listed here
# The order of variables in hourly or daily is important to assign them correctly below
url = "https://api.open-meteo.com/v1/forecast"
params = {
    "latitude": 30.2672,
    "longitude": -97.7431,
    "daily": [
        "weather_code",
        "sunrise",
        "sunset",
        "temperature_2m_max",
        "temperature_2m_min",
    ],
    "timezone": "auto",
    "forecast_days": 2,
    "wind_speed_unit": "mph",
    "temperature_unit": "fahrenheit",
    "precipitation_unit": "inch",
}


def gen_weather():
    lines = []

    lines.append("## Weather")

    responses = openmeteo.weather_api(url, params=params)
    response = responses[0]
    daily = response.Daily()

    weather_codes = daily.Variables(0).ValuesAsNumpy()
    sunrises = daily.Variables(1).ValuesInt64AsNumpy()
    sunsets = daily.Variables(2).ValuesInt64AsNumpy()
    temps_max = daily.Variables(3).ValuesAsNumpy()
    temps_min = daily.Variables(4).ValuesAsNumpy()

    start = daily.Time()
    interval = daily.Interval()

    for i in range(len(weather_codes)):
        if i == 0:
            date = "Today"
        else:
            date = "Tomorrow"
        sunrise = datetime.fromtimestamp(sunrises[i]).strftime("%H:%M")
        sunset = datetime.fromtimestamp(sunsets[i]).strftime("%H:%M")
        code = weather_codes[i]
        weather = weather_codes_map.get(code, f"Unknown ({code})")
        lines.append(
            f"{date}: {weather}, {round(temps_min[i])}°F – {round(temps_max[i])}°F | Sunrise: {sunrise}, Sunset: {sunset}"
        )

    return "\n".join(lines)


gen_weather()

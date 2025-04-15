# fetch-my-weather

A beginner-friendly Python package for fetching weather data, designed for educational use.

## Features

- 🌤️ Easy access to weather data from wttr.in
- 🌙 Moon phase information
- 🗺️ Location-based weather (cities, airports, coordinates)
- 🌍 Multiple language support
- 📊 Multiple output formats: JSON (with Pydantic models), raw JSON (dict), text and PNG
- 🏗️ Type-safe Pydantic models for JSON responses
- 🚀 Built-in caching to be nice to the wttr.in service
- 🧪 Mock mode for development and testing without API rate limits
- 🛡️ Beginner-friendly error handling (no exceptions)
- 📊 Response metadata for tracking data source and error information
- 📚 Designed for teaching Python and API interactions
- 🤖 LLM-ready with comprehensive [LLM guide](LLM-GUIDE.md) you can upload to AI assistants

## Installation

```bash
pip install fetch-my-weather
```

## Quick Start

```python
import fetch_my_weather

# Get weather for your current location (based on IP) as JSON
current_weather = fetch_my_weather.get_weather()  # Default format is 'json'
print(f"Temperature: {current_weather['current_condition'][0]['temp_C']}°C")

# Get weather for Berlin in metric units as text
berlin_weather = fetch_my_weather.get_weather(location="Berlin", units="m", format="text")
print(berlin_weather)

# Get moon phase for a specific date
moon = fetch_my_weather.get_weather(is_moon=True, moon_date="2025-07-04")
print(moon)
```

## Teaching Applications

fetch-my-weather is designed as a teaching tool for:

- Introducing API interactions in a beginner-friendly way
- Demonstrating HTTP requests without exception handling complexity
- Teaching caching concepts
- Working with different data formats (JSON, text and binary/PNG)
- Understanding URL construction and query parameters
- Processing and displaying weather data in applications
- Parsing and working with JSON data

### Mini-Projects

The package includes a collection of ready-to-use mini-projects in the `docs/mini-projects/` directory:

- **Beginner projects**: Weather dashboard, multi-city checker, image saver
- **Intermediate projects**: Weather-based recommendations, forecast tracking, wallpaper changer
- **Advanced projects**: Notification system, data analyzer, home automation, weather-based game

These projects provide practical examples and serve as great teaching resources or starting points for your own applications.

## Usage Guide

### Getting Weather Data

```python
import fetch_my_weather

# JSON format (default) - current location with Pydantic model
weather = fetch_my_weather.get_weather()
# Access data using type-safe models with autocomplete
temp = weather.current_condition[0].temp_C
condition = weather.current_condition[0].weatherDesc[0].value

# Raw JSON format - returns a Python dictionary
raw_weather = fetch_my_weather.get_weather(format="raw_json")
# Access data using dictionary key/value access
temp = raw_weather["current_condition"][0]["temp_C"]
condition = raw_weather["current_condition"][0]["weatherDesc"][0]["value"]

# Text format - specific location
nyc_weather = fetch_my_weather.get_weather(location="New York", format="text")

# Airport code
lax_weather = fetch_my_weather.get_weather(location="lax")

# Geographic coordinates
coord_weather = fetch_my_weather.get_weather(location="48.8567,2.3508")

# Compact view (applies to text format)
compact_weather = fetch_my_weather.get_weather(view_options="0", format="text")

# Compact view + quiet (no city name in header)
compact_quiet = fetch_my_weather.get_weather(view_options="0q", format="text")

# Units: metric (default), USCS (u), or wind in m/s (M)
us_units = fetch_my_weather.get_weather(units="u")

# Different language
spanish = fetch_my_weather.get_weather(lang="es")

# Type annotations for better IDE support
from fetch_my_weather import WeatherResponse
weather_typed: WeatherResponse = fetch_my_weather.get_weather()
```

### Getting Moon Phase Data

```python
import fetch_my_weather

# Current moon phase
moon = fetch_my_weather.get_weather(is_moon=True)

# Moon phase for specific date
christmas_moon = fetch_my_weather.get_weather(is_moon=True, moon_date="2025-12-25")

# Moon with location hint (affects timing)
paris_moon = fetch_my_weather.get_weather(is_moon=True, moon_location_hint=",+Paris")
```

### Getting PNG Weather Images

```python
import fetch_my_weather

# Weather as PNG using format parameter (returns bytes)
london_png = fetch_my_weather.get_weather(location="London", format="png")

# Save PNG to file
with open("london_weather.png", "wb") as f:
    f.write(london_png)

# PNG with options (transparency)
transparent_png = fetch_my_weather.get_weather(location="Tokyo", format="png", png_options="t")

# Legacy method (deprecated but still supported)
legacy_png = fetch_my_weather.get_weather(location="Paris", is_png=True)
```

### Configuration Settings

```python
import fetch_my_weather

# Change cache duration (in seconds, 0 to disable)
fetch_my_weather.set_cache_duration(1800)  # 30 minutes

# Clear the cache
fetch_my_weather.clear_cache()

# Set a custom user agent
fetch_my_weather.set_user_agent("My Weather App v1.0")

# Enable mock mode (for development and testing)
fetch_my_weather.set_mock_mode(True)  # Use mock data instead of real API calls

# Use mock mode for a single request
mock_weather = fetch_my_weather.get_weather(location="London", use_mock=True)
```

### Error Handling

```python
import fetch_my_weather

# fetch-my-weather never raises exceptions, it returns error messages as strings
result = fetch_my_weather.get_weather(location="NonExistentPlace12345")

# Check if result is an error message (JSON format will return dict when successful)
if isinstance(result, str) and result.startswith("Error:"):
    print(f"Something went wrong: {result}")
elif isinstance(result, dict):
    print("Weather data received successfully as JSON")
else:
    print("Weather data received successfully")
```

### Response Metadata

For more advanced error handling and tracking of data sources, use the `with_metadata` parameter:

```python
import fetch_my_weather
from fetch_my_weather import ResponseWrapper

# Get weather with metadata information
response = fetch_my_weather.get_weather(location="London", with_metadata=True)

# Response is a wrapper containing both data and metadata
if isinstance(response, ResponseWrapper):
    # Check metadata properties
    metadata = response.metadata
    print(f"Data source: {'API' if metadata.is_real_data else 'Cache' if metadata.is_cached else 'Mock'}")
    
    # If there was an error, it will be in the metadata
    if metadata.error_type:
        print(f"Error: {metadata.error_message}")
        # Data will be mock data instead of an error string
    
    # Access the actual data (always available, even during errors)
    data = response.data
    if hasattr(data, "current_condition") and data.current_condition:
        print(f"Temperature: {data.current_condition[0].temp_C}°C")
```

When using the metadata feature, the package will always return usable data rather than error strings, falling back to mock data during API errors or rate limiting.

## Pydantic Models

When using the JSON format (default), the package returns a structured `WeatherResponse` Pydantic model that contains:

- `current_condition`: Current weather data (temperature, humidity, etc.)
- `nearest_area`: Location information (city, country, coordinates)
- `weather`: Forecast data for multiple days
- `request`: Information about the API request

```python
# Example of accessing model properties
weather = fetch_my_weather.get_weather(location="London")

# Current weather
current = weather.current_condition[0]
print(f"Temperature: {current.temp_C}°C")
print(f"Condition: {current.weatherDesc[0].value}")

# Location data  
location = weather.nearest_area[0]
print(f"Location: {location.areaName[0].value}, {location.country[0].value}")

# Forecast
for day in weather.weather:
    print(f"Date: {day.date}")
    print(f"Max temp: {day.maxtempC}°C, Min temp: {day.mintempC}°C")
    print(f"Sunrise: {day.astronomy[0].sunrise}, Sunset: {day.astronomy[0].sunset}")
```

## Complete Parameter Reference

The `get_weather()` function accepts these parameters:

| Parameter | Type | Description |
|-----------|------|-------------|
| `location` | str | Location identifier (city name, airport code, coordinates, etc.) |
| `units` | str | Units system: `m` (metric, default), `u` (US/imperial), `M` (wind in m/s) |
| `view_options` | str | Display options: `0`-`3` (forecast days), `n` (narrow), `q` (quiet), etc. |
| `lang` | str | Language code (e.g., `en`, `fr`, `es`, `ru`, `zh-cn`) |
| `format` | str | Output format: `json` (default, Pydantic model), `raw_json` (Python dict), `text`, or `png` |
| `is_png` | bool | If `True`, return PNG image as bytes instead of text (deprecated, use `format="png"`) |
| `png_options` | str | PNG-specific options: `p` (padding), `t` (transparency), etc. |
| `is_moon` | bool | If `True`, show moon phase instead of weather |
| `moon_date` | str | Date for moon phase in `YYYY-MM-DD` format (with `is_moon=True`) |
| `moon_location_hint` | str | Location hint for moon phase (e.g., `,+US`, `,+Paris`) |
| `use_mock` | bool | If `True`, use mock data instead of making a real API request |
| `with_metadata` | bool | If `True`, returns both data and metadata about the response source and any errors |

## Documentation

📚 **Full documentation is now live at [michael-borck.github.io/fetch-my-weather](https://michael-borck.github.io/fetch-my-weather/)!**

The documentation includes:
- 📘 Detailed [user guide](https://michael-borck.github.io/fetch-my-weather/user-guide/) with examples
- 🛠️ [Mini-projects](https://michael-borck.github.io/fetch-my-weather/mini-projects/README/) for learning (beginner to advanced)
- 🎓 [Teaching resources](https://michael-borck.github.io/fetch-my-weather/teaching-guide/) for educators
- 📋 [Technical documentation](https://michael-borck.github.io/fetch-my-weather/technical-doc/) for developers

## AI Assistant Integration

🤖 This package includes an [LLM guide](LLM-GUIDE.md) specifically designed for AI assistants.

To use with AI assistants:
1. Download the [LLM-GUIDE.md](LLM-GUIDE.md) file
2. Upload it to your AI assistant (like Claude, ChatGPT, etc.)
3. The AI can now help you use the package more effectively

## License

MIT License - see the [LICENSE](LICENSE) file for details.

## Contributors

This project is maintained by [Michael Borck](https://github.com/michael-borck) with contributions from various individuals. See [AUTHORS.md](AUTHORS.md) for a complete list of contributors.

## Acknowledgments

This package is a wrapper around the amazing [wttr.in](https://github.com/chubin/wttr.in) service created by [Igor Chubin](https://github.com/chubin). Please be respectful of the wttr.in service by not making too many requests.

# Open-Meteo Weather API Client

This Python project fetches and processes weather data from the 
[Open-Meteo API](https://open-meteo.com/) using caching and retry mechanisms. 
It provides both current and hourly weather information with all numeric values 
rounded to two decimal places.

The project retrieves current weather, including temperature, rain, wind speed, 
and wind direction. Hourly weather forecasts are processed into a Pandas DataFrame, 
with all numeric values rounded for clarity, making the output clean and readable.

A virtual environment (`venv`) was used to manage project dependencies, 
ensuring that all required packages are isolated from the system Python environment. 
This approach maintains a clean and reproducible development setup while safely 
handling packages like `openmeteo-requests`, `pandas`, `requests_cache`, and 
`retry_requests`.

API responses are cached for one hour using `requests_cache`, and failed requests 
are automatically retried using `retry_requests`. This ensures reliable and 
efficient retrieval of weather data. The project demonstrates best practices in 
API handling, data processing, caching, retries, and numeric formatting.

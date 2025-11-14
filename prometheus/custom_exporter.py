from prometheus_client import start_http_server, Gauge
import requests
import time

OPENWEATHER_API_KEY = "55e8c1d30fdc5900a9809a6d2dc8aaf9"   
CITY = "Astana"
URL = f"http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={OPENWEATHER_API_KEY}&units=metric"

# METRICS 
temp_gauge = Gauge("weather_temp_celsius", "Temperature in Celsius")
feels_gauge = Gauge("weather_feels_like_celsius", "Feels like temperature")
temp_min_gauge = Gauge("weather_temp_min_celsius", "Min temperature")
temp_max_gauge = Gauge("weather_temp_max_celsius", "Max temperature")

humidity_gauge = Gauge("weather_humidity_percent", "Humidity in %")
pressure_gauge = Gauge("weather_pressure_hpa", "Pressure in hPa")

wind_speed_gauge = Gauge("weather_wind_speed", "Wind speed (m/s)")
wind_deg_gauge = Gauge("weather_wind_deg", "Wind direction degrees")

clouds_gauge = Gauge("weather_cloudiness_percent", "Cloudiness %")
visibility_gauge = Gauge("weather_visibility_meters", "Visibility in meters")

sunrise_gauge = Gauge("weather_sunrise_timestamp", "Sunrise unix timestamp")
sunset_gauge = Gauge("weather_sunset_timestamp", "Sunset unix timestamp")

last_update_gauge = Gauge("weather_last_update_timestamp", "Last update timestamp")


def update_metrics():
    try:
        r = requests.get(URL)
        data = r.json()

        main = data["main"]
        wind = data.get("wind", {})
        clouds = data.get("clouds", {})
        sys = data.get("sys", {})

        temp_gauge.set(main["temp"])
        feels_gauge.set(main["feels_like"])
        temp_min_gauge.set(main["temp_min"])
        temp_max_gauge.set(main["temp_max"])

        humidity_gauge.set(main["humidity"])
        pressure_gauge.set(main["pressure"])

        wind_speed_gauge.set(wind.get("speed", 0))
        wind_deg_gauge.set(wind.get("deg", 0))

        clouds_gauge.set(clouds.get("all", 0))
        visibility_gauge.set(data.get("visibility", 0))

        sunrise_gauge.set(sys.get("sunrise", 0))
        sunset_gauge.set(sys.get("sunset", 0))

        last_update_gauge.set(data.get("dt", 0))

        print("✔ Weather metrics updated")

    except Exception as e:
        print("Error:", e)



if __name__ == "__main__":
    print("Starting Weather Exporter on port 9200...")
    start_http_server(9200)

    while True:
        update_metrics()
        time.sleep(20)     

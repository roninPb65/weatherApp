from flask import Flask, render_template
from dotenv import load_dotenv
import requests, geocoder, os

load_dotenv()

app = Flask(__name__)

API = "https://api.openweathermap.org/data/2.5/weather"
KEY = os.getenv("WEATHER_API_KEY")


# --- Safe check (no crash in production)
if not KEY:
    print("WARNING: WEATHER_API_KEY is missing")


def get_weather_data(lat, lon):
    try:
        params = {
            "lat": lat,
            "lon": lon,
            "units": "metric",
            "appid": KEY
        }

        r = requests.get(API, params=params, timeout=10)

        # IMPORTANT: don't crash on API errors
        data = r.json()

        if r.status_code != 200:
            return {"error": data.get("message", "API request failed")}

        return data

    except requests.RequestException as e:
        return {"error": str(e)}


def get_user_location():
    try:
        g = geocoder.ip("me")

        if not g.ok or not g.latlng:
            return None, None

        return g.latlng

    except Exception:
        return None, None


@app.route("/")
def index():
    lat, lon = get_user_location()

    if lat is None or lon is None:
        return render_template(
            "index.html",
            weather_data=None,
            error="Unable to determine location"
        )

    data = get_weather_data(lat, lon)

    error = data.get("error") if isinstance(data, dict) else None
    weather = None if error else data

    return render_template(
        "index.html",
        weather_data=weather,
        error=error
    )


if __name__ == "__main__":
    app.run(debug=True)

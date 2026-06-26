from flask import Flask, render_template
from dotenv import load_dotenv
import requests, geocoder, os
load_dotenv()
app=Flask(__name__)
API="https://api.openweathermap.org/data/2.5/weather"
KEY=os.getenv("WEATHER_API_KEY")
if not KEY: raise RuntimeError("Set WEATHER_API_KEY in .env")
def get_weather_data(lat,lon):
    try:
        r=requests.get(API,params={"lat":lat,"lon":lon,"units":"metric","appid":KEY},timeout=10)
        r.raise_for_status(); return r.json()
    except requests.RequestException as e:
        return {"error":str(e)}
def get_user_location():
    g=geocoder.ip("me")
    if not g.ok or not g.latlng: return None,None
    return g.latlng
@app.route("/")
def index():
    lat,lon=get_user_location()
    if lat is None: return render_template("index.html",weather_data=None,error="Unable to determine location")
    data=get_weather_data(lat,lon)
    return render_template("index.html",weather_data=None if "error" in data else data,error=data.get("error"))
if __name__=="__main__":
    app.run(debug=True)

import datetime
from dotenv import load_dotenv
import requests
from django.shortcuts import render
import os

# Create your views here.
def configure():
    load_dotenv()
    
def index(request):
    configure()
    current_weather_url = f"https://api.openweathermap.org/data/2.5/weather?q={{}}&appid={os.getenv('api_key')}"
    forecast_url = f"https://api.openweathermap.org/data/2.5/onecall?lat={{}}&lon={{}}&exclude=current,minutely,hourly,alerts&appid={os.getenv('api_key')}"

    if request.method == "POST":
        city1 = request.POST['city1']
        city2 = request.POST.get('city2', None)

        weather_data1, daily_forecasts1 = fetch_weather_and_forecast(city1, os.getenv('api_key'), current_weather_url, forecast_url)

        if city2:
            weather_data2, daily_forecasts2 = fetch_weather_and_forecast(city2, os.getenv('api_key'), current_weather_url, forecast_url)
        else:
            weather_data2, daily_forecasts2 = None, None

        context = {
            "weather_data1": weather_data1,
            "daily_forecasts1": daily_forecasts1,
            "weather_data2": weather_data2,
            "daily_forecasts2": daily_forecasts2,
        }
        return render(request, "weather_app/index.html", context)
    else:
        return render(request, "weather_app/index.html")

def fetch_weather_and_forecast(city, api_key, current_weather_url, forecast_url): 
    configure()
    response = requests.get(current_weather_url.format(city, api_key)).json()
    lat, lon = response.get('coord', {}).get('lat'), response.get('coord', {}).get('lon')
    forecast_response = requests.get(forecast_url.format(lat, lon, api_key)).json()
    print("!!",response)
    weather_data = {
        "city": city,
        "temperature": round(response['main']['temp'] - 273.15, 2),
        "description": response['weather'][0]['description'],
        "icon": response['weather'][0]['icon']
    }

    daily_forecasts = []
    for daily_data in forecast_response.get('daily_forecast', [])[:5]:
            daily_forecasts.append({
                "day": datetime.datetime.fromtimestamp(daily_data['dt']).strftime("%A"),
                "min_temp": round(daily_data['temp']['min'] - 273.15, 2),
                "max_temp": round(daily_data['temp']['max'] - 273.15, 2),
                "description": daily_data['weather'][0]['description'],
                "icon": daily_data['weather'][0]['icon']
            })
    return weather_data, daily_forecasts
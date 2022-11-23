from flask import Flask, render_template, request
import requests
import configparser
from datetime import datetime

app = Flask(__name__)
app.debug = True


@app.route('/')
def weather_dashboard():
    return render_template('home.html')


def get_weather_results_imperial(zip_code, api_key):
    api_url = "https://api.openweathermap.org/data/2.5/weather?zip={}&units=imperial&appid={}".format(zip_code, api_key)
    r = requests.get(api_url)
    return r.json()


def get_weather_results_metric(zip_code, api_key):
    api_url = "https://api.openweathermap.org/data/2.5/weather?zip={}&units=metric&appid={}".format(zip_code, api_key)
    r = requests.get(api_url)
    return r.json()


@app.route('/results', methods=['POST'])
def render_results():
    zip_code = request.form['zipCode']
    temp_units = request.form['temp_units']
    api_key = get_api_key()
    if temp_units == 'F':
        data = get_weather_results_imperial(zip_code, api_key)
        temp = "{0:.2f}".format(data["main"]["temp"])
        feels_like = "{0:.2f}".format(data["main"]["feels_like"])
    else:
        data = get_weather_results_metric(zip_code, api_key)
        temp = "{0:.2f}".format(data["main"]["temp"])
        feels_like = "{0:.2f}".format(data["main"]["feels_like"])
    icon = data["weather"][0]["icon"]
    iconurl = "http://openweathermap.org/img/w/" + icon + ".png"
    weather = data["weather"][0]["main"]
    location = data["name"]
    sunrise = data["sys"]["sunrise"]
    dt_obj = datetime.fromtimestamp(int(sunrise))
    now = datetime.now().replace(microsecond=0)
    timezone = 1663274335.823856
    # generate utc time now
    now_utc = datetime.utcnow()
    # convert to timestamp
    print(now_utc)
    timestamp_utc = datetime.timestamp(now_utc)
    # read timezone from data convert to integer
    tz_offset = int(data["timezone"])
    # add timezone offset
    local_timestamp = timestamp_utc + tz_offset
    print(local_timestamp)
    local_dt_obj = datetime.fromtimestamp(local_timestamp)
    print(local_dt_obj)
    # convert timestamp  back to datetime object

    return render_template('results.html',
                           location=location, temp=temp, iconurl=iconurl, dt_obj=dt_obj,
                           feels_like=feels_like, weather=weather, sunrise=sunrise, now=now, local_dt_obj=local_dt_obj)


def get_api_key():
    config = configparser.ConfigParser()
    config.read('config.ini')
    return config['openweathermap']['api']


def get_weather_results_imperial(zip_code, api_key):
    api_url = "https://api.openweathermap.org/data/2.5/weather?zip={}&units=imperial&appid={}".format(zip_code, api_key)
    r = requests.get(api_url)
    return r.json()


def get_weather_results_metric(zip_code, api_key):
    api_url = "https://api.openweathermap.org/data/2.5/weather?zip={}&units=metric&appid={}".format(zip_code, api_key)
    r = requests.get(api_url)
    return r.json()


if __name__ == '__main__':
    app.run()

print(get_weather_results_metric("95129", get_api_key()))


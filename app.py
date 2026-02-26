from flask import Flask, request ,redirect,render_template, jsonify
import requests
from datetime import datetime


app=Flask(__name__)

API_KEY = "680208fc2a1486cc54ab99795d231c27"

@app.route('/',methods=['GET'])
def index():
    return render_template("weather.html")

@app.route("/get_weather",methods=['POST'])
def get_weather():
    city=request.form['city']
    url =  f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    data = response.json()
    return render_template("weather.html", weather=data)

@app.route("/get_weather_forecast", methods=['GET'])
def get_weather_forecast():
    city = request.args.get('city')
    date_str = request.args.get('datetime')

    if not city or not date_str:
        return jsonify({"error": "Missing 'city' or 'datetime' parameter"}), 400

    try:
        forecast_date = datetime.strptime(date_str, '%Y-%m-%d')
    except ValueError:
        return jsonify({"error": "Invalid datetime format. Use YYYY-MM-DD"}), 400

    url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    data = response.json()

    if response.status_code != 200:
        return jsonify({"error": data.get("message", "Failed to fetch forecast")}), 400

    filtered_forecast = []
    for forecast in data.get("list", []):
        forecast_time = datetime.fromtimestamp(forecast["dt"])
        if forecast_time.date() == forecast_date.date():
            filtered_forecast.append(forecast)

    return jsonify({
        "city": data.get("city", {}).get("name"),
        "date": date_str,
        "forecasts": filtered_forecast
    })

if __name__=="__main__":
    app.run(debug=True)
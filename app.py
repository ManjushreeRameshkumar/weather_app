from flask import Flask, request ,redirect,render_template
import requests


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

if __name__=="__main__":
    app.run(debug=True)
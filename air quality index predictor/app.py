from flask import Flask, render_template, request
import pickle

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')
# prajyot birajdar
# prajyotbirajada1998@gmail.com

@app.route('/', methods=['POST'])
def home_post():
    so2 = request.form['so2']
    no2 = request.form['no2']
    rspm = request.form['rspm']
    spm = request.form['spm']
    if len(so2) == 0 or len(no2) == 0 or len(rspm) == 0 or len(spm) == 0:
        result = "Please give missing value from above , unable to calculate Air quality index"

    else:
        soi = calculate_si(float(str(so2)))
        noi = calculate_ni(float(str(no2)))
        rspmi = calculate_(float(str(rspm)))
        spmi = calculate_spi(float(str(spm)))

        with open(r"model", "rb") as f:
            model = pickle.load(f)

        aqi = float(model.predict([[soi, noi, rspmi, spmi]]))

        quality = aqi_analysis(aqi)

        result = f"The Air quality of given data is : {aqi} and according to indian standard air quality is: {quality} "

    return render_template('index.html', output=result, so=so2, ni=no2, rsm=rspm, pm=spm)


def aqi_analysis(x):
    if x <= 50:
        return "Good"
    elif x > 50 and x <= 100:
        return "Moderate"
    elif x > 100 and x <= 200:
        return "Poor"
    elif x > 200 and x <= 300:
        return "Unhealthy"
    elif x > 400:
        return "Hazardous"


def calculate_si(so2):
    si = 0
    if so2 <= 40:
        si = so2 * (50 / 40)
    if so2 > 40 and so2 <= 80:
        si = 50 + (so2 - 40) * (50 / 40)
    if (so2 > 80 and so2 <= 380):
        si = 100 + (so2 - 80) * (100 / 300)
    if (so2 > 380 and so2 <= 800):
        si = 200 + (so2 - 380) * (100 / 800)
    if (so2 > 800 and so2 <= 1600):
        si = 300 + (so2 - 800) * (100 / 800)
    if (so2 > 1600):
        si = 400 + (so2 - 1600) * (100 / 800)
    return si


def calculate_ni(no2):
    ni = 0
    if (no2 <= 40):
        ni = no2 * 50 / 40
    elif (no2 > 40 and no2 <= 80):
        ni = 50 + (no2 - 14) * (50 / 40)
    elif (no2 > 80 and no2 <= 180):
        ni = 100 + (no2 - 80) * (100 / 100)
    elif (no2 > 180 and no2 <= 280):
        ni = 200 + (no2 - 180) * (100 / 100)
    elif (no2 > 280 and no2 <= 400):
        ni = 300 + (no2 - 280) * (100 / 120)
    else:
        ni = 400 + (no2 - 400) * (100 / 120)
    return ni


def calculate_(rspm):
    rpi = 0
    if (rpi <= 30):
        rpi = rpi * 50 / 30
    elif (rpi > 30 and rpi <= 60):
        rpi = 50 + (rpi - 30) * 50 / 30
    elif (rpi > 60 and rpi <= 90):
        rpi = 100 + (rpi - 60) * 100 / 30
    elif (rpi > 90 and rpi <= 120):
        rpi = 200 + (rpi - 90) * 100 / 30
    elif (rpi > 120 and rpi <= 250):
        rpi = 300 + (rpi - 120) * (100 / 130)
    else:
        rpi = 400 + (rpi - 250) * (100 / 130)
    return rpi


def calculate_spi(spm):
    spi = 0
    if (spm <= 50):
        spi = spm
    if (spm < 50 and spm <= 100):
        spi = spm
    elif (spm > 100 and spm <= 250):
        spi = 100 + (spm - 100) * (100 / 150)
    elif (spm > 250 and spm <= 350):
        spi = 200 + (spm - 250)
    elif (spm > 350 and spm <= 450):
        spi = 300 + (spm - 350) * (100 / 80)
    else:
        spi = 400 + (spm - 430) * (100 / 80)
    return spi


if __name__ == '__main__':
    app.run(debug=True)

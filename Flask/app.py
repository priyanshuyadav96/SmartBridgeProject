import numpy as np
import pickle
import pandas as pd
from flask import Flask, request, render_template

app = Flask(__name__, static_url_path='/Flask/static')
model = pickle.load(open('model.pkl', 'rb'))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/predict', methods=['GET','POST'])
def predict():
    if request.method == "POST":
        Gender = request.form["Gender"]
        Hemoglobin = request.form["Hemoglobin"]
        MCH = request.form["MCH"]
        MCHC = request.form["MCHC"]
        MCV = request.form["MCV"]
        if Gender=='' or Hemoglobin=='' or MCH=='' or MCHC=='' or MCV=='':
            return render_template("predict.html", prediction_text="Enter valid numbers")
        Gender=float(Gender)
        Hemoglobin=float(Hemoglobin)
        MCH=float(MCH)
        MCHC=float(MCHC)
        MCV=float(MCV)
        features_values = np.array([[Gender, Hemoglobin, MCH, MCHC, MCV]])  # reshape to 2D array
        df = pd.DataFrame(features_values, columns=['Gender', 'Hemoglobin', 'MCH', 'MCHC', 'MCV'])
        print(df)

        prediction = model.predict(df)
        print(prediction[0])
        result = prediction[0]

        if prediction[0] == 0:
            result = "You don't have any Anemic Disease"
        elif prediction[0] == 1:
            result = "You have anemic disease"

        text = "Hence, based on calculation: "
        return render_template("predict.html", prediction_text=text + str(result))
    else:
        return render_template('predict.html')

if __name__ == "__main__":
    app.run(debug=True, port=5000)
from flask import Flask, request, jsonify
import os
import pickle
import sqlite3
from sklearn.model_selection import cross_val_score, train_test_split
import pandas as pd


os.chdir(os.path.dirname(__file__))

app = Flask(__name__)
app.config['DEBUG'] = True

@app.route("/", methods=['GET'])
def hello():
    return "Bienvenido a mi API del modelo advertising"

# 1. Endpoint que devuelva la predicción de los nuevos datos enviados mediante argumentos en la llamada
@app.route('/v1/predict', methods=['GET'])
def predict():
    model = pickle.load(open('data/advertising_model','rb'))

    tv = request.args.get('TV', None)
    radio = request.args.get('radio', None)
    newspaper = request.args.get('newspaper', None)

    if tv is None or radio is None or newspaper is None:
        return "Missing args, the input values are needed to predict"
    else:
        prediction = model.predict([[int(tv),int(radio),int(newspaper)]])
        return "The prediction of sales investing that amount of money in TV, radio and newspaper is: " + str(round(prediction[0],2)) + 'k €'

# 1. Ofrezca la predicción de ventas a partir de todos los valores de gastos en publicidad. (/v2/predict)
@app.route('/v2/predict_bd', methods=['GET'])
def predict_bd():
    query = "SELECT * FROM Advertising;"
    conn = sqlite3.connect('ejercicio/data/Advertising.db')
    crsr = conn.cursor()
    crsr.execute(query)
    ans = crsr.fetchall()
    conn.close()
    names = [description[0] for description in crsr.description]
    df=pd.DataFrame(ans,columns=names).drop(columns=['sales'])
    model = pickle.load(open('data/advertising_model','rb'))

    predictions = model.predict(df)

    rounded_predictions = [round(pred, 2) for pred in predictions]


    predictions_dict = {"predictions": rounded_predictions}

    return jsonify(predictions_dict)

# 2. Un endpoint para almacenar nuevos registros en la base de datos que deberás crear previamente.(/v2/ingest_data)
@app.route('/v2/ingest_data', methods=['POST'])
def ingest_data():
    conn = sqlite3.connect('ejercicio/data/Advertising.db')
    crsr = conn.cursor()
    data = request.get_json()
    values = [(data['TV'], data['radio'], data['newspaper'], data['sales'])]
    crsr.executemany('INSERT INTO Advertising (TV, radio, newspaper, sales) VALUES (?, ?, ?, ?);', values)
    conn.commit()
    conn.close()

    return jsonify({'message': 'Base de Datos actualizados'})

#3. Posibilidad de reentrenar de nuevo el modelo con los posibles nuevos registros que se recojan. (/v2/retrain)

@app.route('/v2/retrain', methods=['POST'])
def retrain():
    conn = sqlite3.connect('ejercicio/data/Advertising.db')
    crsr = conn.cursor()
    data = request.get_json()
    values = [(data['TV'], data['radio'], data['newspaper'], data['sales'])]
    crsr.executemany('INSERT INTO Advertising (TV, radio, newspaper, sales) VALUES (?, ?, ?, ?);', values)
    conn.commit()
    
    query = "SELECT * FROM Advertising;"
    crsr.execute(query)
    ans = crsr.fetchall()
    conn.close()
    names = [description[0] for description in crsr.description]
    df=pd.DataFrame(ans,columns=names)
    model = pickle.load(open('data/advertising_model','rb'))
    X = df[["TV", "newspaper", "radio"]]
    y = df["sales"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=10)
    model.fit(X_train, y_train)
    pred = model.predict(X_test)

    pred = [round(t, 2) for t in pred]
    conn.close()

    return jsonify({"message": "Modelo reentrenado con éxito.", "predictions": pred})

app.run()

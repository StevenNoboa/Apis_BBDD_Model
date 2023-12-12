from flask import Flask, request, jsonify
import os
import pickle
import sqlite3
from sklearn.model_selection import cross_val_score, train_test_split
import pandas as pd
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

app = Flask(__name__)
app.config['DEBUG'] = True

@app.route("/", methods=['GET'])
def hello():
    return "Bienvenido a mi API del modelo advertising"

# 1. Endpoint que devuelva la predicción de los nuevos datos enviados mediante argumentos en la llamada
@app.route('/v2/predict', methods=['GET'])
def predict_list():
    model = pickle.load(open('data/advertising_model','rb'))
    data = request.get_json()

    input_values = data['data'][0]
    tv, radio, newspaper = map(int, input_values)

    prediction = model.predict([[tv, radio, newspaper]])
    return jsonify({'prediction': round(prediction[0], 2)})



# 2. Un endpoint para almacenar nuevos registros en la base de datos que deberás crear previamente.(/v2/ingest_data)
@app.route('/ingest', methods=['POST'])
def add_data():
    data = request.get_json()

    for row in data.get('data', []):
        tv, radio, newspaper, sales = row
        query = "INSERT INTO Advertising (tv, radio, newspaper, sales) VALUES (?, ?, ?, ?)"
        connection = sqlite3.connect('ejercicio/data/Advertising.db')
        crsr = connection.cursor()
        crsr.execute(query, (tv, radio, newspaper, sales))
        connection.commit()
        connection.close()

    return jsonify({'message': 'Datos ingresados correctamente'})

#3. Posibilidad de reentrenar de nuevo el modelo con los posibles nuevos registros que se recojan. (/v2/retrain)

@app.route('/v2/retrain', methods=['POST'])
def retrain():
    conn = sqlite3.connect('ejercicio/data/Advertising.db')
    crsr = conn.cursor()
    query = "SELECT * FROM Advertising;"
    crsr.execute(query)
    ans = crsr.fetchall()
    conn.close()
    names = [description[0] for description in crsr.description]
    df = pd.DataFrame(ans, columns=names)

        # Cargar el modelo existente
    model = pickle.load(open('data/advertising_model', 'rb'))

        # Dividir los datos en características (X) y etiquetas (y)
    X = df[["TV", "newspaper", "radio"]]
    y = df["sales"]

        # Dividir los datos en conjuntos de entrenamiento y prueba
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=10)

        # Reentrenar el modelo con los nuevos datos
    model.fit(X_train, y_train)

        # Guardar el modelo reentrenado
    pickle.dump(model, open('advertising_model_2', 'wb'))

    return jsonify({'message': 'Modelo reentrenado correctamente.'})

app.run()

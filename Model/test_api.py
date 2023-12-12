import requests
import os
from flask import Flask
import pytest


def test_ingest_endpoint():
    url = 'http://127.0.0.1:5000/ingest'  
    data = {'data': [[100, 100, 200, 3000], [200, 230, 500, 4000]]}
    response = requests.post(url, json=data)
    assert response.status_code == 200
    assert response.json() == {'message': 'Datos ingresados correctamente'}

def test_predict_endpoint():
    url = 'http://127.0.0.1:5000/v2/predict'  
    data = {'data': [[100, 100, 200]]} 
    response = requests.get(url, json=data)
    assert response.status_code == 200
    assert 'prediction' in response.json()

def test_retrain_endpoint():
    url = 'http://127.0.0.1:5000/v2/retrain'  
    response = requests.post(url)
    assert response.status_code == 200
    assert response.json() == {'message': 'Modelo reentrenado correctamente.'}


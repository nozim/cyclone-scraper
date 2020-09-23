from flask import Flask, jsonify
from models import app, CycloneHistory, CycloneForecast


@app.route("/api/v1/cyclones/history", methods=["GET"])
def history():
    hist = CycloneHistory.query.all()
    return jsonify(hist)


@app.route("/api/v1/cyclones/forecast", methods=["GET"])
def forecast():
    forecast = CycloneForecast.query.all()
    return jsonify(forecast)

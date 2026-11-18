"""Sejf sekretow i kalkulator - celowo podatna aplikacja do laboratorium 7.

Uruchamiaj wylacznie lokalnie, w kontenerze z pakietu. Dane sa fikcyjne.
"""
import sqlite3
import re

from flask import Flask, render_template, request

app = Flask(__name__)
BAZA = "file:/dane/sekrety.db?mode=ro"


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/sekret")
def sekret():
    klucz = request.args.get("klucz", "")
    zapytanie = "SELECT wlasciciel, sekret FROM sekrety WHERE klucz = ?"
    wiersze, blad = [], None
    try:
        with sqlite3.connect(BAZA, uri=True) as db:
            wiersze = db.execute(zapytanie, (klucz,)).fetchall()
    except sqlite3.Error:
        app.logger.exception("Błąd bazy danych dla klucza %r", klucz)
        blad = "Wystąpił błąd bazy danych."
    return render_template("sekret.html", klucz=klucz, zapytanie=zapytanie, wiersze=wiersze, blad=blad)


@app.route("/kalkulator")
def kalkulator():
    wyrazenie = request.args.get("wyrazenie")
    if wyrazenie is None:
        return render_template("kalkulator.html", wyrazenie="", wynik=None)
    if len(wyrazenie) > 100:
        return "Wyrażenie za długie (maks. 100 znaków).", 400
    wzorzec = r"\s*(-?\d+(?:\.\d+)?)\s*([+\-*/])\s*(-?\d+(?:\.\d+)?)\s*"
    dopasowanie = re.fullmatch(wzorzec, wyrazenie)
    if not dopasowanie:
        return "Nieprawidłowe wyrażenie.", 400
    a = float(dopasowanie.group(1))
    operator = dopasowanie.group(2)
    b = float(dopasowanie.group(3))
    dzialania = {
        "+": lambda x, y: x + y,
        "-": lambda x, y: x - y,
        "*": lambda x, y: x * y,
        "/": lambda x, y: x / y,
    }
    try:
        wynik = dzialania[operator](a, b)
    except ZeroDivisionError:
        return "Dzielenie przez zero.", 400
    return render_template("kalkulator.html", wyrazenie=wyrazenie, wynik=wynik)



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)

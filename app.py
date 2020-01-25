import os

import pandas as pd
import numpy as np

from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
    """Return the homepage."""
    return render_template("index.html")

@app.route("/d3")
def dpage():
    return render_template("d3.html")

@app.route("/model")
def ppage():
    return render_template("model.html")

if __name__ == "__main__":
    app.run()
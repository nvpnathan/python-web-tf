from flask import Flask, request, url_for, redirect, render_template
from datetime import datetime
import requests
import os
import subprocess
from dotenv import load_dotenv
import json

load_dotenv()  # take environment variables from .env.

app = Flask(__name__)


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/status")
def get_tf_state():
    try:
        tf_state = subprocess.run(['terraform', 'show'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                  universal_newlines=True)
        output = tf_state.stdout
        print(output.strip())
    except subprocess.CalledProcessError as e:
        return "An error occurred while trying to fetch terraform state."
    return render_template('status.html', tf_output=output.strip())


@app.route("/update", methods=['POST'])
def update_tf_infra():
    if request.method == 'POST':
        try:
            tf_state = subprocess.run(['terraform', 'apply'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                      universal_newlines=True)
            output = tf_state.stdout
            print(output.strip())
        except subprocess.CalledProcessError as e:
            return "An error occurred while trying to update terraform state."
        return render_template('update.html', tf_output=output.strip())


if __name__ == '__main__':
    # Run the app
    app.run(port=8080, host="0.0.0.0", debug=True)


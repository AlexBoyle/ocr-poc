import os.path

from flask import Flask, Response
import subprocess

app = Flask(__name__,
static_url_path='/static', 
static_folder='output')

@app.route('/check/<number>')
def success(number):
    output = subprocess.run(["./parse.sh", "./images/"+ number + "-receipt.jpg"],  stdout=subprocess.PIPE).stdout.decode('utf-8')
    return "<pre>" + output + "</pre><img src=/static/final.jpg/><img src=/static/inital.jpg/>"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
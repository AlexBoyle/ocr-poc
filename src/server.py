import os.path

from flask import Flask, Response
import subprocess
import proceser
app = Flask(__name__,
static_url_path='/static', 
static_folder='output')

@app.route('/check/<number>')
def success(number):
    output = proceser.process("./images/"+ number + "-receipt.jpg")
    return "<img style='width: 40%;' src=/static/final.webp/><img style='width: 40%;' src=/static/inital.webp/><pre>" + output + "</pre>"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
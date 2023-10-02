import os.path

from flask import Flask, Response
import subprocess
from src.server.server import proceser

app = Flask(__name__, static_folder='/main/client/build')

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path != "" and os.path.exists(app.static_folder + '/' + path):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')


@app.route('/check/<number>')
def success(number):
    output = proceser.process("./images/" + number + "-receipt.jpg")
    return "<img style='width: 40%;' src=/static/final.webp/><img style='width: 40%;' src=/static/inital.webp/><pre>" + output + "</pre>"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
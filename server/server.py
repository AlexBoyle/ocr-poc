import os.path

from flask import Flask, Response, render_template,send_file
import subprocess
import proceser

app = Flask(
    __name__,
    static_url_path='',
    static_folder='../client/build'
)
html_content=""
with open('../client/build/index.html', 'r') as html_file:
    html_content = html_file.read()


@app.route('/check/<number>')
def success(number):
    output = proceser.process("../images/" + number + "-receipt.jpg", number, None)
    return "<pre>" + output + "</pre>"

@app.route('/list-debug-images/<string:runId>')
def listDebugImages(runId):
    return os.listdir('../staticImages/'+runId)
@app.route('/debug-images/<string:runId>/<string:imageName>')
def getDebugImages(runId, imageName):
    return send_file('../staticImages/'+runId+'/'+ imageName, mimetype='image/webp')
@app.route('/', defaults={'path': ""})
@app.route('/<string:path>')
def index_redir(path):
    return html_content

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
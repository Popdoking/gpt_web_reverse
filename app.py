import json
import connGPT
from flask import Flask, render_template, request, Response

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    question = json.loads(request.data.decode('utf-8'))['input_text']
    return Response(connGPT.getQuestion(question))

if __name__ == '__main__':
    connGPT.getTocken()
    app.run('0.0.0.0', 1234)

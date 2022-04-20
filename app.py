from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
import certifi

app = Flask(__name__)
ca = certifi.where()

client = MongoClient('mongodb+srv://test:sparta@cluster0.zgm92.mongodb.net/myFirstDatabase?retryWrites=true&w=majority',
                     tlsCAFile=ca)
db = client.cafe


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/detail', methods=["POST"])
def detail():
    cafe = request.form['cafe']
    image = request.form['image']
    data = {
        'cafe':cafe,
        'image':image
    }
    print(data)
    return render_template('detail.html', data=data)

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)

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


@app.route('/post_comment', methods=["POST"])
def post_comment():
    cafe = request.form['cafe']
    nickname = request.form['nickname']
    comment = request.form['comment']
    doc = {'cafe': cafe, 'nickname': nickname, 'comment': comment}
    db.comment.insert_one(doc)
    return jsonify({'msg':"댓글 작성 완료"})

@app.route('/comment_list', methods=["GET"])
def comment_list():
    cafes = request.args.get('cafe')
    cafe_list = list(db.comment.find({"cafe":{'$regex': cafes }}, {'_id': False}))
    return jsonify({'cafe_list': cafe_list})



if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)

from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
import certifi
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


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
    code = request.form['code']
    dats_list = list();
    data = {
        'cafe':cafe,
        'image':image,
        'code':code
    }
    dats_list.append(data)
    return render_template('detail.html', data=data)


@app.route('/post_comment', methods=["POST"])
def post_comment():
    cafe = request.form['cafe']
    nickname = request.form['nickname']
    comment = request.form['comment']
    cafe_list = list(db.comment.find({"cafe": {'$regex': cafe}}, {'_id': False}))
    count = len(cafe_list)+1
    doc = {'num':count,'cafe': cafe, 'nickname': nickname, 'comment': comment}
    db.comment.insert_one(doc)
    return jsonify({'msg':"댓글 작성 완료"})

@app.route('/comment_list', methods=["GET"])
def comment_list():
    cafes = request.args.get('cafe')
    cafe_list = list(db.comment.find({"cafe":{'$regex': cafes }}, {'_id': False}))
    return jsonify({'cafe_list': cafe_list})

@app.route('/comment_del', methods=["POST"])
def comment_del():
    num = request.form['num']
    db.comment.delete_one({'num':int(num)})
    return jsonify({'msg': "삭제되었습니다."})

@app.route('/comment_update', methods=["POST"])
def comment_update():
    num = request.form['num']
    comment= request.form['comment']
    nickname = request.form['nickname']
    db.comment.update_one({'num':int(num)}, {'$set': {'nickname': nickname,'comment':comment}})
    return jsonify({'msg': "수정되었습니다.."})

@app.route('/detail_info', methods=["GET"])
def detail_info():
    caps = DesiredCapabilities().CHROME
    caps["pageLoadStrategy"] = "none"
    cafe_cade = request.args.get('code')

    url ='http://place.map.kakao.com/'+cafe_cade

    options = Options()
    options.add_argument('--no-sandbox')
    options.add_argument('--headless')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(url)
    #driver.implicitly_wait(10)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#mArticle > div.cont_essential")))
    data = driver.page_source
    soup = BeautifulSoup(data, 'html.parser')
    address = soup.select_one("#mArticle > div.cont_essential > div.details_placeinfo > div > div > span")
    times = soup.select_one("#mArticle > div.cont_essential > div.details_placeinfo > div:nth-child(3) > div > div > ul > li> span")
    homepage = soup.select_one(
        "#mArticle > div.cont_essential > div.details_placeinfo > div:nth-child(4) > div > div > a")
    tell_num = soup.select_one(
        "#mArticle > div.cont_essential > div.details_placeinfo > div:nth-child(5) > div > div > span")
    return jsonify({'address':address.text,'time':times.text,'homepage':homepage['href'],'tell':tell_num.text})

@app.route('/cafe_list', methods=["GET"])
def cafe_list():
    cafes = request.args.get('city')
    lists = list(db.cafe.find({"add":{'$regex': cafes }}, {'_id': False}))
    return jsonify({'list': lists})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)

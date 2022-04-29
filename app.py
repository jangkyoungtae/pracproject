from flask import Flask, render_template, request, jsonify
from selenium.common.exceptions import NoSuchElementException

app = Flask(__name__)
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

import requests
from bs4 import BeautifulSoup
import time
import re
from pymongo import MongoClient
import certifi
ca = certifi.where()
client = MongoClient('mongodb+srv://test:sparta@cluster0.zgm92.mongodb.net/Cluster0?retryWrites=true&w=majority', tlsCAFile=ca)
db = client.cafe

@app.route('/')
def home():
    return render_template('main.html')

@app.route('/main', methods=["POST"])
def main():
    search = request.form['search']
    data = {
        'search': search
    }
    return render_template('index.html', data=data)

@app.route('/comment', methods=["POST"])
def comment():
    title = request.form['title']
    image = request.form['image']
    cafeUrl = request.form['cafeUrl']
    # cafeCode=cafeUrl.split('/')[3]
    data = {
        'title': title,
        'image': image,
        'cafeUrl': cafeUrl
    }

    return render_template('comment.html', data=data)

@app.route("/cafe", methods=["GET"])
def cafe_get():
    search_receive = request.args.get('search_give')
    cafe_list = list(db.cafe.find({'add': {'$regex': search_receive}}, {'_id': False}))
    return jsonify({'cafelist': cafe_list})
    # db.cafe.drop() db 저장된거 다 삭제


@app.route("/info", methods=["GET"])
def info_get():
    url_receive = request.args.get('url_give')
    options = webdriver.ChromeOptions()
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('window-size=1920x1080')
    options.add_argument("no-sandbox")
    # options.add_argument('--single-process')
    options.add_argument("disable-gpu")
    options.add_argument("lang=ko_KR")
    # options.add_experimental_option("excludeSwitches", ["enable-automation"])
    # options.add_experimental_option('useAutomationExtension', False)
    options.add_argument("headless")  # 크롬창 안뜨게 해줌!!
    options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.41 Safari/537.36")
    # # options.add_argument('--disable-blink-features=AutomationControlled')
    # options.add_argument("--disable-extensions")
    # options.add_experimental_option('useAutomationExtension', False)
    # options.add_experimental_option("excludeSwitches", ["enable-automation"])

    # driver = webdriver.Chrome('./chromedriver', chrome_options=options)
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), chrome_options=options)
    # driver = webdriver.Chrome(executable_path='/Users/choijihoon/Desktop/hanghae/pracproject/chromedriver', chrome_options=options)
    # driver.get(url_receive)
    driver.get(url_receive)
    driver.implicitly_wait(3)

    # image = driver.find_elements_by_css_selector('#mArticle > div.cont_photo > div.photo_area > ul > li > a')[0].get_attribute(
    #     'style').split('"')[1].split(')')[0].lstrip('/')
    # title = driver.find_element_by_xpath('//*[@id="mArticle"]/div[1]/div[1]/div[2]/div/h2').text

    try:
        address = driver.find_element(By.XPATH, '//*[@id="mArticle"]/div[1]/div[2]/div[1]/div/span[1]').text
        # address = driver.find_element_by_xpath('//*[@id="mArticle"]/div[1]/div[2]/div[1]/div/span[1]').text
        time = driver.find_element_by_xpath('//*[@id="mArticle"]/div[1]/div[2]/div[2]/div/div[1]/ul/li/span').text
        # //*[@id="mArticle"]/div[1]/div[2]/div[2]/div/div[1]/ul/li/span/span
        url = driver.find_element_by_xpath('//*[@id="mArticle"]/div[1]/div[2]/div[3]/div/div/a').get_attribute('href')
        phoneNumber = driver.find_element_by_xpath('//*[@id="mArticle"]/div[1]/div[2]/div[4]/div/div/span/span[1]').text
    except NoSuchElementException:
        phoneNumber = "없음"
    driver.quit()
    return jsonify({'address': address, 'time': time, 'url': url, 'phoneNumber': phoneNumber})

@app.route("/comment_list", methods=["POST"])
def comment_post():
    name_receive = request.form['name_give']
    comment_receive = request.form['comment_give']
    title_receive = request.form['title_give']
    commentList = list(db.comments.find({'title': {'$regex': title_receive}}, {'_id': False}))
    count = len(commentList) + 1

    doc = {
        'name': name_receive,
        'comment': comment_receive,
        'title':title_receive,
        'num':count,

    }
    db.comments.insert_one(doc)
    return jsonify({'msg': '등록 완료!'})

@app.route("/comment_list/update", methods=["POST"])
def comment_update():
    title_receive = request.form['title_give']
    num_receive = request.form['num_give']
    comment_receive = request.form['comment_give']
    db.comments.update_one({'title': {'$regex': title_receive}, 'num': int(num_receive)}, {'$set': {'comment': comment_receive}})
    return jsonify({'msg': '수정 완료!'})

@app.route("/comment_list/cancel", methods=["POST"])
def comment_cancel():
    title_receive = request.form['title_give']
    num_receive = request.form['num_give']
    db.comments.delete_one({'title': {'$regex': title_receive}, 'num': int(num_receive)})
    return jsonify({'msg': '삭제 완료!'})

@app.route("/comment_list", methods=["GET"])
def comment_get():
    title_receive = request.args.get('title_give')
    comment_list = list(db.comments.find({'title': {'$regex': title_receive}}, {'_id': False}))
    return jsonify({'comment_list': comment_list})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
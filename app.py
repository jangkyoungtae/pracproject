from flask import Flask, render_template, request, jsonify
from selenium.common.exceptions import NoSuchElementException

app = Flask(__name__)
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
# options = webdriver.ChromeOptions()
# options.add_argument("headless")
# driver = webdriver.Chrome('./chromedriver.exe')
# driver.implicitly_wait(3)
# driver.get('https://map.kakao.com/')
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
    return render_template('index.html')

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

# @app.route('/searchList')
# def searchList():
#     return render_template('index.html')



# @app.route("/cafe", methods=["POST"])
# def cafe_post():
#     search_receive =request.form['search_give']

#     return jsonify({'msg': '검색 완료!'})

@app.route("/cafe", methods=["GET"])
def cafe_get():
    search_receive = request.args.get('search_give')
    cafe_list = list(db.cafe.find({'add': {'$regex': str(search_receive) }}, {'_id': False}))
    return jsonify({'cafelist': cafe_list})
    # db.cafe.drop() db 저장된거 다 삭제

@app.route("/info", methods=["GET"])
def info_get():
    url_receive = request.args.get('url_give')
    options = webdriver.ChromeOptions()
    options.add_argument("headless")  # 크롬창 안뜨게 해줌!!
    driver = webdriver.Chrome('./chromedriver', chrome_options=options)
    driver.implicitly_wait(3)
    driver.get(url_receive)
    # image = driver.find_elements_by_css_selector('#mArticle > div.cont_photo > div.photo_area > ul > li > a')[0].get_attribute(
    #     'style').split('"')[1].split(')')[0].lstrip('/')
    # title = driver.find_element_by_xpath('//*[@id="mArticle"]/div[1]/div[1]/div[2]/div/h2').text
    try:
        add = driver.find_element_by_xpath('//*[@id="mArticle"]/div[1]/div[2]/div[1]/div/span[1]').text
        time = driver.find_element_by_xpath('//*[@id="mArticle"]/div[1]/div[2]/div[2]/div/div[1]/ul/li/span').text
        # //*[@id="mArticle"]/div[1]/div[2]/div[2]/div/div[1]/ul/li/span/span
        url = driver.find_element_by_xpath('//*[@id="mArticle"]/div[1]/div[2]/div[3]/div/div/a').get_attribute('href')
        phoneNumber = driver.find_element_by_xpath('//*[@id="mArticle"]/div[1]/div[2]/div[4]/div/div/span/span[1]').text
    except NoSuchElementException:
        phoneNumber = "없음"

    driver.quit()
    return jsonify({'add': add, 'time': time, 'url': url, 'phoneNumber': phoneNumber})

@app.route("/comment_list", methods=["POST"])
def comment_post():
    name_receive = request.form['name_give']
    comment_receive = request.form['comment_give']
    title_receive = request.form['title_give']

    doc = {
        'name': name_receive,
        'comment': comment_receive,
        'title':title_receive
    }
    db.comments.insert_one(doc)
    return jsonify({'msg': '등록 완료!'})


@app.route("/comment_list", methods=["GET"])
def comment_get():
    title_receive = request.args.get('title_give')
    comment_list = list(db.comments.find({'title': {'$regex': str(title_receive)}}, {'_id': False}))
    return jsonify({'comment_list': comment_list})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
import requests
from bs4 import BeautifulSoup
from flask import Flask, render_template, jsonify

app = Flask(__name__)


# HTML 화면 보여주기
@app.route('/')
def home():
    return render_template('index.html')


# API 역할을 하는 부분

# 뉴스, 날씨, 쇼핑, 경제 웹크롤링 api
# 뉴스
@app.route('news', methods=['GET'])
def news():
    html = requests.get('https://news.naver.com/')
    soup = BeautifulSoup(html.text, 'html.parser')

    data1 = soup.find('div', {'id': 'today_main_news'})


# 날씨
@app.route('/weather', methods=['GET'])
def weather():
    html = requests.get('https://search.naver.com/search.naver?query=날씨')
    soup = BeautifulSoup(html.text, 'html.parser')

    data1 = soup.find('div', {'class': 'weather_box'})

    find_address = data1.find('span', {'class': 'btn_select'}).text
    find_currenttemp = data1.find('span', {'class': 'todaytemp'}).text
    find_details = data1.find('p', {'class': 'cast_txt'}).text

    data2 = data1.findAll('dd')
    find_dust = data2[0].find('span', {'class': 'num'}).text
    find_ultra_dust = data2[1].find('span', {'class': 'num'}).text
    find_ozone = data2[2].find('span', {'class': 'num'}).text

    return jsonify({'위치': find_address, '현재 기온': find_currenttemp, '상세 날씨': find_details, '미세먼지': find_dust, '초미세먼지': find_ultra_dust, '오존': find_ozone})

# 쇼핑
@app.route('/shopping', methods=['GET'])
def shopping():
    
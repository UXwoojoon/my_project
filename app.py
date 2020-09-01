import requests
from datetime import datetime
from bs4 import BeautifulSoup
from flask import Flask, render_template, jsonify

app = Flask(__name__)


# HTML 화면 보여주기
@app.route('/')
def home():
    return render_template('index.html')


# API 역할을 하는 부분

#날짜불러오기
@app.route('/date', methods=['GET'])
def bringDate():
    datetoday = datetime.today()
    DT = datetoday.strftime("20%y.%m.%d")
    return DT

# 뉴스, 날씨, 쇼핑, 경제 웹크롤링 api
# 뉴스
@app.route('/headline', methods=['GET'])
def headline():
    html = requests.get('https://news.naver.com/')
    soup = BeautifulSoup(html.text, 'html.parser')

    data = soup.find('div', {'id': 'today_main_news'})
    headline_title = data.select_one('div[class=hdline_flick_item] > a > div > p').text
    headline_img = data.select_one('div[class=hdline_flick_item] > a > img').get('src')
    headline_list = data.select('ul > li')
    hl_array = []
    for list in headline_list:
        hl_array.append(list.select_one('div[class=hdline_article_tit] > a').text)

    return jsonify({'헤드라인 이미지': headline_img, '헤드라인 타이틀': headline_title, '기사들': hl_array})



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
    html = requests.get('https://search.shopping.naver.com/best100v2/main.nhn')
    soup = BeautifulSoup(html.text, 'html.parser')

    data1 = soup.select('ul[id=popular_srch_lst] > li')
    topten = []
    for line in data1:
        rank = line.select_one('em').text
        name = line.select_one('span[class=txt]').text
        variation = line.select_one('span[class=vary]').text
        tt_element = {'순위': rank, '이름': name, '변동': variation}
        topten.append(tt_element)

    return jsonify({'10위': topten, 'msg': 'success'})




#금융
@app.route('/finance', methods=['GET'])
def finance():
    html = requests.get('https://finance.naver.com/')
    soup = BeautifulSoup(html.text, 'html.parser')

    kosdaq = soup.select_one('div[class=section_stock] > div.kosdaq_area > div.heading_area > a > span > span.num').text
    kospi = soup.select_one('div[class=section_stock] > div.kospi_area > div.heading_area > a > span > span.num').text

    top_traded = soup.select('tbody[id=_topItems1] > tr')
    top_price = soup.select('tbody[id=_topItems4] > tr')
    toptraded_array = []
    topprice_array = []
    for table in top_traded:
        toptraded_array.append(table.select_one('th > a').text)
    for table in top_price:
        topprice_array.append(table.select_one('th > a').text)

    return jsonify({'코스피': kospi, '코스닥': kosdaq, '거래상위': toptraded_array, '시가총액': topprice_array})




if __name__ == '__main__':
    app.run('0.0.0.0',port=5000,debug=True)


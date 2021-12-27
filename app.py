from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

import requests
from bs4 import BeautifulSoup

from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.dbsparta


# 홈화면
@app.route('/')
def home():
    return render_template('index.html')


# DB에 저장된 영화 목록을 차순 정렬로 보여 주는 API
@app.route('/api/list', methods=['GET'])
def show_stars():
    star = list(db.BBBBBBBBBB.find({}, {'_id': False}).sort('like', -1))
    return jsonify({'all_star': star})


# 좋아요 버튼 누르면 1개 증가하는 API
@app.route('/api/like', methods=['POST'])
def like_movie():
    title_receive = request.form['title_give']
    a_like = db.BBBBBBBBBB.find_one({'title': title_receive})
    current_like = a_like['like']
    new_like = current_like + 1
    db.BBBBBBBBBB.update_one({'title': title_receive}, {'$set': {'like': new_like}})

    return jsonify({'msg': '좋아요!'})


# URL을 입력하면 해당 사이트에서 필요한 정보 크롤링 후 DB에 저장하는 API
@app.route('/api/list', methods=['POST'])
def upload_movie():
    url_receive = request.form['url_give']

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get(url_receive, headers=headers)
    soup = BeautifulSoup(data.text, 'html.parser')

    image = soup.select_one('meta[property="og:image"]')['content']
    title = soup.select_one('meta[property="og:title"]')['content']
    desc = soup.select_one('meta[property="og:description"]')['content']
    url = soup.select_one('meta[property="og:url"]')['content']
    movie_code = url.split('=')[1] #코드 숫자 중 5~6개(숫자) 코드이므로 스플릿을 사용

    doc = {
        'image': image,
        'title': title,
        'desc': desc,
        'like': 0,
        'hate': 0,
        'url': url,  #혹시 몰라 저장...☆
        'movie_code': movie_code
    }
    db.BBBBBBBBBB.insert_one(doc)

    return jsonify({'msg': '업로드 완료!'})

# 검색기능
@app.route('/api/search', methods=['GET'])
def search_movie():
    search_receive = request.args.get('searchData')
    # {'title':{'$regex':search_receive}} 검색창에 적은 글자가 찾을 영화제목에 포함되어 있을시 그영화를 가져옵니다.
    result = list(db.BBBBBBBBBB.find({'title':{'$regex':search_receive}}, {'_id': False}).sort('like', -1))

    return jsonify({'msg': '검색 완료!','result':result})


# 싫어요 버튼 누르면 1개 증가
@app.route('/api/hate', methods=['POST'])
def hate_movie():
    title_receive = request.form['title_give']
    a_hate = db.BBBBBBBBBB.find_one({'title': title_receive})
    current_hate = a_hate['hate']
    new_hate = current_hate + 1
    db.BBBBBBBBBB.update_one({'title': title_receive}, {'$set': {'hate': new_hate}})

    return jsonify({'msg': '싫어요!'})


# 업로드시 url뒤에 있는 코드와 DB에있는 코드를 비교하기 위해 사용합니다.
# db에 코드가 없을시엔 빈값으로 리턴시켜주면
# script에서 새로 업로드 하는지 좋아요를 하는지 체크합니다.
@app.route('/api/code', methods=['POST'])
def movie_code():
    code_receive = request.form['code_give']
    movie = db.BBBBBBBBBB.find_one({'movie_code': code_receive})

    if movie is not None:
        current_code = movie['movie_code']
    else:
        current_code = ""

    return jsonify({'current_code': current_code})



# 중복 된 영화가 있을경우 좋아요+1 입니다.
@app.route('/api/overlap', methods=['POST'])
def duplication():
    code_receive = request.form['code_give']
    movie = db.BBBBBBBBBB.find_one({'movie_code': code_receive})
    current_like = movie['like']
    new_like = current_like + 1
    db.BBBBBBBBBB.update_one({'movie_code': code_receive}, {'$set': {'like': new_like}})

    return jsonify({'msg': '중복되기에 해당 영화에 좋아요+1 !!!'})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)

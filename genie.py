import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient  # pymongo를 임포트 하기(패키지 설치 먼저 해야겠죠?)
client = MongoClient('localhost', 27017)  # mongoDB는 27017 포트로 돌아갑니다.
db = client.dbsparta

headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}

musicURL = 'https://www.genie.co.kr/chart/top200?ditc=D&rtm=N&ymd=20200713'



for page in range(1,5):
    # params 선언, key:value형식
    params = {'pg': page}
    # requests.get에서 params를 추가
    data = requests.get(musicURL, params=params, headers=headers)
    soup = BeautifulSoup(data.text, 'html.parser')
    songs = soup.select('#body-content > div.newest-list > div > table > tbody > tr')
    for song in songs:
        n_tag=song.select_one('td.number').contents[0].strip()
        name=song.select_one('td.info > a').contents[0].strip()
        artist=song.select_one('td.info > a.artist.ellipsis').contents[0].strip()
        print(n_tag,name,artist)
        doc = {
            'rank': n_tag,
            'title': name,
            'artist': artist
        }
        db.ranking.insert_one(doc)



#contents는 처음 텍스트를 가져와 출력해준다. strip()은 빈 공백을 없애준다.
#body-content > div.newest-list > div > table > tbody > tr:nth-child(1) > td.info > a.artist.ellipsis
#body-content > div.newest-list > div > table > tbody > tr:nth-child(1) > td.info > a.title.ellipsis
#body-content > div.newest-list > div > table > tbody > tr:nth-child(2) > td.info > a.artist.ellipsis
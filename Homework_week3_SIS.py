# 신인섭 3주차 과제
import requests
from bs4 import BeautifulSoup

from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.dbsparta

# 타겟 URL을 읽어서 HTML를 받아오고,
headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
data = requests.get('https://www.genie.co.kr/chart/top200?ditc=D&rtm=N&ymd=20200713', headers=headers)

# HTML을 BeautifulSoup이라는 라이브러리를 활용해 검색하기 용이한 상태로 만듦
# soup이라는 변수에 "파싱 용이해진 html"이 담긴 상태가 됨
# 이제 코딩을 통해 필요한 부분을 추출하면 된다.
soup = BeautifulSoup(data.text, 'html.parser')

# 순위테이블 #body-content > div.newest-list > div > table > tbody > tr.list
# 순위 v순위테이블 > td.number
# 문자열 위치 지정([start:stop:step]) + 공백제거(strip())가 동시에 필요. 달달한 맛 문제 code 참고.
# 문자열의 첫줄만 출력할 수 있는 방법은?
# 제목 v순위테이블 > td.info > a.title.ellipsis
# 아티스트 v순위테이블 > td.info > a.artist.ellipsis
songs = soup.select('#body-content > div.newest-list > div > table > tbody >tr.list') # 순위차트의 각 line
for song in songs :
    # rank_info = td.number의 모든 text = 순위 + 빈칸 + (줄바꿈 = \n) + 순위변동정보
    rank_info = song.select_one('td.number').text
#    rank = rank_info[0:2].strip() # 달달한맛 참고
    # 이 아래부턴 직접 만든..
    # 순위 변동정보(span의 text)
    excl_info = song.select_one('span').text
    # rank_info 에서 replace로 순위변동정보와 줄바꿈을 삭제하고 strip으로 빈칸 정리(strip을 안하면 어마어마한 공백이..)
    rank = rank_info.replace(excl_info,'').replace('\n','').strip()
    # 노래 제목. strip 필요
    title = song.select_one('td.info > a.title.ellipsis').text.strip()
    # 아티스트 명
    artist = song.select_one('td.info > a.artist.ellipsis').text
    print(rank, title, artist)
#    db.song_chart.insert_one({'rank': repr(rank) , 'title' : title, 'artist' : artist}) # mongo db insert

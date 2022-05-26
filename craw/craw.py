from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import re
import sys
import io
import os
import time
# 입출력 데이터 형식을 utf-8로 설정
sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding = 'utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding ='utf-8')

# 파일 경로 가져오기
dirName = os.path.dirname(os.path.realpath(__file__))

# chrome driver 옵션 설정
options = webdriver.ChromeOptions()
options.add_argument('--disable-software-rasterizer')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--no-sandbox')
options.add_argument('window-size=1980x1080')
options.add_argument('--ignore-cetificate-errors')

# chrome driver 경로 설정 없이도 최신 chrome driver 사용 가능하게 해주는 함수 
def set_chrome_driver():
    chrome_options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    return driver

# 새로운 화면의 html 정보 저장 
def newtab(url):
	driver.get(url)                                # 현재 url로 접속
	print(url)
	html = driver.page_source                      # 새로운 창의 코드 정보 저장
	return html

# text 추출
def text(html):
    
    last_tab = driver.window_handles[-1]           # 다음 url 화면으로 넘어갈 Handler 선언
    first_tab = driver.window_handles[0]           # 처음 화면으로 돌아올 Handler 선언
    soup = BeautifulSoup(html, 'html.parser')      # 현재 페이지의 html 값 저장
    driver.switch_to.window(window_name=last_tab)# 다음 url 화면으로 넘어감
    time.sleep(3)
    if soup.select_one('body') != None:  
        result = soup.select_one('body').get_text()    # 현재 페이지의 텍스트 값 크롤링
        driver.switch_to.window(window_name=first_tab) # 처음 화면으로 돌아옴
        if result !=None:
            print("saving file...")
            return result

# Save text file
def Savefile(data):
 
    f =open(os.path.join(dirName,'text/')+keyword+'.hwp','a', encoding='utf-8')
    str_data = str(data)
    f.write(str_data)
    f.close()

driver = set_chrome_driver()
# 검색하고자 하는 키워드 입력 변수 = keyword
keyword = "레드원테크놀러지"
# 입력된 키워드를 google에 검색
driver.get('https://www.google.com/search?q='+keyword) # google driver로 url 접속
ht = driver.page_source                                # 현재 페이지의 코드 정보 저장
soup = BeautifulSoup(ht, 'html.parser')                # BeatifulSoup로 현재 페이지의 html 값 저장


for href in soup.find_all('div',{'class':'yuRUbf'}) :  # 현재 page의 모든 url 정보 가져오기
	url = href.find('a')['href']                       # 현재 page의 모든 url 정보 가져오기
	print(type(url))
	html = newtab(url)                                 # newtab 함수 호출
	re = text(html)                                    # text 함수 호출
	Savefile(re)                                       # Savefile 함수 호출
 
driver.quit()

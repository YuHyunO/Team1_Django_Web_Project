import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import csv

f = open('C://Users//kosmo//Desktop//team1_Django_Wed_Project//구월점_codek-room.csv', 'w',encoding='cp949', newline='')
wr = csv.writer(f)
wr.writerow(['지점명', '주소,전화번호,운영시간','카페이미지url'])

path = "C://Users//kosmo//Desktop//team1_Django_Wed_Project//chromedriver.exe"
driver = webdriver.Chrome(path)
url = "http://www.code-k.co.kr/sub/code_sub02_2.html"
driver.get(url)

driver.maximize_window()
time.sleep(1)

datas = []

for x in range(1):
    room = driver.find_element(By.XPATH, '//*[@id="cont_text"]/ul[1]/a[2]/li').text
    call = driver.find_element(By.XPATH, '//*[@id="cont_text"]/div[8]').text
    img_path = driver.find_element(By.XPATH,'//*[@id="cont_text"]/div[4]/ul/li[6]/img').get_attribute('src')
    print(x)
    data = ['더 코드케이'+room, call,img_path]
    wr.writerow(data)
    print(data)
    
    driver.execute_script("window.scrollTo(0, 200);")
f.close()    

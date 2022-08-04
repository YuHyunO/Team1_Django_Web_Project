import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import csv

f = open('C://Users//kosmo//Desktop//team1_Django_Wed_Project//nextedition_room.csv', 'w',encoding='cp949', newline='')
wr = csv.writer(f)
wr.writerow(['지점명', '주소', '테마수','전화번호'])

path = "C://Users//kosmo//Desktop//team1_Django_Wed_Project//chromedriver.exe"
driver = webdriver.Chrome(path)
url = "https://www.nextedition.co.kr/shops"
driver.get(url)

driver.maximize_window()
time.sleep(1)

for x in range(1,14):
    room = driver.find_element(By.XPATH,'/html/body/div[3]/div/div['+str(x)+']/div/div/h3/a').text
    loc = driver.find_element(By.XPATH,'/html/body/div[3]/div/div['+str(x)+']/div/div/span').text
    theme_num = driver.find_element(By.XPATH,' /html/body/div[3]/div/div['+str(x)+']/div/div/ul/li[1]').text
    call = driver.find_element(By.XPATH,'/html/body/div[3]/div/div['+str(x)+']/div/div/ul/li[2]').text
    print(x)
    data = ['넥스트에디션 '+ room, loc , theme_num , call]
    wr.writerow(data)
    print(data)
    
    driver.execute_script("window.scrollTo(0, 200);")
f.close() 
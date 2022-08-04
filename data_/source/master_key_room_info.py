import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import csv

f = open('master_key.csv', 'w',encoding='cp949', newline='')
wr = csv.writer(f)
wr.writerow(['지점명', '주소', '전화번호'])

path = "C://Users//kosmo//Desktop//team1_Django_Wed_Project//chromedriver.exe"
driver = webdriver.Chrome(path)
url = "http://www.master-key.co.kr/home/office"
driver.get(url)

driver.maximize_window()
time.sleep(1)
# driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
room = driver.find_element(By.XPATH,'//*[@id="first"]/div/div[2]/p[2]').text
loc = driver.find_element(By.XPATH,'//*[@id="first"]/div/div[2]/p[1]').text
call = driver.find_element(By.XPATH,'//*[@id="first"]/div/div[2]/p[3]/a').text

data_e =['마스터키 '+ room , loc , call]
print(data_e)

for x in range(3,25):
    room = driver.find_element(By.XPATH,'/html/body/div[2]/div[3]/div['+str(x)+']/div[2]/p[1]').text
    loc = driver.find_element(By.XPATH,'/html/body/div[2]/div[3]/div['+str(x)+']/div[2]/p[2]').text
    call = driver.find_element(By.XPATH,'/html/body/div[2]/div[3]/div['+str(x)+']/div[2]/p[3]/a').text
    
    print(x)
    data = ['마스터키 '+room, loc, call]
    wr.writerow(data)
    print(data)
    
    driver.execute_script("window.scrollTo(0, 200);")
f.close() 
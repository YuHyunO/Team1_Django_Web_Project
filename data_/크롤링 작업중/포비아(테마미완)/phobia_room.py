import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import csv

f = open('C://Users//kosmo//Desktop//team1_Django_Wed_Project//PHOBIA_room.csv', 'w',encoding='cp949', newline='')
wr = csv.writer(f)
wr.writerow(['지점명', '주소','전화번호','카페이미지url'])

path = "C://Users//kosmo//Desktop//team1_Django_Wed_Project//chromedriver.exe"
driver = webdriver.Chrome(path)
url = "https://www.xphobia.net/directions/directions.php?sido1=%EC%8B%9C%2F%EB%8F%84+%EC%84%A0%ED%83%9D&match=&x=41&y=14#sear_cj"
driver.get(url)

driver.maximize_window()
time.sleep(1)
# driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
room = driver.find_element(By.XPATH,'//*[@id="sear_cj"]/div[2]/div/div[2]/table/tbody[1]/tr/td[1]').text
loc = driver.find_element(By.XPATH,'//*[@id="sear_cj"]/div[2]/div/div[2]/table/tbody[1]/tr/td[2]').text
call = driver.find_element(By.XPATH,'//*[@id="sear_cj"]/div[2]/div/div[2]/table/tbody[1]/tr/td[3]').text
img_path = driver.find_element(By.XPATH,'//*[@id="sear_cj"]/div[2]/div/div[1]/div[1]/img').get_attribute('src')
data_e =['포비아 본점'+ room , loc , call,img_path]
print(data_e)

for x in range(1,11):
    room = driver.find_element(By.XPATH,' //*[@id="sear_cj"]/div[2]/div/div[2]/table/tbody[2]/tr['+str(x)+']/td[1]').text
    loc = driver.find_element(By.XPATH,'//*[@id="sear_cj"]/div[2]/div/div[2]/table/tbody[2]/tr['+str(x)+']/td[2]').text
    call = driver.find_element(By.XPATH,'//*[@id="sear_cj"]/div[2]/div/div[2]/table/tbody[2]/tr['+str(x)+']/td[3]').text
    img_path = driver.find_element(By.XPATH,'//*[@id="sear_cj"]/div[2]/div/div[1]/div[1]/img').get_attribute('src')
    print(x)
    data = ['포비아 '+ room, loc, call,img_path]
    wr.writerow(data)
    print(data)
    
    driver.execute_script("window.scrollTo(0, 200);")
f.close() 
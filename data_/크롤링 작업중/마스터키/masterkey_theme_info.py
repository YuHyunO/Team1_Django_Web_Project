import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import csv

 

options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome(options=options)

f = open('C://Users//kosmo//Desktop//team1_Django_Wed_Project//nextedition_theme.csv', 'w',encoding='cp949', newline='')
wr = csv.writer(f)
wr.writerow(['테마이름', '장르','추천인원수','소속지점', '이미지경로'])

path = "C://Users//kosmo//Desktop//team1_Django_Wed_Project//chromedriver.exe"
driver = webdriver.Chrome(path)
url = "https://www.nextedition.co.kr/themes"
driver.get(url)

driver.maximize_window()
time.sleep(1)
if:
    
        img_path = driver.find_element(By.XPATH, '//*[@id="list_div1"]/div[1]/div/div['+str(x)+']/a/div/img').get_attribute('src')
    for x in range(1, 21):
        theme = driver.find_element(By.ID, 'tdm_title').text
        genre = driver.find_element(By.ID, 'tdm_type').text
        num_Recommend = driver.find_element(By.ID,'tdm_people').text
        room = driver.find_element(By.ID, 'tdm_s2').text

time.sleep(1)
print(x)
data = [theme, genre, num_Recommend,'넥스트에디션 '+room, img_path]
print(data)
wr.writerow(data)
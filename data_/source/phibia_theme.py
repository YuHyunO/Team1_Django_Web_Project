import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import csv

from selenium.webdriver.common.keys import Keys


f = open('C://Users//kosmo//Desktop//team1_Django_Wed_Project//phobia_theme.csv','w',  newline='')
wr = csv.writer(f)
wr.writerow(['테마이름', '테마소개', '장르', '소속지점', '이미지경로','추천인원'])

path = "C:\\Users\\kosmo\\Desktop\\team1_Django_Wed_Project\\chromedriver.exe"
driver = webdriver.Chrome(path)
url = "https://www.xphobia.net/quest/quest_list.php"
driver.get(url)

datas = []

time.sleep(1)

for x in range(1, 52):
    link = driver.find_element(By.XPATH, '//*[@id="questWrapper"]/div[2]/div/div[3]/div/div['+str(x)+']/div[1]/a').get_attribute('href')
    theme = driver.find_element(By.XPATH,'//*[@id="questWrapper"]/div[2]/div/div[3]/div/div['+str(x)+']/div[2]/h5/a').text
    print(x)
    datas.append(link)
    # wr.writerow(data)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
print(datas)
    
driver.close()

for x in datas:
    
    path = "C:\\Users\\kosmo\\Desktop\\team1_Django_Wed_Project\\chromedriver.exe"
    driver = webdriver.Chrome(path) 
    driver.get(x)
   
    theme = driver.find_element(By.XPATH, '//*[@id="questDetail"]/div[2]/div[2]/div/div[1]/div[1]/div[1]/h5').text
    info = driver.find_element(By.XPATH, '//*[@id="questDetail"]/div[2]/div[2]/div/div[1]/div[3]').text
    # genre = driver.find_element(By.XPATH, '//*[@id="questDetail"]/div[2]/div[2]/div/div[1]/div[1]/div[2]/dl[1]').text
    # room = driver.find_element(By.XPATH, '//*[@id="questDetail"]/div[2]/div[2]/div/div[1]/div[1]/div[2]/dl[3]/dd/span').text
    # total = driver.find_element_by_class_name('tit_wrap')
    # total = driver.find_elements(By.CLASS_NAME, "tit_wrap").text
    total = driver.find_elements(By.TAG_NAME,'dd')
    # total = driver.find_elements(By.TAG_NAME,'a').text
    img_path = driver.find_element(By.XPATH, '//*[@id="questDetail"]/div[2]/div[2]/div/div[1]/div[2]/img').get_attribute('src')
    # num_recomend = driver.find_element(By.XPATH,'//*[@id="questDetail"]/div[2]/div[2]/div/div[1]/div[1]/div[2]/dl[2]/dd').text
    print(x) 
    print(total)
    # data = [theme, info, total, img_path]
    # print(data)
    # wr.writerow(data)
    driver.close()
    
f.close()    

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import csv

f = open('C://Users//kosmo//Desktop//team1_Django_Wed_Project//sherlock-holmes_room.csv', 'w',encoding='cp949', newline='')
wr = csv.writer(f)
wr.writerow(['카페이미지url','지점명', '주소','전화번호'])

path = "C://Users//kosmo//Desktop//team1_Django_Wed_Project//chromedriver.exe"
driver = webdriver.Chrome(path)
url = "http://sherlock-holmes.co.kr/branch/"
driver.get(url)

driver.maximize_window()
time.sleep(1)
for x in range(1,27):
    img_path = driver.find_element(By.XPATH,'//*[@id="branch"]/section[2]/div/div[2]/div['+str(x)+']/div[1]/img').get_attribute('src')
    driver.find_element(By.XPATH,'//*[@id="branch"]/section[2]/div/div[2]/div['+str(x)+']/div[3]/a[1]').click()
    room = driver.find_element(By.XPATH, '//*[@id="branch"]/section[2]/div/h2').text
    loc = driver.find_element(By.XPATH, '//*[@id="branch"]/section[2]/div/div[1]/div[1]/ul/li[1]').text
    call = driver.find_element(By.XPATH, '//*[@id="branch"]/section[2]/div/div[1]/div[1]/ul/li[2]').text
    
    print(x)
    data = [img_path,'셜록홈즈 '+room, loc, call]
    wr.writerow(data)
    print(data)
    #목록 버튼
    while True:
        try:
            driver.find_element(By.XPATH,'//*[@id="branch"]/section[2]/div/div[3]/a[2]').click()
            break
        except:
            time.sleep(0.1)
    
    driver.execute_script("window.scrollTo(0, 200);")
#f.close()    

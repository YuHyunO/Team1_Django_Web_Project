import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import csv
#클릭버튼 에러
from selenium.webdriver.common.keys import Keys
# driver.find_element_by_xpath('//*[@id="publish"]').send_keys(Keys.ENTER)

# f = open('C://Users//kosmo//Desktop//team1_Django_Wed_Project//codek_theme.csv', 'w', newline='')
# wr = csv.writer(f)
# wr.writerow(['소속지점','이미지경로','테마이름', '테마소개', '장르'])

path = "C:\\Users\\kosmo\\Desktop\\team1_Django_Wed_Project\\chromedriver.exe"
driver = webdriver.Chrome(path)
url = "http://www.code-k.co.kr/sub/code_sub03.html?R_JIJEM=S1"
driver.get(url)

# driver.maximize_window()
time.sleep(1)

for x in range(1, 15):
    room = driver.find_element(By.XPATH, '//*[@id="cont_text"]/ul[1]/a[1]/li').text
    img_path = driver.find_element(By.XPATH, '//*[@id="cont_text"]/div[4]/ul/li['+str(x)+']/a/img').get_attribute('src')
    theme = driver.find_element(By.XPATH, '//*[@id="cont_text"]/div[4]/ul/li['+str(x)+']/table/tbody/tr[1]/th').text
    detail = driver.find_element(By.XPATH,'//*[@id="btns1"]/a').send_keys(Keys.ENTER)
    print(detail)
    # num_recomend,genre,level = driver.find_element(By.XPATH,'//*[@id="tab1"]/div[2]/div[1]/ul/li[2]').text
    # num_recomend = driver.find_element(By.ID, 'tab'+str(x)+'').text
    # num_recomend = driver.find_element(By.XPATH, '//*[@id="tab'+str(x)+'"]/div[2]/div[1]/ul/li[2]/b[1]').text
    # genre = driver.find_element(By.XPATH,'//*[@id="tab1"]/div[2]/div[1]/ul/li[2]/text()[2]').text
    genre = driver.find_element(By.CSS_SELECTOR, '#tab1 > div.in_list_wrap > div.in_list_new > ul > li:nth-child(2)').text
    info = driver.find_element(By.XPATH,'//*[@id="tab'+str(x)+'"]/div[2]/div[3]/div[2]').text
    print(info)
    back = driver.find_element(By.XPATH,' //*[@id="btns1"]/a').send_keys(Keys.ENTER)
    time.sleep(1)
    # print(x)
    data = ['코드케이 '+room,img_path,theme, genre,info]
    print(data)
    # print(theme)
       
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    
# f.close()    

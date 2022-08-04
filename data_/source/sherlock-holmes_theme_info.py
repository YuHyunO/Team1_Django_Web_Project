import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import csv

f = open('C://Users//kosmo//Desktop//team1_Django_Wed_Project//sherlock-holmes_theme.csv', 'w', newline='')
wr = csv.writer(f)
wr.writerow(['테마이름', '테마소개', '장르', '소속지점', '이미지경로'])

# df = pd.DataFrame()
# df.to_csv('C:\\Users\\kosmo\Desktop\\team1_Django_Wed_Project\\자료실\\output\\EscapeRoom_theme.csv')

path = "C:\\Users\\kosmo\\Desktop\\team1_Django_Wed_Project\\chromedriver.exe"
driver = webdriver.Chrome(path)
url = "http://sherlock-holmes.co.kr/theme/"
driver.get(url)

driver.maximize_window()
time.sleep(1)

page_no = 1
while True:
    print('page: '+str(page_no))
    page_no += 1
    for x in range(1, 13):
        driver.find_element(By.XPATH, '//*[@id="theme_list"]/div/div[2]/div['+str(x)+']/div/img').click()
        time.sleep(0.5)
        theme = driver.find_element(By.XPATH, '//*[@id="theme_list"]/div/div[2]/div['+str(x)+']/div/div/div/div[1]').text
        info = driver.find_element(By.XPATH, '//*[@id="theme_list"]/div/div[2]/div['+str(x)+']/div/div/div/div[2]').text
        genre = driver.find_element(By.XPATH, '//*[@id="theme_list"]/div/div[2]/div['+str(x)+']/div/div/div/div[3]/table/tbody/tr[1]/td[1]').text
        room = driver.find_element(By.XPATH, '//*[@id="theme_list"]/div/div[2]/div['+str(x)+']/div/div/div/div[3]/table/tbody/tr[2]/td[2]').text
        img_path = driver.find_element(By.XPATH, '//*[@id="theme_list"]/div/div[2]/div['+str(x)+']/div/img').get_attribute('src')
        time.sleep(1)
        print(x)
        data = [theme, info, genre, '셜록홈즈 '+room, img_path]
        print(data)
        # print(theme)
        try:
            wr.writerow(data)
        except UnicodeEncodeError:
            print('EncodeErrorData : '+str(data))
            continue
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(1)
    driver.find_element(By.XPATH, '//*[@id="footer"]/section[1]/div/button').click()
    time.sleep(1)
    driver.find_element(By.XPATH, '//*[@id="theme_list"]/div/div[1]/ul/li[13]/a').click()
    
# f.close()    

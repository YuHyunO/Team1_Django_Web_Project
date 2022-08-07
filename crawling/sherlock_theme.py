import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import csv

# f = open('C://Users//kosmo//Desktop//team1_Django_Wed_Project//sherlock-holmes_room.csv', 'w',encoding='cp949', newline='')
# wr = csv.writer(f)
# wr.writerow(['카페이미지url','지점명', '주소','전화번호'])

path = "C:/ChromeDriver/chromedriver.exe"
driver = webdriver.Chrome(path)
url = "http://sherlock-holmes.co.kr/reservation/"
driver.get(url)

# NoSuchElementException
# data = []

driver.maximize_window()
time.sleep(1)
print(1)
for x in range(2,9):
    driver.find_element(By.XPATH, '//*[@id="selectArea"]/option['+str(x)+']').click() # 지역 선택
    time.sleep(1)
    print(2)
    for y in range(2, 20):
        try:
            driver.find_element(By.XPATH, '//*[@id="selectBranch"]/option['+str(y)+']').click() # 지점 선택
            time.sleep(1)
            print(3)
            for z in range(1, 20):
                try:
                    global people
                    people = driver.find_element(By.XPATH, '/html/body/div[1]/section[3]/div[2]/ul/li['+str(z)+']/div[1]/div[3]') # 인원  
                    print(4)
                    time.sleep(1)
                    driver.find_element(By.XPATH, '/html/body/div[1]/section[3]/div[2]/ul/li['+str(z)+']/h2/a').click() #자세히보기
                    print(5)
                    time.sleep(1)
                    driver.find_element(By.XPATH, '//*[@id="pop_info"]/div/div/img').click() #이미지 클릭
                    print(6)
                    time.sleep(1)
                    global img_path
                    img_path = driver.find_element(By.XPATH, '//*[@id="pop_info"]/div/div/img').get_attribute('src') #이미지 주소                    
                    print(7)
                    time.sleep(1)
                    global theme
                    global info
                    global genre
                    theme = driver.find_element(By.XPATH, '//*[@id="pop_info"]/div/div/div/div/div[1]').text # 테마이름
                    print(8)
                    info = driver.find_element(By.XPATH, '//*[@id="pop_info"]/div/div/div/div/div[2]').text # 테마소개
                    print(9)
                    genre = driver.find_element(By.XPATH, '//*[@id="pop_info"]/div/div/div/div/div[3]/table/tbody/tr[1]/td[1]').text # 장르
                    print(10)
                    time.sleep(1)                    
                    try:
                        global difficulty
                        difficulty = 0
                        time.sleep(1)
                        try:
                            for i in range(1,6):
                                driver.find_element(By.XPATH, '//*[@id="pop_info"]/div/div/div/div/div[3]/table/tbody/tr[1]/td[2]/div/i['+str(i)+']')
                                difficulty = i
                                print(11)
                        except Exception:
                            print('exc1-1',str(Exception))
                            break
                        time.sleep(1)
                    except Exception:
                        print('exc1-2',str(Exception))
                        break
                    
                    try:
                        global horror
                        horror = 0
                        time.sleep(1)
                        try:
                            for i in range(1,6):                    
                                driver.find_element(By.XPATH, '//*[@id="pop_info"]/div/div/div/div/div[3]/table/tbody/tr[2]/td[1]/div/i['+str(i)+']')                                
                                horror = i
                                print(12)
                        except Exception:
                            print('exc1-3',str(Exception))
                            break
                        time.sleep(1)                                              
                    except Exception:
                        print('exc1-4',str(Exception))
                        break

                    global room
                    room = driver.find_element(By.XPATH, '//*[@id="pop_info"]/div/div/div/div/div[3]/table/tbody/tr[2]/td[2]').text
                    print(13)
                    time.sleep(1)
                    driver.find_element(By.XPATH, '//*[@id="pop_info"]/div/div/div/a').click()
                    print(14)
                    time.sleep(1)
                except Exception:
                    print('exc1',str(Exception))
                    break
                data = [theme, room, img_path, genre, people, info, difficulty, horror]
                print(data)
        except Exception:
            print('exc2',str(Exception))
            break
print('done')

    # driver.execute_script("window.scrollTo(0, 200);")
#f.close()    

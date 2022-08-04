from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd

path = "C:/ChromeDriver/chromedriver.exe"
driver = webdriver.Chrome(path)
url = 'http://sherlock-holmes.co.kr/theme/'
driver.get(url)

for x in range(1,27):
    driver.maximize_window()
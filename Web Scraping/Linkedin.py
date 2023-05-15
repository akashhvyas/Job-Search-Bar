import pandas as pd
import numpy as np
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

df = pd.read_excel("A:\Masai Projects\ML Project Job ANAlytics/Remaning company.xlsx")

company = []

for i in df['Company']:
    company.append(i)

service = Service('C:/Users/Mi/Downloads/chromedriver_win32/chromedriver.exe')
driver = webdriver.Chrome(executable_path=r'C:/Users/Mi/Downloads/chromedriver_win32/chromedriver.exe')

link = "https://www.linkedin.com/"

driver.get(link)

time.sleep(5)

username = driver.find_element(By.XPATH,'//*[@id="session_key"]')
username.send_keys(str("harsh.agrawal9010@gmail.com"))

time.sleep(5)

password = driver.find_element(By.XPATH,'//*[@id="session_password"]')
password.send_keys(str("Harsh@9174"))
time.sleep(5)

signin = driver.find_element(By.XPATH,'//*[@id="main-content"]/section[1]/div/div/form/div[2]/button').click()

time.sleep(60)

search_box = driver.find_element(By.XPATH,'//*[@id="global-nav-typeahead"]/input')

data = []
try:

    for comp in company:
        search_box.clear()
        search_box.send_keys(str(comp))
        search_box.send_keys(Keys.ENTER)
        time.sleep(8)
        try:

            followers = driver.find_element(By.CLASS_NAME, 'reusable-search-simple-insight__text-container').text

            data.append([comp,followers])

            print(f"{comp}: {followers}")

        except:
            print("NA")
except:
    print("NA")

df = pd.DataFrame(data,columns=['company','followers'])

df.to_csv("A:/Masai Projects/Job Analytics project/Followers.csv",index = False)
print(df)



# for com in company:
#     link = f'https://www.google.com/search?q={com}+linkedin+followers&sxsrf=APwXEddFR4lS97vVKHTqlsT0-D6yrqKnCg%3A1682604846556&ei=LoNKZI_MId2fseMPvruYsAY&ved=0ahUKEwiPm7TBn8r-AhXdT2wGHb4dBmYQ4dUDCA8&uact=5&oq=Google+linkedin+followers&gs_lcp=Cgxnd3Mtd2l6LXNlcnAQAzIICAAQCBAHEB4yCAgAEAgQBxAeMggIABAIEAcQHjIICAAQCBAHEB4yCAgAEAgQBxAeMggIABCKBRCGAzIICAAQigUQhgM6CggAEEcQ1gQQsAM6BggAEAcQHjoHCAAQDRCABDoICAAQBRAHEB5KBAhBGABQ5gdYzxBg_hFoAnABeACAAZ0CiAH_CZIBAzItNZgBAKABAcgBCMABAQ&sclient=gws-wiz-serp'

#     driver.get(link)
#     time.sleep(2)
#     fol = driver.find_element(By.XPATH,'//*[@id="rso"]/div[1]/div/div/div[2]/div/span').text
#     print(fol)
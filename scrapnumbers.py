from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get("https://web.whatsapp.com/")
time.sleep(10)

group_name = "group name"

try:
    input_box = driver.find_element(
        By.XPATH, "(//p[@class='selectable-text copyable-text iq0m558w'])[1]"
    )
except:
    time.sleep(10)
    input_box = driver.find_element(
        By.XPATH, "(//p[@class='selectable-text copyable-text iq0m558w'])[1]"
    )
input_box.send_keys(group_name)
time.sleep(10)
# group = driver.find_element(By.XPATH, f"(//span[@title='{group_name}'])[1]")
group = driver.find_element(By.XPATH, "(//span[@class='matched-text _11JPr'])[1]")

group.click()
time.sleep(10)
number_element = driver.find_element(
    By.XPATH,
    "(//div[@class='p357zi0d r15c9g6i g4oj0cdv ovllcyds l0vqccxk pm5hny62'])[1]",
).text
members_number = str(number_element)
seaprate_numbers = members_number.split(",")
members_number_df = pd.DataFrame({"numbers": seaprate_numbers})
members_number_df = members_number_df[members_number_df["numbers"] != " You"]
members_number_df.to_csv(f"{group_name}.csv", index=False)

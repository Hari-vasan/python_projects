from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import json
import mysql.connector
import re

mydb = mysql.connector.connect(
    host="localhost", user="root", password="admin", database="whatsup_mebers"
)


from subprocess import call


var = call(["node", "example.js"])

with open("data.json", "r", encoding="utf-8") as group_name:
    group_name = json.load(group_name)

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get("https://web.whatsapp.com/")
time.sleep(10)

# group_name = "DMK4Alangudi"
count = 0
for i in group_name["group_names"]:
    count = count + 1
    i = re.sub(r"[^\w\s]", "", i)
    try:
        input_box = driver.find_element(
            By.XPATH, "(//p[@class='selectable-text copyable-text iq0m558w'])[1]"
        )
    except:
        time.sleep(10)
        input_box = driver.find_element(
            By.XPATH, "(//p[@class='selectable-text copyable-text iq0m558w'])[1]"
        )

    time.sleep(10)
    if count < 1:
        print(i, count)
        input_box.send_keys(i)
    else:
        print(i, count)
        input_box = driver.find_element(
            By.XPATH, "//div[@id='side']/div/div/div/div[2]/div/div/p"
        )
        input_box.send_keys(i)
    time.sleep(10)
    # group = driver.find_element(By.XPATH, f"(//span[@title='{i}'])[1]")
    group = driver.find_element(By.XPATH, "(//span[@class='matched-text _11JPr'])[1]")

    group.click()
    time.sleep(10)
    number_element = driver.find_element(
        By.XPATH,
        "(//div[@class='p357zi0d r15c9g6i g4oj0cdv ovllcyds l0vqccxk pm5hny62'])[1]",
    ).text
    members_number = str(number_element)
    seaprate_numbers = members_number.split(",")
    # members_number_df = pd.DataFrame({"numbers": seaprate_numbers})
    # members_number_df = members_number_df[members_number_df["numbers"] != " You"]
    # members_number_df.to_csv(f"{i}.csv", index=False)
    mycursor = mydb.cursor()
    sql = "INSERT INTO members_data (group_name,phone_number) VALUES (%s, %s)"
    for mebers_db in seaprate_numbers:
        values = (i, mebers_db)
        mycursor.execute(sql, values)
        mydb.commit()  # Commit the changes to the database

    exit_button = driver.find_element(
        By.XPATH, "//div[@id='side']/div/div/div/button/div[2]/span"
    )
    exit_button.click()
    time.sleep(10)
mydb.close()

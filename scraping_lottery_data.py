from selenium import webdriver
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import csv

# Selenium setup
options = webdriver.FirefoxOptions()
options.headless = True
service = Service(GeckoDriverManager().install())
driver = webdriver.Firefox(service=service, options=options)

driver.get("https://basketball.realgm.com/nba/draft/lottery_results/")

# Waiting until dropdown is present
wait = WebDriverWait(driver, 10)
wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "select")))

# Gather dropdown data of all options
dropdown = driver.find_element(By.CSS_SELECTOR, "select")
select = Select(dropdown)
num_options = len(select.options)

lottery_data = []

for i in range(num_options):
    # Relocate dropdown and option after reloading each page
    dropdown = driver.find_element(By.CSS_SELECTOR, "select")
    select = Select(dropdown)
    option = select.options[i]

    # Gather draft and value of each page
    draft = option.text.strip()
    value = option.get_attribute("value").strip()

    if not value:
        print(f"No value found for {draft}")
        continue

    print(f"Processing data for {draft}")

    select.select_by_value(value)
    time.sleep(2)

    soup = BeautifulSoup(driver.page_source,"html.parser")
    table = soup.find('table', class_="table table-striped table-centered table-hover table-bordered table-compact table-nowrap")
    
    if not table: 
        print(f"No table found for {draft}")
        continue

    # Inserting data to add to CSV
    dataRows = soup.find_all('tr')
    for data in dataRows[1:]:
        cols = [col.text.strip() for col in data.find_all('td')]
        if cols:
            lottery_data.append([draft] + cols)

# Inserting data to CSV file and defining column names for data
header = ["Draft", "Pick", "Team", "Record", "Odds", "Chances", "Pre-Lottery Position", "Pick Change", "Player Taken", "Draft Team"]
with open("lottery_data.csv", "w", newline='', encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(header)
    writer.writerows(lottery_data)

driver.quit()
print("Process Complete")
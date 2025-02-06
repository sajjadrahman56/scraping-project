from selenium import webdriver
import time
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

chrome_options = Options()
chrome_options.add_argument("--disable-cache")
chrome_options.add_argument("--incognito")
driver = webdriver.Chrome(options=chrome_options)


driver.maximize_window()
driver.get('https://www.google.com/maps/')


search_box = driver.find_element(By.ID, 'searchboxinput')
search_box.send_keys('car shop sylhet')
driver.find_element(By.ID, 'searchbox-searchbutton').click()


wait = WebDriverWait(driver, 20)
wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div[role="feed"]')))


scroll_area = driver.find_element(By.CSS_SELECTOR, 'div[role="feed"]')

prev_height = driver.execute_script("return arguments[0].scrollHeight", scroll_area)

while True:
    driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight;", scroll_area)
    time.sleep(10) 

    new_height = driver.execute_script("return arguments[0].scrollHeight", scroll_area)
    if new_height == prev_height:
        break  
    prev_height = new_height


stores = driver.find_elements(By.XPATH, "//div[contains(@class, 'bfdHYd Ppzolf OFBs3e')]")

data = []

for store in stores:
        name_elements = store.find_elements(By.XPATH, ".//div[contains(@class, 'qBF1Pd fontHeadlineSmall')]")
        name = name_elements[0].text if name_elements else "NA"

        phone_elements = store.find_elements(By.XPATH, ".//div[4]/div[2]/span[2]/span[2]")
        phone = phone_elements[0].text.strip() if phone_elements else "N/A"

        data.append({
            "name": name,
            "phone": phone
        })

print(data)
driver.quit


 
df = pd.DataFrame(data)

# Save to CSV file
df.to_csv('./car_shops_sylhet.csv', index=False, encoding='utf-8')

print("CSV file has been saved successfully.")
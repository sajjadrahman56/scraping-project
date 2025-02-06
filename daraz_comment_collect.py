import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support import expected_conditions as EC

chrome_options = Options()
chrome_options.add_argument("--disable-cache")
chrome_options.add_argument("--incognito")

driver = webdriver.Chrome(options=chrome_options)
driver.maximize_window()

driver.get('https://www.daraz.com.bd/products/tp-link-deco-e4-ac1200-router-whole-home-mesh-wi-fi-system-1-pack-i156550140-s1086146208.html')

driver.refresh()
time.sleep(3)

height = driver.execute_script('return document.body.scrollHeight')

for i in range(0, height + 300, 30):
    driver.execute_script(f'window.scrollTo(0, {i});')
    time.sleep(0.5)

wait = WebDriverWait(driver, 10)

pagination_xpath = '//*[@id="module_product_review"]/div/div/div[3]'
pagination_container = wait.until(EC.presence_of_element_located((By.XPATH, pagination_xpath)))

def get_comment():
    data = []
    wait = WebDriverWait(driver, 10)
    for j in range(1, 6):  
        try:
            comment_xpath = f'#module_product_review > div > div > div:nth-child(3) > div.mod-reviews > div:nth-child({j}) > div.item-content > div.content'
            comment_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, comment_xpath)))
            comment = comment_element.text if comment_element.text.strip() != '' else ' '
            data.append(comment)
        except Exception as e:
            print(f"Error fetching comment {j}: {e}")
    return data

data_dict = {}   
page = 1

while True:
    try:     
        comments = get_comment()
        data_dict[page] = comments   
        next_button_xpath = '//*[@id="module_product_review"]/div/div/div[3]/div[2]/div/button[2]/i' 
        next_button = driver.find_element(By.XPATH, next_button_xpath)
        parent_button = next_button.find_element(By.XPATH, './..') 

        if parent_button.get_attribute('disabled') is not None:
            print("The next button is disabled. Reached the last page.")
            break  
        else:           
            print(f"Page {page}: Clicking next button...")
            driver.execute_script("arguments[0].click();", parent_button)  
            time.sleep(5) 
            print("Clicked next button.")
 
        page += 1  # Increment the page counter
        if(page==20):
            break
    except Exception as e:
        print(f"An error occurred: {e}")
        break

print(f'--------------------------------------number of total page = {page}---------------------------------------')
print(data_dict)
 

    # last_button_xpath = f'//*[@id="module_product_review"]/div/div/div[3]/div[2]/div/div/button[5]'
    # element = wait.until(EC.element_to_be_clickable((By.XPATH, last_button_xpath)))
    # data2 = get_comment()

time.sleep(5)
driver.quit()

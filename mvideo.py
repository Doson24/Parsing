import time
from pymongo import MongoClient
from selenium.webdriver.common.actions.interaction import KEY
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import ast

options = Options()
options.add_argument("--start-maximized")
options.add_argument('--disable-notifications')
# options.add_argument("--headless")  # Режим без интерфейса
driver = webdriver.Chrome('C:\\install\\chromedriver.exe', options= options)

driver.get('https://www.mvideo.ru')

element = WebDriverWait(driver, timeout= 5)
el = element.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.c-popup__content div span')))
driver.refresh()
driver.refresh()

action = ActionChains(driver)
action.move_to_element(driver.find_element_by_class_name('wide-banner')).perform()

while True:
    try:
        WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH, '//div[@class="facelift gallery-layout products--shelve gallery-layout_products '
                                      'gallery-layout_product-set grid-view"]/div/div[2]/div/div[1]/a[2]'))).click()
    except Exception:
        print('button disable')
        break
wrapper = driver.find_elements_by_class_name('caroufredsel_wrapper')[3]
li = wrapper.find_elements_by_class_name('gallery-list-item')
bestseller = []
for a in li:
    info = a.find_element_by_class_name('sel-product-tile-title')
    string = info.get_attribute('data-product-info')
    my_dict = ast.literal_eval(string)
    bestseller.append(my_dict)

client = MongoClient('localhost', 27017)
# Connect to our database
db = client['mvideo']
# Fetch our series collection
series_collection = db['Bestseller']
series_collection.insert_many(bestseller)

driver.close()
import time
from pymongo import MongoClient
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import pandas as pd
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


url = 'https://mail.ru'
# url = 'https://e.mail.ru/inbox/'
login = ''
password = ''


class Mail():

    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Режим без интерфейса
        # self.driver = webdriver.Chrome('C:\\install\\chromedriver.exe', options=chrome_options)
        self.driver = webdriver.Chrome('C:\\install\\chromedriver.exe')

        #списки
        self.thems = []
        self.text_letter = []
        self.authors = []
        self.date =[]
        # Create the client
        client = MongoClient('localhost', 27017)
        # Connect to our database
        db = client['mail']
        # Fetch our series collection
        self.series_collection = db['test1']

    def authorization(self, url, login, password):

        self.driver.get(url)
        self.driver.find_element_by_name('login').send_keys(login)
        self.driver.find_element_by_xpath('//form/button[@data-testid="enter-password"]').click()

        self.driver.implicitly_wait(1)
        self.driver.find_element_by_xpath('//*[@id="mailbox"]//input[@data-testid="password-input"]').send_keys(password)
        self.driver.find_element_by_xpath('//form/button[@data-testid="login-to-mail"]').click()

    def catalogue_letter(self):
        # self.driver.implicitly_wait(3)
        self.driver.get('https://e.mail.ru/inbox/')
        self.authors = [i.get_attribute('title') for i in self.driver.find_elements_by_css_selector('div[class$=item_correspondent] span')]

    def get_letter(self, page=3):
        self.driver.get('https://e.mail.ru/inbox/')
        self.driver.find_elements_by_css_selector('div[class$=item_correspondent] span')[0].click()
        self.driver.implicitly_wait(1)
        for i in range(page):
            #обработка исключения
            time.sleep(1)
            text = self.driver.find_element_by_css_selector('div[class=letter-body]').text.strip()
            self.text_letter.append(text)
            self.authors.append(self.driver.find_element_by_css_selector('.letter-contact').get_attribute('title'))
            self.thems.append(self.driver.find_element_by_css_selector('h2').text)
            self.date.append(self.driver.find_element_by_css_selector('.letter__date').text)

            self.driver.find_element_by_css_selector('span[data-title-shortcut="Ctrl+↓"]').click()


    def close_driver(self):
        self.driver.close()

    def import_database(self):
        data = []
        for i in range(len(self.thems)):
            data.append({'Тема' : self.thems[i],
                    'отправитель':self.authors[i],
                    "текст": self.text_letter[i],
                    "дата": self.date[i]
             })
        self.series_collection.insert_many(data)

# # непрочитанные писма
# driver.find_element_by_class_name('filters-control__filter-text').click()
# driver.find_element_by_xpath("//div[@class='list list_hover-support']/div[2]/span[2]").click()
# driver.implicitly_wait(3)
# driver.get('https://e.mail.ru/inbox/?filter_unread=1')

a = Mail()
a.authorization(url,login,password)
a.get_letter(50)
a.import_database()
a.close_driver()

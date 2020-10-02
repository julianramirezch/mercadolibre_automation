#!/usr/bin/python3

from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import unittest
import time
import pandas as pd


class SearchTesting(unittest.TestCase):
    def setUp(self):
        time.sleep(5)
        self.driver = webdriver.Chrome(executable_path='./chromedriver.exe')
        driver = self.driver
        driver.get('https://www.mercadolibre.com/')
        driver.maximize_window()
        driver.implicitly_wait(30)

    def test_search_xbox(self):
        driver = self.driver

        country = driver.find_element_by_id('CO')
        country.click()

        search_field = driver.find_element_by_name('as_word')
        search_field.clear()
        search_field.send_keys('xbox')
        search_field.submit()
        time.sleep(3)

        try:
            ok = driver.find_element_by_id('cookieDisclaimerButton')
            ok.click()
        except Exception:
            print('No disclaimer button')

        ubication = driver.find_element_by_partial_link_text('Bogotá D.C.')
        ubication.click()

        condition = driver.find_element_by_partial_link_text('Nuevo')
        condition.click()

        list = driver.find_element_by_xpath('//button[@class="andes-dropdown__trigger"]')
        list.click()

        #higuer_price = driver.find_element_by_partial_link_text('Más relevantes')
        #higuer_price.click()

        titles = driver.find_elements_by_xpath('//h2[@class="ui-search-item__title"]')
        prices_list = driver.find_elements_by_xpath('//div[@class="ui-search-price__second-line"]//span[@class="price-tag-fraction"]')
        print(len(prices_list))
        articles = []
        prices = []
        final = []

        for title in titles:
            print(title.text)
            articles.append(title.text)

        for i in range(0, len(prices_list), 2):
            print(prices_list[i].text)
            prices.append(prices_list[i].text)

        for article, price in zip(articles, prices):
            data = {
                'articulo': article,
                'precio': price,
            }
            final.append(data)

        print(final)
        df = pd.DataFrame(final)
        df.to_csv('productos.csv')

    def tearDown(self):
        self.driver.close()


if __name__ == "__main__":
    unittest.main(verbosity=2)

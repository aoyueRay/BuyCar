# -*- coding:utf-8 -*-

from selenium import webdriver
import time

class BuyCar(object):

    database_name = 'MyCar'

    def open_url(self):

        driver = webdriver.Firefox()
        driver.get('http://car.autohome.com.cn/price/list-8_18-101-0-2-101-0-0-0-0-0-0-0-0-0-0-1.html')
        driver.implicitly_wait(10)

        # temp = driver.find_elements_by_xpath('//div[@class="list-cont"]/div/div[2]/div')
        temp = driver.find_elements_by_xpath('//div[@class="list-cont"]')
        for each in temp:
            # a = each.find_element_by_xpath('a').text
            a = each.get_attribute('data-value')
            print a
            print type(a)

        driver.close()

        return None


if __name__ == '__main__':
    bc = BuyCar()
    bc.open_url()
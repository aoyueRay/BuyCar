# -*- coding:utf-8 -*-

from selenium import webdriver
import time

class BuyCar(object):

    database_name = 'MyCar'
    setting_list = []

    def open_url(self):

        # driver = webdriver.Firefox()
        driver = webdriver.PhantomJS()
        driver.get('http://car.autohome.com.cn/price/list-8_18-101-0-2-101-0-0-0-0-0-0-0-0-0-0-1.html')
        driver.implicitly_wait(10)

        next_page_available = 1
        while next_page_available:

            # Setting Page URL
            eligible_models = driver.find_elements_by_xpath('//div[@class="intervalcont fn-hide"]/div[@class="interval01"]/ul/li')
            eligible_len = len(eligible_models)
            print eligible_len
            for each_index in xrange(eligible_len):
                setting_url = eligible_models[each_index].find_element_by_xpath('div[last()]/div[1]/a[4]').get_attribute('href')
                self.setting_list.append(setting_url)

            next_page_xpath = '//div[@class="page"]/a[last()]'
            next_page_available = 1 if len(driver.find_element_by_xpath(next_page_xpath).get_attribute('href')) > 20 else 0
            if next_page_available:
                driver.find_element_by_xpath(next_page_xpath).click()

        driver.close()
        return None

    def detail_infos(self):

        driver = webdriver.Firefox()
        url = 'http://car.autohome.com.cn/config/spec/31052.html#pvareaid=2042112'
        driver.get(url)
        driver.implicitly_wait(10)

        car_name = driver.title
        car_name = car_name.split('_')[0][4:]
        print car_name

        head_xpath = '//div[@id="config_data"]'
        car_company = driver.find_element_by_xpath(head_xpath + '/table[2]/tbody/tr[2]/td').text
        car_level = driver.find_element_by_xpath(head_xpath + '/table[2]/tbody/tr[3]/td').text
        car_market_time = driver.find_element_by_xpath(head_xpath + '/table[2]/tbody/tr[4]/td').text
        car_gearbox = driver.find_element_by_xpath(head_xpath + '/table[2]/tbody/tr[6]/td').text
        car_lwh = driver.find_element_by_xpath(head_xpath + '/table[2]/tbody/tr[7]/td').text
        car_body_structure = driver.find_element_by_xpath(head_xpath + '/table[2]/tbody/tr[8]/td').text


        print car_company
        print car_level
        print car_market_time
        print car_gearbox
        print car_lwh
        print car_body_structure

        driver.close()

        return None





if __name__ == '__main__':
    bc = BuyCar()
    # bc.open_url()
    # print len(bc.setting_list)
    bc.detail_infos()


# -*- coding:utf-8 -*-

from selenium import webdriver
import MySQLdb
import time


class BuyCar(object):

    def __init__(self):
        self.conn = MySQLdb.connect(
            host='localhost',
            user='root',
            passwd='433280',
            db='MyCar',
            charset='utf8',
            use_unicode=True,
        )
        self.cursor = self.conn.cursor()

        self.url_list = []
        self.car = {}

    def get_urls(self):
        """
        Open URL and get the setting urls.
        Append the url in global variable url_list,
        :return:None
        """
        driver = webdriver.Firefox()
        # driver = webdriver.PhantomJS()
        driver.implicitly_wait(100)
        # Compact
        # driver.get('http://car.autohome.com.cn/price/list-8_18-101-0-2-101-0-0-0-0-0-0-0-0-0-0-1.html')
        # 10 - 20W 自动档
        driver.get('https://car.autohome.com.cn/price/list-10_20-0-0-0-101-0-0-0-0-0-0-0-0-0-0-1.html')

        # SUV
        # driver.get('http://car.autohome.com.cn/price/list-8_18-9-0-0-101-0-0-0-0-0-0-0-0-0-0-1.html')

        print 'Start getting URL lists...'

        next_page_available = 1
        while next_page_available:

            # Setting Page URL
            driver.implicitly_wait(100)
            eligible_models = driver.find_elements_by_xpath('//div[@class="intervalcont fn-hide"]/div[@class="interval01"]/ul/li')
            eligible_len = len(eligible_models)
            print eligible_len
            for each_index in xrange(eligible_len):
                setting_url = eligible_models[each_index].find_element_by_xpath('div[1]/div[1]/p[1]/a').get_attribute('href')
                self.url_list.append(setting_url)

            driver.implicitly_wait(100)
            next_page_xpath = '//div[@class="page"]/a[last()]'
            driver.implicitly_wait(100)
            next_page_available = 1 if len(driver.find_element_by_xpath(next_page_xpath).get_attribute('href')) > 20 else 0
            if next_page_available:
                driver.implicitly_wait(100)
                driver.find_element_by_xpath(next_page_xpath).click()
        driver.close()

        # Write the urls into file.
        print 'There are %d records!' % len(self.url_list)
        with open('URLs.txt','a') as f:
            for each_url in self.url_list:
                f.write(each_url)
                f.write('\n')
        return None

    def crwal_urls(self):
        """
        Read the url_list in turn and crawl detail infos.
        :return:
        """
        print 'Start getting detail car models...'
        # driver = webdriver.PhantomJS()
        driver = webdriver.Firefox()
        # self.url_list = ['http://car.autohome.com.cn/config/spec/31052.html#pvareaid=2042112']
        with open('URLs.txt', 'r') as f:
            urls = f.readlines()
        print 'There are %d records!' % len(urls)
        for each_index in xrange(len(urls)):
            each_url = urls[each_index][:-1]
            print '---' * 33
            print '%d:%s' %(each_index + 1, each_url)

            driver.get(each_url)

            self.detail_url(driver)    # Open detail URL.

            # self.detail_infos(driver)    # Get detail infos.

        driver.close()
        print 'Done!'
        return None

    def detail_url(self, driver):
        """
        Open detail URL.
        :return: None
        """
        # Get dealer page url.
        time.sleep(1)
        sub_url = driver.find_element_by_xpath('//div[@class="uibox"]/iframe').get_attribute('src')
        driver.get(sub_url)

        try:
            # Get deatil url.
            driver.implicitly_wait(10)
            # detail_url = driver.find_element_by_xpath('//div[@class="tab-content"]/div/ul/li[1]/dl[1]/dd[1]/span[1]/a').get_attribute('href')
            detail_url = driver.find_element_by_xpath('//div[@id="dealer-box"]/div/ul/li[1]/dl[1]/dd[1]/span[1]/a').get_attribute('href')
            with open('Final.txt', 'a') as f:
                f.write(detail_url)
                f.write('\n')
            # driver.get(detail_url)
        except Exception,e:
            print 'Dealer not existed error!'
            print e

        return None

    def crawl_infos(self):
        """
        Get detail infos by detail url.
        :return:None
        """
        with open('Final.txt','r') as f:
            urls = f.readlines()
        print 'Start getting detail infos...'
        print 'There are %d records!' % len(urls)
        # driver = webdriver.Firefox()
        driver = webdriver.PhantomJS()
        for each_index in xrange(len(urls)):
            each_url = urls[each_index][:-1]
            print '---' * 33
            print '%d:%s' %(each_index + 1, each_url)

            driver.implicitly_wait(100)
            driver.get(each_url)

            self.detail_infos(driver)    # Get detail infos.
            driver.implicitly_wait(100)
            # break

        driver.close()
        print 'Done'
        return None

    def detail_infos(self, driver):
        """
        Get detail infos.
        :param driver:
        :return: None
        """
        self.car = {}

        self.car['name'] = driver.find_element_by_xpath('//div[@class="infocont-main"]/h3/p').text
        print self.car['name']

        try:
            head_xpath = '//div[@class="tabcont-cont"]'
            driver.implicitly_wait(100)
            self.car['company'] = driver.find_element_by_xpath(head_xpath + '/div[1]/div[2]/table/tbody/tr[1]/td[1]').text
            time.sleep(1)
            self.car['level'] = driver.find_element_by_xpath(head_xpath + '/div[1]/div[2]/table/tbody/tr[1]/td[2]').text
            driver.implicitly_wait(100)
            self.car['market_time'] = driver.find_element_by_xpath(head_xpath + '/div[1]/div[2]/table/tbody/tr[2]/td[1]').text
            driver.implicitly_wait(100)
            self.car['engine'] = driver.find_element_by_xpath(head_xpath + '/div[1]/div[2]/table/tbody/tr[2]/td[2]').text
            driver.implicitly_wait(100)
            self.car['gearbox'] = driver.find_element_by_xpath(head_xpath + '/div[1]/div[2]/table/tbody/tr[3]/td[1]').text
            driver.implicitly_wait(100)
            self.car['lwh'] = driver.find_element_by_xpath(head_xpath + '/div[1]/div[2]/table/tbody/tr[3]/td[2]').text
            driver.implicitly_wait(100)
            self.car['body_structure'] = driver.find_element_by_xpath(head_xpath + '/div[1]/div[2]/table/tbody/tr[4]/td[1]').text
            driver.implicitly_wait(100)
            self.car['maximum_speed'] = driver.find_element_by_xpath(head_xpath + '/div[1]/div[2]/table/tbody/tr[4]/td[2]').text
            driver.implicitly_wait(100)
            self.car['fuel_consumption'] = driver.find_element_by_xpath(head_xpath + '/div[1]/div[2]/table/tbody/tr[7]/td[1]').text
            driver.implicitly_wait(100)
            self.car['engine_capacity'] = driver.find_element_by_xpath(head_xpath + '/div[1]/div[6]/table/tbody/tr[1]/td[1]').text
            driver.implicitly_wait(100)
            self.car['engine_form'] = driver.find_element_by_xpath(head_xpath + '/div[1]/div[6]/table/tbody/tr[1]/td[2]').text
            driver.implicitly_wait(100)
            self.car['gearbox_type'] = driver.find_element_by_xpath(head_xpath + '/div[1]/div[8]/table/tbody/tr[1]/td[1]').text
            driver.implicitly_wait(100)
            self.car['parking_brake_type'] = driver.find_element_by_xpath(head_xpath + '/div[1]/div[12]/table/tbody/tr[1]/td[1]').text

            driver.implicitly_wait(100)
            driver.find_element_by_xpath('//div[@class="tabcont"]/div[1]/ul[1]/li[2]/a').click()

            driver.implicitly_wait(100)
            self.car['ps_airbag'] = driver.find_element_by_xpath(head_xpath + '/div[2]/div[2]/table/tbody/tr[1]/td[1]').text
            driver.implicitly_wait(100)
            self.car['ba_side_airbag'] = driver.find_element_by_xpath(head_xpath + '/div[2]/div[2]/table/tbody/tr[1]/td[2]').text
            driver.implicitly_wait(100)
            self.car['ba_head_airbag'] = driver.find_element_by_xpath(head_xpath + '/div[2]/div[2]/table/tbody/tr[2]/td[1]').text
            driver.implicitly_wait(100)
            self.car['tire_pressure'] = driver.find_element_by_xpath(head_xpath + '/div[2]/div[2]/table/tbody/tr[3]/td[1]').text
            driver.implicitly_wait(100)
            self.car['seat_belt_warning'] = driver.find_element_by_xpath(head_xpath + '/div[2]/div[2]/table/tbody/tr[4]/td[1]').text
            driver.implicitly_wait(100)
            self.car['child_seat'] = driver.find_element_by_xpath(head_xpath + '/div[2]/div[2]/table/tbody/tr[4]/td[2]').text
            driver.implicitly_wait(100)
            self.car['abs'] = driver.find_element_by_xpath(head_xpath + '/div[2]/div[2]/table/tbody/tr[5]/td[1]').text
            driver.implicitly_wait(100)
            self.car['ebd'] = driver.find_element_by_xpath(head_xpath + '/div[2]/div[2]/table/tbody/tr[5]/td[2]').text
            driver.implicitly_wait(100)
            self.car['eba'] = driver.find_element_by_xpath(head_xpath + '/div[2]/div[2]/table/tbody/tr[6]/td[1]').text
            driver.implicitly_wait(100)
            self.car['asr'] = driver.find_element_by_xpath(head_xpath + '/div[2]/div[2]/table/tbody/tr[6]/td[2]').text
            driver.implicitly_wait(100)
            self.car['esc'] = driver.find_element_by_xpath(head_xpath + '/div[2]/div[2]/table/tbody/tr[7]/td[1]').text
            driver.implicitly_wait(100)
            self.car['merge_support'] = driver.find_element_by_xpath(head_xpath + '/div[2]/div[2]/table/tbody/tr[7]/td[2]').text
            driver.implicitly_wait(100)
            self.car['deviation_warning'] = driver.find_element_by_xpath(head_xpath + '/div[2]/div[2]/table/tbody/tr[8]/td[1]').text
            driver.implicitly_wait(100)
            self.car['securiyt_system'] = driver.find_element_by_xpath(head_xpath + '/div[2]/div[2]/table/tbody/tr[8]/td[2]').text
            driver.implicitly_wait(100)
            self.car['night_version'] = driver.find_element_by_xpath(head_xpath + '/div[2]/div[2]/table/tbody/tr[9]/td[1]').text

            driver.implicitly_wait(100)
            self.car['parking_radar'] = driver.find_element_by_xpath(head_xpath + '/div[2]/div[4]/table/tbody/tr[1]/td[1]').text
            driver.implicitly_wait(100)
            self.car['parking_video'] = driver.find_element_by_xpath(head_xpath + '/div[2]/div[4]/table/tbody/tr[1]/td[2]').text
            driver.implicitly_wait(100)
            self.car['panoramic_carmera'] = driver.find_element_by_xpath(head_xpath + '/div[2]/div[4]/table/tbody/tr[2]/td[1]').text
            driver.implicitly_wait(100)
            self.car['cruise'] = driver.find_element_by_xpath(head_xpath + '/div[2]/div[4]/table/tbody/tr[2]/td[1]').text
            driver.implicitly_wait(100)
            self.car['adaptive_cruise'] = driver.find_element_by_xpath(head_xpath + '/div[2]/div[4]/table/tbody/tr[3]/td[1]').text
            driver.implicitly_wait(100)
            self.car['automatic_parking'] = driver.find_element_by_xpath(head_xpath + '/div[2]/div[4]/table/tbody/tr[3]/td[2]').text
            driver.implicitly_wait(100)
            self.car['engine_automatic'] = driver.find_element_by_xpath(head_xpath + '/div[2]/div[4]/table/tbody/tr[4]/td[1]').text
            driver.implicitly_wait(100)
            self.car['uphill_support'] = driver.find_element_by_xpath(head_xpath + '/div[2]/div[4]/table/tbody/tr[4]/td[2]').text

            driver.implicitly_wait(100)
            self.car['automatic_skylight'] = driver.find_element_by_xpath(head_xpath + '/div[2]/div[6]/table/tbody/tr[1]/td[1]').text
            driver.implicitly_wait(100)
            self.car['panoramic_skylight'] = driver.find_element_by_xpath(head_xpath + '/div[2]/div[6]/table/tbody/tr[1]/td[2]').text
            driver.implicitly_wait(100)
            self.car['rims'] = driver.find_element_by_xpath(head_xpath + '/div[2]/div[6]/table/tbody/tr[2]/td[2]').text
            driver.implicitly_wait(100)
            self.car['automatic_door'] = driver.find_element_by_xpath(head_xpath + '/div[2]/div[6]/table/tbody/tr[3]/td[1]').text
            driver.implicitly_wait(100)
            self.car['automatic_trunk'] = driver.find_element_by_xpath(head_xpath + '/div[2]/div[6]/table/tbody/tr[4]/td[1]').text
            driver.implicitly_wait(100)
            self.car['induce_trunk'] = driver.find_element_by_xpath(head_xpath + '/div[2]/div[6]/table/tbody/tr[4]/td[2]').text
            driver.implicitly_wait(100)
            self.car['roof_racks'] = driver.find_element_by_xpath(head_xpath + '/div[2]/div[6]/table/tbody/tr[5]/td[1]').text
            driver.implicitly_wait(100)
            self.car['engine_antitheft'] = driver.find_element_by_xpath(head_xpath + '/div[2]/div[6]/table/tbody/tr[5]/td[2]').text
            driver.implicitly_wait(100)
            self.car['parking_lock'] = driver.find_element_by_xpath(head_xpath + '/div[2]/div[6]/table/tbody/tr[6]/td[1]').text
            driver.implicitly_wait(100)
            self.car['remote_key'] = driver.find_element_by_xpath(head_xpath + '/div[2]/div[6]/table/tbody/tr[6]/td[2]').text
            driver.implicitly_wait(100)
            self.car['keyless_start'] = driver.find_element_by_xpath(head_xpath + '/div[2]/div[6]/table/tbody/tr[7]/td[1]').text
            driver.implicitly_wait(100)
            self.car['keyless_entry'] = driver.find_element_by_xpath(head_xpath + '/div[2]/div[6]/table/tbody/tr[7]/td[2]').text

            driver.implicitly_wait(100)
            self.car['steering_wheel'] = driver.find_element_by_xpath(head_xpath + '/div[2]/div[8]/table/tbody/tr[1]/td[1]').text

            type_1 = len(driver.find_elements_by_xpath(head_xpath + '/div[2]/div[10]/table/tbody/tr'))
            if type_1 < 10:
                driver.implicitly_wait(100)
                self.car['seat_memory'] = driver.find_element_by_xpath(
                    head_xpath + '/div[2]/div[10]/table/tbody/tr[5]/td[2]').text
                driver.implicitly_wait(100)
                self.car['seat_falldown'] = driver.find_element_by_xpath(
                    head_xpath + '/div[2]/div[10]/table/tbody/tr[8]/td[1]').text
                driver.implicitly_wait(100)
                self.car['central_armrest'] = driver.find_element_by_xpath(
                    head_xpath + '/div[2]/div[10]/table/tbody/tr[8]/td[2]').text
                driver.implicitly_wait(100)
                self.car['cup_holder'] = driver.find_element_by_xpath(
                    head_xpath + '/div[2]/div[10]/table/tbody/tr[9]/td[1]').text
            else:
                driver.implicitly_wait(100)
                self.car['seat_memory'] = driver.find_element_by_xpath(
                    head_xpath + '/div[2]/div[10]/table/tbody/tr[6]/td[1]').text
                driver.implicitly_wait(100)
                self.car['seat_falldown'] = driver.find_element_by_xpath(
                    head_xpath + '/div[2]/div[10]/table/tbody/tr[9]/td[1]').text
                driver.implicitly_wait(100)
                self.car['central_armrest'] = driver.find_element_by_xpath(
                    head_xpath + '/div[2]/div[10]/table/tbody/tr[9]/td[2]').text
                driver.implicitly_wait(100)
                self.car['cup_holder'] = driver.find_element_by_xpath(
                    head_xpath + '/div[2]/div[10]/table/tbody/tr[10]/td[1]').text

            driver.implicitly_wait(100)
            self.car['seat_material'] = driver.find_element_by_xpath(head_xpath + '/div[2]/div[10]/table/tbody/tr[1]/td[1]').text
            driver.implicitly_wait(100)
            self.car['seat_adjust'] = driver.find_element_by_xpath(head_xpath + '/div[2]/div[10]/table/tbody/tr[2]/td[1]').text
            driver.implicitly_wait(100)
            self.car['ps_seat_adjust'] = driver.find_element_by_xpath(head_xpath + '/div[2]/div[10]/table/tbody/tr[3]/td[2]').text
            driver.implicitly_wait(100)
            self.car['after_seat_adjust'] = driver.find_element_by_xpath(head_xpath + '/div[2]/div[10]/table/tbody/tr[5]/td[1]').text

            type_2 = len(driver.find_elements_by_xpath(head_xpath + '/div[2]/div[12]/table/tbody/tr'))
            if type_2 == 6:
                driver.implicitly_wait(100)
                self.car['interface'] = driver.find_element_by_xpath(
                    head_xpath + '/div[2]/div[12]/table/tbody/tr[5]/td[1]').text
                driver.implicitly_wait(100)
                self.car['cddvd'] = driver.find_element_by_xpath(
                    head_xpath + '/div[2]/div[12]/table/tbody/tr[5]/td[2]').text
                driver.implicitly_wait(100)
                self.car['speaker'] = driver.find_element_by_xpath(
                    head_xpath + '/div[2]/div[12]/table/tbody/tr[6]/td[2]').text
            elif type_2 == 7:
                driver.implicitly_wait(100)
                self.car['interface'] = driver.find_element_by_xpath(
                    head_xpath + '/div[2]/div[12]/table/tbody/tr[6]/td[1]').text
                driver.implicitly_wait(100)
                self.car['cddvd'] = driver.find_element_by_xpath(
                    head_xpath + '/div[2]/div[12]/table/tbody/tr[6]/td[2]').text
                driver.implicitly_wait(100)
                self.car['speaker'] = driver.find_element_by_xpath(
                    head_xpath + '/div[2]/div[12]/table/tbody/tr[7]/td[2]').text
            else:
                driver.implicitly_wait(100)
                self.car['interface'] = driver.find_element_by_xpath(
                    head_xpath + '/div[2]/div[12]/table/tbody/tr[6]/td[2]').text
                driver.implicitly_wait(100)
                self.car['cddvd'] = driver.find_element_by_xpath(
                    head_xpath + '/div[2]/div[12]/table/tbody/tr[7]/td[1]').text
                driver.implicitly_wait(100)
                self.car['speaker'] = driver.find_element_by_xpath(
                    head_xpath + '/div[2]/div[12]/table/tbody/tr[8]/td[1]').text

            driver.implicitly_wait(100)
            self.car['gps'] = driver.find_element_by_xpath(head_xpath + '/div[2]/div[12]/table/tbody/tr[1]/td[1]').text
            driver.implicitly_wait(100)
            self.car['positioning'] = driver.find_element_by_xpath(head_xpath + '/div[2]/div[12]/table/tbody/tr[1]/td[2]').text
            driver.implicitly_wait(100)
            self.car['screen'] = driver.find_element_by_xpath(head_xpath + '/div[2]/div[12]/table/tbody/tr[2]/td[1]').text
            driver.implicitly_wait(100)
            self.car['screen_size'] = driver.find_element_by_xpath(head_xpath + '/div[2]/div[12]/table/tbody/tr[2]/td[2]').text

            driver.implicitly_wait(100)
            self.car['lowlight'] = driver.find_element_by_xpath(head_xpath + '/div[2]/div[14]/table/tbody/tr[1]/td[1]').text
            driver.implicitly_wait(100)
            self.car['highlight'] = driver.find_element_by_xpath(head_xpath + '/div[2]/div[14]/table/tbody/tr[1]/td[2]').text
            driver.implicitly_wait(100)
            self.car['led'] = driver.find_element_by_xpath(head_xpath + '/div[2]/div[14]/table/tbody/tr[2]/td[1]').text
            driver.implicitly_wait(100)
            self.car['adpative_lights'] = driver.find_element_by_xpath(head_xpath + '/div[2]/div[14]/table/tbody/tr[2]/td[2]').text
            driver.implicitly_wait(100)
            self.car['head_lights'] = driver.find_element_by_xpath(head_xpath + '/div[2]/div[14]/table/tbody/tr[3]/td[1]').text
            driver.implicitly_wait(100)
            self.car['support_lights'] = driver.find_element_by_xpath(head_xpath + '/div[2]/div[14]/table/tbody/tr[3]/td[2]').text
            driver.implicitly_wait(100)
            self.car['fog_lights'] = driver.find_element_by_xpath(head_xpath + '/div[2]/div[14]/table/tbody/tr[4]/td[2]').text
            driver.implicitly_wait(100)
            self.car['atmosphere_lights'] = driver.find_element_by_xpath(head_xpath + '/div[2]/div[14]/table/tbody/tr[6]/td[1]').text

            type_3 = len(driver.find_elements_by_xpath(head_xpath + '/div[2]/div[16]/table/tbody/tr'))
            if type_3 < 8:
                driver.implicitly_wait(100)
                self.car['automatic_window'] = driver.find_element_by_xpath(
                    head_xpath + '/div[2]/div[16]/table/tbody/tr[1]/td[1]').text
                driver.implicitly_wait(100)
                self.car['window_lift'] = ''
                driver.implicitly_wait(100)
                self.car['window_anticliphand'] = driver.find_element_by_xpath(
                    head_xpath + '/div[2]/div[16]/table/tbody/tr[1]/td[2]').text
                driver.implicitly_wait(100)
                self.car['insulated_glass'] = driver.find_element_by_xpath(
                    head_xpath + '/div[2]/div[16]/table/tbody/tr[2]/td[1]').text
                driver.implicitly_wait(100)
                self.car['automatic_rearview_adjust'] = driver.find_element_by_xpath(
                    head_xpath + '/div[2]/div[16]/table/tbody/tr[2]/td[2]').text
                driver.implicitly_wait(100)
                self.car['automatic_rearview_fold'] = driver.find_element_by_xpath(
                    head_xpath + '/div[2]/div[16]/table/tbody/tr[3]/td[1]').text
                driver.implicitly_wait(100)
                self.car['makeup_mirror'] = driver.find_element_by_xpath(
                    head_xpath + '/div[2]/div[16]/table/tbody/tr[6]/td[2]').text
                driver.implicitly_wait(100)
                self.car['wipers'] = driver.find_element_by_xpath(
                    head_xpath + '/div[2]/div[16]/table/tbody/tr[7]/td[1]').text
                driver.implicitly_wait(100)
                self.car['induce_wipers'] = driver.find_element_by_xpath(
                    head_xpath + '/div[2]/div[16]/table/tbody/tr[7]/td[2]').text
            else:
                driver.implicitly_wait(100)
                self.car['automatic_window'] = driver.find_element_by_xpath(
                    head_xpath + '/div[2]/div[16]/table/tbody/tr[1]/td[1]').text
                driver.implicitly_wait(100)
                self.car['window_lift'] = driver.find_element_by_xpath(
                    head_xpath + '/div[2]/div[16]/table/tbody/tr[1]/td[2]').text
                driver.implicitly_wait(100)
                self.car['window_anticliphand'] = driver.find_element_by_xpath(
                    head_xpath + '/div[2]/div[16]/table/tbody/tr[2]/td[1]').text
                driver.implicitly_wait(100)
                self.car['insulated_glass'] = driver.find_element_by_xpath(
                    head_xpath + '/div[2]/div[16]/table/tbody/tr[2]/td[2]').text
                driver.implicitly_wait(100)
                self.car['automatic_rearview_adjust'] = driver.find_element_by_xpath(
                    head_xpath + '/div[2]/div[16]/table/tbody/tr[3]/td[1]').text
                driver.implicitly_wait(100)
                self.car['automatic_rearview_fold'] = driver.find_element_by_xpath(
                    head_xpath + '/div[2]/div[16]/table/tbody/tr[5]/td[1]').text
                driver.implicitly_wait(100)
                self.car['makeup_mirror'] = driver.find_element_by_xpath(
                    head_xpath + '/div[2]/div[16]/table/tbody/tr[7]/td[2]').text
                driver.implicitly_wait(100)
                self.car['wipers'] = driver.find_element_by_xpath(
                    head_xpath + '/div[2]/div[16]/table/tbody/tr[8]/td[1]').text
                driver.implicitly_wait(100)
                self.car['induce_wipers'] = driver.find_element_by_xpath(
                    head_xpath + '/div[2]/div[16]/table/tbody/tr[8]/td[2]').text


            driver.implicitly_wait(100)
            self.car['air_conditioning'] = driver.find_element_by_xpath(head_xpath + '/div[2]/div[18]/table/tbody/tr[1]/td[1]').text
            driver.implicitly_wait(100)
            self.car['wind_outlet'] = driver.find_element_by_xpath(head_xpath + '/div[2]/div[18]/table/tbody/tr[2]/td[1]').text

            self.database_process()  # Insert infos into databases.
        except Exception,e:
            print '%s error !' % self.car['name']
            print e

        return None

    def database_process(self):
        """
        Insert infos into databases.
        :return: None
        """
        sql_insert = 'insert into car_infos values ("%s","%s","%s","%s","%s","%s","%s","%s","%s","%s",' \
                     '"%s","%s","%s","%s","%s","%s","%s","%s","%s","%s",' \
                     '"%s","%s","%s","%s","%s","%s","%s","%s","%s","%s",' \
                     '"%s","%s","%s","%s","%s","%s","%s","%s","%s","%s",' \
                     '"%s","%s","%s","%s","%s","%s","%s","%s","%s","%s",' \
                     '"%s","%s","%s","%s","%s","%s","%s","%s","%s","%s",' \
                     '"%s","%s","%s","%s","%s","%s","%s","%s","%s","%s",' \
                     '"%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s")' % (
            self.car['name'], self.car['company'], self.car['level'],self.car['market_time'],
            self.car['engine'],self.car['gearbox'],self.car['lwh'],self.car['body_structure'],
            self.car['maximum_speed'],self.car['fuel_consumption'],self.car['engine_capacity'],
            self.car['engine_form'],self.car['gearbox_type'],self.car['parking_brake_type'],
            self.car['ps_airbag'],self.car['ba_side_airbag'],self.car['ba_head_airbag'],
            self.car['tire_pressure'],self.car['seat_belt_warning'],self.car['child_seat'],
            self.car['abs'],self.car['ebd'],self.car['eba'],self.car['asr'],self.car['esc'],
            self.car['merge_support'],self.car['deviation_warning'],self.car['securiyt_system'],
            self.car['night_version'],self.car['parking_radar'],self.car['parking_video'],
            self.car['panoramic_carmera'],self.car['cruise'],self.car['adaptive_cruise'],
            self.car['automatic_parking'],self.car['engine_automatic'],self.car['uphill_support'],
            self.car['automatic_skylight'],self.car['panoramic_skylight'],self.car['rims'],
            self.car['automatic_door'],self.car['automatic_trunk'],self.car['induce_trunk'],
            self.car['roof_racks'],self.car['engine_antitheft'],self.car['parking_lock'],
            self.car['remote_key'],self.car['keyless_start'],self.car['keyless_entry'],
            self.car['steering_wheel'],self.car['seat_material'],self.car['seat_adjust'],
            self.car['ps_seat_adjust'],self.car['after_seat_adjust'],self.car['seat_memory'],
            self.car['seat_falldown'],self.car['central_armrest'],self.car['cup_holder'],
            self.car['gps'],self.car['positioning'],self.car['screen'],self.car['screen_size'],
            self.car['interface'],self.car['cddvd'],self.car['speaker'],self.car['lowlight'],
            self.car['highlight'],self.car['led'],self.car['adpative_lights'],
            self.car['head_lights'],self.car['support_lights'],self.car['fog_lights'],
            self.car['atmosphere_lights'],self.car['automatic_window'],self.car['window_lift'],
            self.car['window_anticliphand'],self.car['insulated_glass'],
            self.car['automatic_rearview_adjust'],self.car['automatic_rearview_fold'],
            self.car['makeup_mirror'],self.car['wipers'],self.car['induce_wipers'],
            self.car['air_conditioning'],self.car['wind_outlet']
        )

        try:
            self.cursor.execute(sql_insert)
            self.conn.commit()
        except MySQLdb.Error as err:
            print("Error %d : %s" % (err.args[0], err.args[1]))

        return None

    def close_database(self):
        """
        Close database cursor and conn.
        :return: None
        """
        self.cursor.close()
        self.conn.close()
        return None

if __name__ == '__main__':
    bc = BuyCar()
    # bc.get_urls()
    # bc.crwal_urls()
    bc.crawl_infos()
    bc.close_database()

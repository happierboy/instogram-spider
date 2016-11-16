# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
import config
import time
import os, csv

__author__ = 'ZHANGLI'

class url_spiders(object):
    '''spider to crawl the urls from account_config'''
    def __init__(self, intogram_accounts):
        super(url_spiders, self).__init__()
        self.intogram_accounts = intogram_accounts
        self.driver = webdriver.Chrome()
        pass
    
    def spider_accounts(self):
        print 'start crawl intogram account'
        for account in self.intogram_accounts:
            result = self.spider_account(account)
            if result == True:
                self.save_result()
            else:
                self.save_exception()
        self.driver.close()
            
    def spider_account(self, account_url):
        self.account_url = account_url
        self.img_url_dict = {}
        if(True == self.spider_initilization(account_url)):
            self.basic_info = self.spider_crawl_info()
            self.spider_click_load_more()
            self.write_init()
            self.spider_crawl_scroll_down()
            return True
        else:
            return False
    
    def spider_initilization(self, account_url):
        self.driver.get(account_url)
        try:
            self.spider_wait_all_load()
        except Exception:
            return False
        return True
    
    def spider_crawl_info(self):
        info = []
        element = self.driver.find_element_by_xpath("//h1")
        info.append(element.text)
        elements = self.driver.find_elements_by_xpath("//span[@class='_bkw5z']")
        for element in elements:
            if element.get_attribute("title"):
                num = element.get_attribute("title")
                info.append(int(self.normalize_num_str(num)))
            else:
                num = element.text
                info.append(int(self.normalize_num_str(num)))
        return info
    
    def spider_click_load_more(self):
        try:
            js = "window.scrollTo(0,document.body.scrollHeight)"
            self.driver.execute_script(js)
        except WebDriverException:
            print 'scroll fail'
        self.spider_wait_all_load()
        element = self.driver.find_element_by_xpath("//a[@class='_oidfu']")
        assert(element.text.lower()=='load more')
        element.click()
        self.spider_wait_all_load()
    
    def spider_crawl_scroll_down(self):
        self.write_header()
        imgs_hrefs = self.spider_get_imgs()
        pic_num = len(imgs_hrefs)
        unchange_time = 0
        while True:
            try:
                js = "window.scrollBy(0, -50)"
                self.driver.execute_script(js)
                time.sleep(0.5)
                self.spider_wait_all_load()
                js = "window.scrollTo(0, document.body.scrollHeight)"
                self.driver.execute_script(js)
                time.sleep(0.5)
                self.spider_wait_all_load()
            except WebDriverException:
                print 'scroll fail'
                return
            
            imgs_hrefs = self.spider_get_imgs()
            _new_pic_num = len(imgs_hrefs)
            
            if pic_num==_new_pic_num:
                unchange_time = unchange_time + 1
            else:
                self.write_urls(imgs_hrefs)
                pic_num = _new_pic_num
                unchange_time = 0
            
            if unchange_time>0 and unchange_time%10==0:
                js = "window.scrollBy(0, -50)"
                self.driver.execute_script(js)
                time.sleep(10)
                self.spider_wait_all_load()
            
            if unchange_time >= 100:
                break
        return
    
    def spider_get_imgs(self):
        imgs_href = []
        hrefs = self.driver.find_elements_by_xpath("//div[@class='_nljxa']/div[@class='_myci9']/a[@href]")
        for href in hrefs:
            img = href.find_element_by_xpath(".//img")
            if img.get_attribute('src'):
                imgs_href.append((img.get_attribute('src'), href.get_attribute('href')))
        print len(imgs_href)
        return imgs_href
    
    def spider_wait_all_load(self, implicitly_wait_time = 5):
        self.driver.implicitly_wait(implicitly_wait_time)
        try:
            WebDriverWait(self.driver, config.TIMEOUT).until(
                EC.presence_of_element_located((By.XPATH, "//div[@class='_nljxa']"))
            )
        except TimeoutException:
            print 'loading timeout'
        except Exception as e:
            print e
            print 'loading fail'
    
            
    def normalize_num_str(self, num):
        num = num.replace(',','')
        num = num.replace('k', '000')
        num = num.replace('m', '000000')
        return num
    
    def write_init(self):
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.out_dir = os.path.join(os.path.join(self.base_dir, '../file'), self.basic_info[0])
        if not os.path.exists(self.out_dir):
            os.makedirs(self.out_dir)
        self.header_name = os.path.join(self.out_dir, 'info.csv')
        if not os.path.exists(self.header_name):
            with open(self.header_name, 'wt') as fp:
                self.writer = csv.writer(fp)
                self.writer.writerow(('name', 'posts', 'followers', 'following', 
                                      'base_url', 
                                      'update_time',
                                      'total_imgs'))
        self.urls_name = os.path.join(self.out_dir, 'urls.csv')
        if not os.path.exists(self.urls_name):
            with open(self.urls_name, 'wt') as fp:
                self.writer = csv.writer(fp)
                self.writer.writerow(('img_url', 
                                      'href_url',
                                      'update_time'))
        pass
    
    def write_header(self):
        with open(self.header_name, 'at') as fp:
            self.writer = csv.writer(fp)
            self.writer.writerow((self.basic_info[0],
                                  self.basic_info[1], 
                                  self.basic_info[2], 
                                  self.basic_info[3],
                                  self.account_url, 
                                  time.ctime(),
                                  len(self.img_url_dict)))
        pass
    
    def write_urls(self, imgs_hrefs):
        with open(self.urls_name, 'at') as fp:
            self.writer = csv.writer(fp)
            for (img_src, href) in imgs_hrefs:
                if img_src in self.img_url_dict:
                    continue
                else:
                    self.img_url_dict[img_src] = 'https://www.instagram.com' + href
                    self.writer.writerow((img_src, 
                                          self.img_url_dict[img_src], 
                                          time.ctime()))
        pass
        
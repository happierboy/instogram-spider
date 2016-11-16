# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from pyquery import PyQuery as pq
import config
from ubuntu_sso import account
import time


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
        self.basic_info = []
        self.img_url = []
        if(True == self.spider_initilization(account_url)):
            self.basic_info = self.spider_crawl_info()
            self.spider_click_load_more()
            self.spider_scroll_down()
            self.imgs_hrefs = self.spider_get_imgs()
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
        #get title name
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
    
    def spider_scroll_down(self):
        img_divs = self.driver.find_elements_by_xpath("//div[@class='_nljxa']/div[@class='_myci9']")
        pic_num = len(img_divs)
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
            
            img_divs = self.driver.find_elements_by_xpath("//div[@class='_nljxa']/div[@class='_myci9']")
            _new_pic_num = len(img_divs)
            
            if pic_num==_new_pic_num:
                unchange_time = unchange_time + 1
            else:
                pic_num = _new_pic_num
                unchange_time = 0
            
            if unchange_time >= 100:
                break
        return
    
    def spider_get_imgs(self):
        imgs_href = []
        imgs = self.driver.find_elements_by_xpath("//div[@class='_nljxa']/div[@class='_myci9']/img")
        hrefs = self.driver.find_elements_by_xpath("//div[@class='_nljxa']/div[@class='_myci9']/a[@href]")
        assert(len(imgs)==len(hrefs))
        for (img, href) in zip(imgs, hrefs):
            imgs_href.append((img, href))
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
    
    def save_result(self):
        pass
    
    def save_exception(self):
        pass
        
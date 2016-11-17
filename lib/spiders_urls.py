# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import config
import time
from lib.db_users import instogramer, db_instogramer
from lib.logger import spider_logger
from lib.db_imgs import db_imgs
from lib.condition_more_than import count_more_than
from lib import condition_more_than
import random

__author__ = 'ZHANGLI'

class spiders_urls(object):
    def __init__(self, intogram_accounts):
        super(spiders_urls, self).__init__()
        self.intogram_accounts = intogram_accounts
        self.driver = webdriver.Chrome()
        self.db_users = db_instogramer()
        self.logger = spider_logger()
        self.db_imgs = db_imgs()
        pass
    
    def spider_accounts(self):
        self.logger.print_info('start crawl intogram account')
        for base_url in self.intogram_accounts:
            self.spider_account(base_url)
        self.driver.close()
            
    def spider_account(self, base_url):
        self.base_url = base_url
        try:
            self.spider_openpage(base_url)
            user = self.spider_crawl_user(base_url)
            self.db_users.update_users(user)
            self.spider_to_bottom(base_url)
        except Exception as e:
            self.logger.print_error('error to crawl user info exception '+ str(e))
    
    def spider_openpage(self, base_url):
        self.driver.get(base_url)
        self.spider_wait_load_all()
    
    def spider_crawl_user(self, base_url):
        user_dict = {}
        element = self.driver.find_element_by_xpath("//h1")
        user_dict['name'] = element.text
        user_dict['base_url'] = base_url
        info = []
        elements = self.driver.find_elements_by_xpath("//span[@class='_bkw5z']")
        for element in elements:
            if element.get_attribute("title"):
                num = element.get_attribute("title")
                info.append(int(self.normalize_num_str(num)))
            else:
                num = element.text
                info.append(int(self.normalize_num_str(num)))
        user_dict['posts'],user_dict['followers'],user_dict['followings'] = info[0], info[1], info[2]
        return instogramer(user_dict)
    
    def spider_to_bottom(self, base_url):
        try:
            js = "window.scrollTo(0,document.body.scrollHeight)"
            self.driver.execute_script(js)
        except Exception as e:
            self.logger.print_error('scroll fail' + str(e))
        try:
            self.spider_click(xpath = "//a[@class='_oidfu']")
        except Exception as e:
            self.logger.print_error('click fail ' + str(e))
        self.spider_scroll_down(base_url)
    
    def spider_click(self, xpath):
        element = self.driver.find_element_by_xpath(xpath)
        element.click()
        self.driver.implicitly_wait(time_to_wait = 3)
    
    def spider_scroll_down(self, base_url):
        unchange_time = 0
        last_process_time = time.time()
        try:
            while True:
                num = self.spider_get_imgs_num()
                print base_url, str(num)
                try:
                    js = "window.scrollBy(0, -50)"
                    self.driver.execute_script(js)
                    time.sleep(random.randint(25, 75)/50.0)
                    js = "window.scrollTo(0, document.body.scrollHeight)"
                    self.driver.execute_script(js)
                    time.sleep(random.randint(25, 75)/50.0)
                    self.spider_wait_more_than(num = num)
#                     new_num = self.spider_get_imgs_num()
                except Exception as e:
                    self.logger.print_error('scroll fail ' + str(e))
                
                new_num = self.spider_get_imgs_num()
                if new_num==num and unchange_time%5==0:
                    try:
                        self.spider_click(xpath = "//a[@class='_oidfu']")
                    except NoSuchElementException:
                        pass
                    except Exception as e:
                        self.logger.print_info("exception load more during crawl " + str(e))
                
                new_num = self.spider_get_imgs_num()
                if new_num == num:
                    unchange_time = unchange_time + 1
                else:
                    unchange_time = 0
                
                if time.time()-last_process_time>60: #we save the temporal results every two minumtes
                    imgs_hrefs = self.spider_get_imgs()
                    self.db_imgs.update_imgs(base_url, imgs_hrefs)
                    last_process_time = time.time()
                    self.logger.print_info("update {num} images from {base_url}".format(num = len(imgs_hrefs), base_url = base_url))
                
                if unchange_time>16:
                    time.sleep(random.randint(60, 180)/60.0)
                
                if unchange_time > 20:
                    break
        except Exception as e: 
            self.logger.print_error("scroll to bottom error " + str(e))
        finally:
            imgs_hrefs = self.spider_get_imgs()
            self.db_imgs.update_imgs(base_url, imgs_hrefs)
        return
    
    def spider_get_imgs(self):
        imgs_href = []
        hrefs = self.driver.find_elements_by_xpath("//div[@class='_nljxa']/div[@class='_myci9']/a[@href]")
        for href in hrefs:
            img = href.find_element_by_xpath(".//img")
            if img.get_attribute('src'):
                imgs_href.append((img.get_attribute('src'), href.get_attribute('href')))
        return imgs_href
    
    def spider_get_imgs_num(self):
        try:
            hrefs = self.driver.find_elements_by_xpath("//div[@class='_nljxa']/div[@class='_myci9']/a[@href]")
        except Exception:
            return 0
        return len(hrefs)
    
    def spider_wait_load_all(self, implicitly_wait_time = 5):
        self.driver.implicitly_wait(implicitly_wait_time)
        try:
            WebDriverWait(self.driver, config.TIMEOUT).until(
                EC.presence_of_element_located((By.XPATH, "//div[@class='_nljxa']"))
            )
        except Exception as e:
            self.logger.print_warn('loading timeout exception '+ str(e))
    
    def spider_wait_more_than(self, implicitly_wait_time = 5, num = 0):
        self.driver.implicitly_wait(implicitly_wait_time)
        try:
            WebDriverWait(self.driver, timeout=30).until(
                count_more_than(self.driver, "//div[@class='_nljxa']/div[@class='_myci9']/a[@href]", num)
            )
        except Exception as e:
            self.logger.print_info('loading wait_increase failure ' + str(e))
    
            
    def normalize_num_str(self, num):
        num = num.replace(',','')
        num = num.replace('k', '000')
        num = num.replace('m', '000000')
        return num
        
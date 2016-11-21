# -*- coding: utf-8 -*-
'''
Created on 19 Nov 2016

@author: mozat
'''
from spiders_logger import spiders_logger
from lib.db_instagramer_info import db_instagramer_info
from lib.db_instagramer_urls import db_instagramer_urls
from worker.spiders_initial_driver import spiders_driver_initializer
from worker.spiders_initial_page import spiders_page_initializer
from worker.spiders_get_user import spiders_user_info
from worker.spiders_scrolldown_page import spiders_page2bottom
from worker.spiders_click_morebutton import spiders_button_clicker
import time

class spiders_worker(object):
    
    XPATH_HREF = "//div[@class='_nljxa']/div[@class='_myci9']/a[@href]"
    XPATH_IMG_SRC = "//div[@class='_nljxa']/div[@class='_myci9']/a[@href]/div/div/img"
    
    def __init__(self, base_url):
        self.base_url = base_url
        self.spider_log = spiders_logger()
        self.db_users = db_instagramer_info()
        self.db_imgs = db_instagramer_urls()
        super(spiders_worker, self).__init__()
        pass
        
    def spider_download(self, reload = False):
        try:
            newin_number = 0
            self.driver = spiders_driver_initializer().spider_initial_driver()
            spiders_page_initializer(self.driver, self.base_url).spider_initial_page()
            instagramer_info = spiders_user_info(self.driver, self.base_url).spider_get_info()
            spiders_button_clicker(self.driver, self.base_url).spider_click_button()
            last_post_num = int(self.spider_get_posts_num())
            new_post_num = int(instagramer_info.posts)
            if reload==True:
                spiders_page2bottom(self.driver, self.base_url)._to_bottom(new_post_num)
            else:
                spiders_page2bottom(self.driver, self.base_url)._to_bottom(new_post_num-last_post_num)
            imgs_hrefs = self.spider_get_imgs()
            newin_number = self.db_imgs.update_instagramer_urls(self.base_url, imgs_hrefs)
            instagramer_info.posts = last_post_num + newin_number
            self.db_users.update_instagramer_info(instagramer_info)
        except Exception as e:
            print e
            newin_number = 0
        finally:
            self.driver.close()
            return newin_number
            
    def spider_get_posts_num(self):
        if self.base_url in self.db_users.db_instagramers:
            return self.db_users.db_instagramers[self.base_url].posts
        else:
            return 0
    
    def spider_get_imgs(self):
        imgs_href = []
        start_time = time.time()
        href_elements = self.driver.find_elements_by_xpath(spiders_worker.XPATH_HREF)
        self.spider_log.logger.info("locating all hrefs using %0.3f"%(time.time()-start_time))
        img_elements = self.driver.find_elements_by_xpath(spiders_worker.XPATH_IMG_SRC)
        self.spider_log.logger.info("locating all imgs and hrefs using %0.3f"%(time.time()-start_time))
        try:
            for (href, img) in zip(href_elements, img_elements):
                imgs_href.append((img.get_attribute('src'), href.get_attribute('href')))
            self.spider_log.logger.info("getting all imgs with hrefs using %0.3f"%(time.time()-start_time))
        except Exception:
            imgs_href = self.spider_get_imgs_slow(href_elements)
        finally:
            return imgs_href
    def spider_get_imgs_slow(self, href_elements):
        imgs_href = []
        start_time = time.time()
        try:
            for idx, href in enumerate(href_elements):
                img = href.find_element_by_xpath(".//img")
                if img.get_attribute('src'):
                    imgs_href.append((img.get_attribute('src'), href.get_attribute('href')))
                if (idx+1)%1000==0:
                    self.spider_log.logger.info("finds %d imgs under hrefs using %0.3f"%(idx/1000*1000, time.time()-start_time))
        except Exception:
            imgs_href = []
        finally:
            return imgs_href

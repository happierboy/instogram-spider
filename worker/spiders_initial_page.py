'''
Created on 19 Nov 2016

@author: mozat
'''
import config
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from spiders_logger import spiders_logger

class spiders_page_initializer(object):
    XPATH_ALL_LOAD = "//div[@class='_nljxa']"
    def __init__(self, driver, base_url):
        self.driver = driver
        self.base_url = base_url
        self.spider_log = spiders_logger()
        super(spiders_page_initializer, self).__init__()
        pass
    
    def spider_initial_page(self):
        self.driver.get(self.base_url)
        self.spider_wait_loadall()
        
    def spider_wait_loadall(self, implicitly_wait_time = 5):
        self.driver.implicitly_wait(implicitly_wait_time)
        try:
            WebDriverWait(self.driver, config.TIMEOUT).until(
                EC.presence_of_element_located((By.XPATH, spiders_page_initializer.XPATH_ALL_LOAD))
            )
        except NoSuchElementException:
            self.spider_log.logger.warn('loadall no such element exception %s'%(self.base_url))
        except TimeoutException:
            self.spider_log.logger.warn('loadall timeout exception %s'%(self.base_url))
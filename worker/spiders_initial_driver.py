'''
Created on 19 Nov 2016

@author: mozat
'''

from selenium import webdriver
from spiders_logger import spiders_logger

class spiders_driver_initializer(object):
    def __init__(self):
        super(spiders_driver_initializer, self).__init__()
        self.spider_log = spiders_logger()
        pass
    
    def spider_initial_driver(self):
        self.spider_log.logger.info('initial driver')
        chromeOptions = webdriver.ChromeOptions()
        prefs = {"profile.managed_default_content_settings.images":2}
        chromeOptions.add_experimental_option("prefs",prefs)
        driver = webdriver.Chrome(chrome_options=chromeOptions)
        return driver
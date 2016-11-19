'''
Created on 19 Nov 2016

@author: mozat
'''

from spiders_logger import spiders_logger
import time, random

class spiders_button_clicker(object):
    XPATH_BUTTON = "//a[@class='_oidfu']"
    def __init__(self, driver, base_url):
        super(spiders_button_clicker, self).__init__()
        self.spider_log = spiders_logger()
        self.driver = driver
        self.base_url = base_url
        pass
    
    def spider_click_button(self):
        js = "window.scrollTo(0,document.body.scrollHeight)"
        self.driver.execute_script(js)
        time.sleep(random.randrange(1, 4))
        element = self.driver.find_element_by_xpath(spiders_button_clicker.XPATH_BUTTON)
        element.click()
        self.driver.implicitly_wait(time_to_wait = random.randrange(3,6))
        self.spider_log.logger.info('clicked load more button')
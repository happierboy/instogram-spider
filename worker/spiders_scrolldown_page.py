'''
Created on 19 Nov 2016

@author: mozat
'''
from lib.condition_more_than import count_more_than
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from spiders_logger import spiders_logger
import time, random, math


class spiders_page2bottom(object):
    XPATH_IMG_HREF = "//div[@class='_nljxa']/div[@class='_myci9']/a[@href]"
    def __init__(self, driver, base_url):
        super(spiders_page2bottom, self).__init__()
        self.spider_log = spiders_logger()
        self.driver = driver
        self.base_url = base_url
        pass
    
    def _to_bottom(self, _to_bottom_num):
        unchange_time = 0
        self.spider_log.logger.info('start scroll down')
        while True:
            current_num = self.spider_get_imgnum()
            try:
                for idx in range(0, random.randint(1,4)):
                    scroll_len = random.randint(-200, -50)* min(math.ceil(math.sqrt(current_num)/15), 10)
                    js = "window.scrollBy(0, %d)"%(scroll_len+idx)
                    self.driver.execute_script(js)
                    time.sleep(0.3*math.ceil(current_num/1000))
                time.sleep(random.randint(25, 75)/50.0)
                js = "window.scrollTo(0, document.body.scrollHeight)"
                self.driver.execute_script(js)
                time.sleep(random.randint(25, 75)/50.0*math.ceil(current_num/5000))
                self.spider_wait_morethan(current_num = current_num)
            except Exception:
                self.spider_log.logger.error('scroll failed')
                
            new_num = self.spider_get_imgnum()
            print self.base_url, str(current_num)
            if new_num == current_num:
                unchange_time = unchange_time + 1
                time.sleep(random.randint(25, 75)/50.0*math.ceil(current_num/1500))
            else:
                unchange_time = 0   
            if unchange_time > 10 or new_num>=_to_bottom_num:
                break
        self.spider_log.logger.info('finish scroll down with %d imgs'%(new_num))
    
    def spider_get_imgnum(self):
        try:
            hrefs = self.driver.find_elements_by_xpath(spiders_page2bottom.XPATH_IMG_HREF)
            img_num = len(hrefs)
        except Exception:
            img_num = 0
        finally:
            return img_num
    
    def spider_wait_morethan(self, implicitly_wait_time = 5, current_num = 0):
        self.driver.implicitly_wait(implicitly_wait_time)
        try:
            WebDriverWait(self.driver, timeout = 15).until(
                count_more_than(self.driver, spiders_page2bottom.XPATH_IMG_HREF, current_num)
            )
        except Exception:
            self.spider_log.logger.info('wait_increase failure')
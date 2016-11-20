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
        self.spider_log.logger.info('start scroll down: targeting %d imgs in %s'%(_to_bottom_num, self.base_url))
        new_num = current_num = 24
        while True:
            current_num = new_num
            try:
                scroll_times = max(int(math.ceil(current_num/250.0)),20)
                for _ in range(scroll_times):
                    for _ in range(4):
                        interval_times = random.randint(int(math.ceil(scroll_times/4.0)), \
                                                        int(math.ceil(scroll_times/2.0))+1)
                        scroll_len = random.randint(-200, -50)* interval_times
                        js = "window.scrollBy(0, %d)"%(scroll_len)
                        self.driver.execute_script(js)
                        time.sleep(random.uniform(0.2, 0.5))
                    time.sleep(random.uniform(0.5, 1.5))
                    js = "window.scrollTo(0, document.body.scrollHeight)"
                    self.driver.execute_script(js)
                    time.sleep(random.uniform(0.5,1.5))      
            except Exception:
                self.spider_log.logger.error('scroll failed')
                
            self.spider_wait_morethan(current_num = current_num)  
            new_num = self.spider_get_imgnum()
            self.spider_log.logger.info('download %d from %s'%(new_num, self.base_url))
            print self.base_url, str(new_num)
            if new_num == current_num:
                unchange_time = unchange_time + 1
                time.sleep(random.uniform(0.5, 1.5))
            else:
                unchange_time = 0  
            if (unchange_time+1)%10==0:
                time.sleep(random.randint(10, 20)) 
            if unchange_time >= 30:
                self.spider_log.logger.critical('error in account: %s'%(self.base_url))
                raise Exception("error in account %s"%(self.base_url))
            if new_num>=_to_bottom_num:
                break
            if new_num>= _to_bottom_num-5 and unchange_time>=5:
                self.spider_log.logger.critical(\
                                                'error in account: %s, posts %d imgs but only gets %d imgs'%\
                                                (self.base_url, _to_bottom_num, new_num))
                break
                
        self.spider_log.logger.info('finish scroll down: %d imgs in %s'%(new_num, self.base_url))
    
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
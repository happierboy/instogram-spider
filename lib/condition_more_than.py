'''
Created on 17 Nov 2016

@author: mozat
'''

class count_more_than(object):
    def __init__(self, driver, xpath, num):
        self.xpath = xpath
        self.driver = driver
        self.num = num
    
    def __call__(self, ignored):
        try:
            count = self.driver.find_elements_by_xpath(self.xpath)
            num = len(count)
        except Exception:
            num = 0
        finally:
            return num>self.num
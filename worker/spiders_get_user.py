'''
Created on 19 Nov 2016

@author: mozat
'''

from lib.db_instagramer_info import instagramer

class spiders_user_info(object):
    XPATH_USER_NAME = "//h1"
    XPATH_USER_INFO = "//span[@class='_bkw5z']"
    
    def __init__(self, driver, base_url):
        self.driver = driver
        self.base_url = base_url
        super(spiders_user_info, self).__init__()
    
    def spider_get_info(self):
        user_dict = {}
        element = self.driver.find_element_by_xpath(spiders_user_info.XPATH_USER_NAME)
        user_dict['name'] = element.text
        user_dict['base_url'] = self.base_url
        info = []
        elements = self.driver.find_elements_by_xpath(spiders_user_info.XPATH_USER_INFO)
        for element in elements:
            if element.get_attribute("title"):
                num = element.get_attribute("title")
                info.append(int(self.instagram_str2num(num)))
            else:
                num = element.text
                info.append(int(self.instagram_str2num(num)))
        user_dict['posts'],user_dict['followers'],user_dict['followings'] = info[0], info[1], info[2]
        return instagramer(user_dict)
    
    def instagram_str2num(self, str_num):
        str_num = str_num.replace(',','')
        str_num = str_num.replace('k', '000')
        num = str_num.replace('m', '000000')
        return num
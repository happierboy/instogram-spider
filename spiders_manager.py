# -*- coding: utf-8 -*-
from spiders_accounts import instagram_accounts
import config
from spiders_logger import spiders_logger
from worker.spiders_worker import spiders_worker
import random, math, time

__author__ = 'ZHANGLI'

class spiders_manager(object):
    def __init__(self, intagram_accounts):
        self.intagram_accounts = intagram_accounts
        self.spider_log = spiders_logger()
        super(spiders_manager, self).__init__()
        pass
    
    def spider_get_rest_time(self, use_time):
        return random.randint(50,70)*math.ceil(use_time/config.ACCOUNT_SLEEP_INTERVAL)
    
    def spider_accounts(self):
        for base_url in self.intagram_accounts:
            start_time = time.time()
            self.spider_log.logger.info('start crawl intagram account: %s'%(base_url))
            worker = spiders_worker(base_url)
            newin_number = worker.spider_download()
            self.spider_log.logger.info('finish crawl intagram account: %s with %d imgs'%(base_url, newin_number))
            finish_time = time.time()
            self.spider_log.logger.info('account: %s, usage: %0.3f, newin_num: %d'%(base_url, finish_time-start_time, newin_number))
            time.sleep(self.spider_get_rest_time(finish_time-start_time))
        

if __name__ == '__main__':
    if __name__ == "__main__":
        spiders = spiders_manager(instagram_accounts)
        spiders.spider_accounts()
        pass
'''
Created on 17 Nov 2016

@author: mozat
'''

import logging
import os
import time

base_dir = os.path.dirname(os.path.abspath(__file__))

def singleton(cls):
    instances = {}
    def getinstance():
        if cls not in instances:
            instances[cls] = cls()
        return instances[cls]
    return getinstance

@singleton
class spiders_logger(object):
    _instance = None
    def __init__(self, filename = 'spider_instogram.log'):
        self.logger_name = self.__class__.__name__
        self.logger = logging.getLogger(self.logger_name)
        self.logger.setLevel(logging.DEBUG)
        self.logger.propagate = False
        filename = time.strftime("%Y-%m-%d %H:%M:%S.log", time.localtime())
        log_path = os.path.join(os.path.join(base_dir, 'log'), filename)
        self.fh = logging.FileHandler(log_path)
        self.fh.setLevel(logging.DEBUG)
        fmt = "%(asctime)-15s %(levelname)s %(filename)s %(lineno)d %(process)d %(message)s"
        datefmt = "%a %d %b %Y %H:%M:%S"
        formatter = logging.Formatter(fmt, datefmt)
        
        self.fh.setFormatter(formatter)
        self.logger.addHandler(self.fh)
    
    def print_debug(self, msg):
        self.logger.debug(msg)
    
    def print_info(self, msg):
        self.logger.info(msg)
        
    def print_warn(self, msg):
        self.logger.warn(msg)
    
    def print_error(self, msg):
        self.logger.error(msg)
    
    def print_critical(self, msg):
        self.logger.critical(msg)


if __name__ == '__main__':
    sl = spiders_logger('test.log')
    sl.print_debug('debug')
    sl.print_info('info')
    sl.print_warn('warn')
    sl.print_error('error')
    sl.print_critical('critical')
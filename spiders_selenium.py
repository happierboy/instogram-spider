#-*- coding: utf-8 -*-
'''
Created on 15 Nov 2016

@author: mozat
'''

from lib.spiders_urls import spiders_urls
from account_config import instogram_accounts

__author__ = 'ZHANGLI'

if __name__ == "__main__":
    spiders = spiders_urls(instogram_accounts)
    spiders.spider_accounts()
    pass
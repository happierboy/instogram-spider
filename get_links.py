#-*- coding: utf-8 -*-
'''
Created on 15 Nov 2016

@author: mozat
'''

from lib.url_spiders import url_spiders
from account_config import intogram_accounts

__author__ = 'ZHANGLI'

if __name__ == "__main__":
    spiders = url_spiders(intogram_accounts)
    spiders.spider_accounts()
    pass
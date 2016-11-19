'''
Created on 17 Nov 2016

@author: mozat
'''
from db.simple_dbs import MySQL
from config import INSTOGRAM_SCHEMA
import datetime


class db_instagramer_urls(object):
    
    _DB_CONFIG = 'spider_instagram'
    _TB_CONFIG = 'instagramer_urls'
    
    def __init__(self):
        self._db_config = db_instagramer_urls._DB_CONFIG
        self._tb_config = db_instagramer_urls._TB_CONFIG
        self.imgs_dicts = {}
        self.conn = MySQL(INSTOGRAM_SCHEMA)
        super(db_instagramer_urls, self).__init__()
        pass
    
    def get_imgs(self, base_url, reload = False):
        if base_url in self.imgs_dicts and reload == False:
            return self.imgs_dicts[base_url]
        
        _sql_template = '''select base_url,img_url, href from {schema}.{table} where base_url = '{base_url}';'''
        imgs_records = self.conn.fetch_rows(_sql_template.format(schema = self._db_config, 
                                                                 table = self._tb_config,
                                                                 base_url = base_url))
        imgs_dict = {}
        for record in imgs_records:
            imgs_dict[record['img_url']] = 1
        
        self.imgs_dicts[base_url] = imgs_dict
        return imgs_dict
    
    def load_all(self):
        _sql_template = '''select distinct base_url from {schema}.{table}'''.format(schema = self._db_config, 
                                                                 table = self._tb_config)
        base_url_records = self.conn.fetch_rows(_sql_template)
        for record in base_url_records:
            self.get_imgs(record['base_url'], reload = True)
        return self.imgs_dicts
    
    def update_instagramer_urls(self, base_url, crawl_list):
        
        _insert_template = '''insert into {schema}.{table} (base_url, img_url, href, update_time) values '''.format(schema = self._db_config, table = self._tb_config)
        _value_template = '''('{base_url}','{img_url}','{href}', '{update_time}')'''
                        
        imgs_dict = self.get_imgs(base_url)
        _value_list = []
        update_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        for (img_url, href) in crawl_list:
            if img_url in imgs_dict:
                continue
            else:
                imgs_dict[img_url] = href
                _value_list.append(_value_template.format(base_url = base_url, 
                                                        img_url = img_url, 
                                                        href = href, 
                                                        update_time = update_time))
        if _value_list:
            sql = _insert_template + ','.join(_value_list)
            affect_rows = self.conn.execute(sql)
        else:
            affect_rows = 0
        return affect_rows
                
if __name__ == '__main__':
    crawl_list = [('deja', 'www.deja.me')]
    t = db_instagramer_urls()
    t.update_instagramer_urls('www.deja.me', crawl_list)
    
        
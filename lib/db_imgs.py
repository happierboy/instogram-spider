'''
Created on 17 Nov 2016

@author: mozat
'''
from db.simple_dbs import MySQL
from config import INSTOGRAM_SCHEMA
import datetime


class db_imgs(object):
    
    _DB_CONFIG = 'spider_instogram'
    _TB_CONFIG = 'instogramer_urls'
    
    def __init__(self):
        self._db_config = db_imgs._DB_CONFIG
        self._tb_config = db_imgs._TB_CONFIG
        self.imgs_dicts = {}
        self.conn = MySQL(INSTOGRAM_SCHEMA)
        super(db_imgs, self).__init__()
        pass
    
    def get_imgs(self, base_url):
        if base_url in self.imgs_dicts:
            return self.imgs_dicts[base_url]
        
        _sql_template = '''select base_url,img_url, href from {schema}.{table} where base_url = '{base_url}';'''
        imgs_records = self.conn.fetch_rows(_sql_template.format(schema = self._db_config, 
                                                                 table = self._tb_config,
                                                                 base_url = base_url))
        imgs_dict = {}
        for record in imgs_records:
            imgs_dict[record['img_url']] = record['href']
        
        self.imgs_dicts[base_url] = imgs_dict
        return imgs_dict
    
    def load_all(self):
        _sql_template = '''select distinct base_url from {schema}.{table}'''.format(schema = self._db_config, 
                                                                 table = self._tb_config)
        base_urls = self.conn.fetch_row(_sql_template)
        for base_url in base_urls:
            self.get_imgs(base_url)
        return self.imgs_dicts
    
    def update_imgs(self, base_url, crawl_list):
        
        _sql_template = '''insert into {schema}.{table} (base_url, img_url, href, update_time) values '''.format(schema = self._db_config, table = self._tb_config)
        value_template = '''('{base_url}','{img_url}','{href}', '{update_time}')'''
                        
        imgs_dict = self.get_imgs(base_url)
        value_list = []
        for (img_src, href) in crawl_list:
            if img_src in imgs_dict:
                continue
            else:
                update_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                sql = _sql_template.format(base_url = base_url, img_url = img_src, href = href, 
                                           update_time = update_time)
                imgs_dict[img_src] = href
                value_list.append(value_template.format(base_url = base_url, 
                                                        img_url = img_src, 
                                                        href = href, 
                                                        update_time = update_time))
        if value_list:
            sql = _sql_template + ','.join(value_list)
            self.conn.execute(sql)
                

        
    
if __name__ == '__main__':
    crawl_list = [('deja', 'www.deja.me')]
    t = db_imgs()
    t.update_imgs('www.deja.me', crawl_list)
    
        
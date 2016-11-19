'''
Created on 17 Nov 2016

@author: mozat
'''
from db.simple_dbs import MySQL
from config import INSTOGRAM_SCHEMA
import datetime

class instagramer(object):
    def __init__(self, user_dict):
        self.name = user_dict['name']
        self.posts = user_dict['posts']
        self.followings = user_dict['followings']
        self.followers = user_dict['followers']
        self.base_url  =user_dict['base_url']
    
    def to_dict(self):
        user_dict = {}
        user_dict['base_url'] = self.base_url
        user_dict['name'] = self.name
        user_dict['posts'] = self.posts
        user_dict['followings'] = self.followings
        user_dict['followers'] = self.followers
        user_dict['update_time'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return user_dict

class db_instagramer_info(object):
    '''later we should pass base_url to this class, as each worker only need to know its own info'''
    _DB_CONFIG = 'spider_instagram'
    _TB_CONFIG = 'instagramer_info'
    
    def __init__(self):
        self._db_config = db_instagramer_info._DB_CONFIG
        self._tb_config = db_instagramer_info._TB_CONFIG
        self.conn = MySQL(INSTOGRAM_SCHEMA)
        self.db_instagramers = None
        self.db_instagramers = self.get_instagramers()
        super(db_instagramer_info, self).__init__()
        pass
    
    def get_instagramers(self, reload = False):
        if self.db_instagramers and reload==False:
            return self.db_instagramers
        
        _sql_template = 'select * from {schema}.{table};'
        user_records = self.conn.fetch_rows(_sql_template.format(schema = self._db_config, table = self._tb_config))
        users_dict = {}
        for user_dict in user_records:
            users_dict[user_dict['base_url']] = instagramer(user_dict)
        
        self.db_instagramers = users_dict
        return self.db_instagramers
    
    def update_instagramer_info(self, instagramer_instance):
        if instagramer_instance.base_url in self.get_instagramers():
            _sql_template = '''update {schema}.{table}'''.format(schema = self._db_config, table = self._tb_config)\
                                +''' set name = '{name}', 
                        posts = {posts}, 
                        followings = {followings}, 
                        followers = {followers},
                        update_time =  '{update_time}'
                        where base_url= '{base_url}';'''.format(**(instagramer_instance.to_dict()))
            self.conn.execute(_sql_template)
            pass
        else:
            _sql_template = '''insert into {schema}.{table} '''.format(schema = self._db_config, table = self._tb_config)\
                                +'''(base_url, name, posts, followings, followers, update_time) values(
                                '{base_url}', '{name}', {posts}, {followings}, {followers}, '{update_time}'
                                )'''.format(**(instagramer_instance.to_dict()))
            self.conn.execute(_sql_template)
            pass
    
if __name__ == '__main__':
    import random
    
    user_dict = {}
    user_dict['name'] = 'zhangli'
    user_dict['posts'] = 100
    user_dict['followings'] = 100
    user_dict['followers'] = 10000
    user_dict['base_url'] = 'www.google.com'
    instagramer_instance = instagramer(user_dict)
    t = db_instagramer_info()
    t.update_instagramer_info(instagramer_instance)
    
    for url, instagramer_instance in t.get_instagramers(reload=True).iteritems():
        print url, instagramer_instance.posts
        instagramer_instance.posts = random.randint(1, 1000)
        t.update_instagramer_info(instagramer_instance)
        user_dict = instagramer_instance.to_dict()
        user_dict['base_url'] = 'www.deja.me'
        new_instagramer_instance = instagramer(user_dict)
        t.update_instagramer_info(new_instagramer_instance)
        
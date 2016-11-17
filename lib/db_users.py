'''
Created on 17 Nov 2016

@author: mozat
'''
from db.simple_dbs import MySQL
from config import INSTOGRAM_SCHEMA
import datetime

class instogramer(object):
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

class db_instogramer(object):
    
    _DB_CONFIG = 'spider_instogram'
    _TB_CONFIG = 'instogramer_info'
    
    def __init__(self):
        self._db_config = db_instogramer._DB_CONFIG
        self._tb_config = db_instogramer._TB_CONFIG
        self.conn = MySQL(INSTOGRAM_SCHEMA)
        self.db_users = None
        self.db_users = self.get_users()
        super(db_instogramer, self).__init__()
        pass
    
    def get_users(self):
        if self.db_users:
            return self.db_users
        
        _sql_template = 'select * from {schema}.{table}'
        user_records = self.conn.fetch_rows(_sql_template.format(schema = self._db_config, table = self._tb_config))
        users_dict = {}
        for user in user_records:
            users_dict[user['base_url']] = instogramer(user)
        
        self.db_users = users_dict
        return self.db_users
    
    def update_users(self, instogram_instance):
        if instogram_instance.base_url in self.db_users:
            _sql_template = '''update {schema}.{table}'''.format(schema = self._db_config, table = self._tb_config)\
                                +''' set name = '{name}', 
                        posts = {posts}, 
                        followings = {followings}, 
                        followers = {followers},
                        update_time =  '{update_time}'
                        where base_url= '{base_url}';'''.format(**(instogram_instance.to_dict()))
            self.conn.execute(_sql_template)
            pass
        else:
            _sql_template = '''insert into {schema}.{table} '''.format(schema = self._db_config, table = self._tb_config)\
                                +'''(base_url, name, posts, followings, followers, update_time) values(
                                '{base_url}', '{name}', {posts}, {followings}, {followers}, '{update_time}'
                                )'''.format(**(instogram_instance.to_dict()))
            self.conn.execute(_sql_template)
            pass
    
if __name__ == '__main__':
    import random
    t = db_instogramer()
    for url, value in  t.get_users().iteritems():
        print url, value.posts
        value.posts = random.randint(1, 1000)
        t.update_users(value)
        value_dict = value.to_dict()
        value_dict['base_url'] = 'www.deja.me'
        value1 = instogramer(value_dict)
        t.update_users(value1)
        
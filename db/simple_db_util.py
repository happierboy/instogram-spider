'''
DB -> MySQL

Configuration Parameters:
Name            Type           Meaning
type            str            mysql, sqlserver, hive
host            str            host name                
port            int            port (optional)
user            str            user name
password        str            password
database        string         default database
'''

_DB_CLASS = {}
def get_db_class_by_type(name):
    if name in _DB_CLASS: # cache hit
        return _DB_CLASS[name]
    
    # dynamic load
    cls = None
    if name == 'mysql':
        from similar_item.db.simple_dbs import MySQL as cls 
    else:
        raise Exception('unknown type {0}'.format(name))   
       
    _DB_CLASS[name] = cls # cache it
    return _DB_CLASS[name]

_DB_POOL = {}
def get_db(config):
    '''Returns a database object.'''
  
    # no cache
    if not config.get('cache_conn', True):
        return get_db_class_by_type(config['type'])(config)
    
    # db pool key
    db_pool_key = str(config)
    
    # remove closed connection
    if db_pool_key in _DB_POOL and not _DB_POOL[db_pool_key].is_open(): 
        del _DB_POOL[db_pool_key]
        
    # create a new connection is necessary    
    if db_pool_key not in _DB_POOL:
        _DB_POOL[db_pool_key] = get_db_class_by_type(config['type'])(config) 
    return _DB_POOL[db_pool_key]

def test():
    print 'Start test_relations connection...'

    conn = {'host' : "10.160.241.142",
            'type': "mysql",
            'port': '3307',
            'username': 'mozone',
            'password': 'morangerunmozone',
            'db': 'test_relations',
           }
    conn = get_db(conn)
    
    ### Test fetch_rows()
    rows = conn.fetch_rows(r'''SELECT * FROM test_relations.product p where id >= 1 and id <= 10''')
    assert(len(rows) == 10)
    
    ### Test fetch_row()
    row = conn.fetch_row(r'''SELECT * FROM test_relations.product p where id = 1''')
    assert(row['pid'] == '5017147')
    
    ### Test execute()
    old_price = int(row['price'])
    new_price = old_price+1
    conn.execute(r'''update test_relations.product p set price = price + 1 where id = 1;''')
    new_price_in_db = conn.fetch_number(r'''SELECT price FROM test_relations.product p where id = 1''')
    assert(new_price_in_db == new_price)
    
    print 'End test_relations connection, test_relations is success!!!'
    
if __name__ == '__main__':
    test()
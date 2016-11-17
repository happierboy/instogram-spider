from similar_item.db.simple_db_util import get_db

def escape_quotes(my_str):
    return my_str.replace('"', '\\"')

class DB_Cache(object):
    '''
    must call the flush manually.
    '''    
    def __init__(self, cache_size, conn_config, table_name,  columns, verbose=False):
        assert(type(cache_size) == int)
        self.enable = False
        self.cache = []
        self.cache_size = cache_size
        self.conn_config = conn_config
        self.conn = get_db(self.conn_config)
        self.verbose = verbose
        self.columns = columns
        self.table_name = table_name
        
    def enable_cache(self):
        self.enable = True
        self.flush()
    
    def disable_cache(self):
        self.enable = False
        self.flush()

    def add(self, row):
        for column in self.columns:
            assert(column in row)
        self.cache.append(row)
        if self.enable == False or len(self.cache) >= self.cache_size:
            self.flush()
            
    def flush(self):
        'insert all rows in self.cache into db' 
        raise NotImplementedError()
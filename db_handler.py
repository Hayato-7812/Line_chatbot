import sqlite3
import logging
import pandas as pd
from datetime import  datetime
LOGGER = logging.getLogger(__name__)

class dbvalue_base():
    #self.attr[0] must be primary key
    def to_list(self):
        return [str(getattr(self,k)) for k in self.attr]
    def to_dict(self):
        return {k:str(getattr(self,k)) for k in self.attr}

class dbvalue_urls(dbvalue_base):
    def __init__(self,_id=-1, _url="",  _date="", _user="",_comment=""):
        self.id = _id
        self.url = _url
        self.date = _date
        self.user = _user
        self.comment = _comment
        self.attr= ["id", "url", "date","user","comment"]
        self.table="urls"

def dbopen(dbfile):
    def recv_func(func):
        def wrapper(*args, **kwargs):
            conn = sqlite3.connect(dbfile)
            cur = conn.cursor()
            result = func(conn,cur,*args)
            conn.commit()
            cur.close()
            conn.close()
            return result
        return wrapper
    return recv_func
 
@dbopen('music.db')
def add_item(conn,cur,obj:dbvalue_urls):
    sql = 'insert into {} (id, url, date,user,comment) values (?,?,?,?,?)'.format(obj.table)
    data = (obj.id, obj.url, obj.date,obj.user,obj.comment)
    cur.execute(sql, data)

@dbopen('music.db')
def get_data(conn,cur):
    data = pd.read_sql('SELECT * FROM urls', conn)
    return(data)

@dbopen('music.db')
def get_items(conn,cur,tablename="urls"): 
        cur.execute('SELECT * FROM {}'.format(tablename))
        return cur.fetchall()  #全ての行をリストで取得する。

@dbopen('music.db')
def get_dbdf(conn,cur):
    df = pd.read_sql('SELECT * FROM urls', conn)
    return df


if __name__ == "__main__":
    obj= dbvalue_urls(
            _id=6,
            _url="https://www.youtube.com/watch?v=uAqITu9ypDo",
            _date = datetime.today(),
            _user = "testman",
            _comment = "nice!"
        )
    
    print(get_dbdf())
    
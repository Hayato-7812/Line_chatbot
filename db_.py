import sqlite3
import logging
from unittest import result
import pandas as pd
from datetime import date, datetime
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

class db_handler():    
    def db_connect(dbfile="music.db"):
        def cursor_moniter(func):
            def wrapper(*args, **kwargs):
                LOGGER.info("db connecting ...")
                conn = sqlite3.connect(dbfile)
                LOGGER.info("succeed !")
                cur = conn.cursor()
                func(cur,*args)#これはtest()
                conn.commit()
                cur.close()
                conn.close()
                LOGGER.info("commit and close db done")
            return wrapper()
        return cursor_moniter
       
    
    def get_item_cnt(self,tablename="urls"):
        sql = 'SELECT count(*) FROM ' + tablename
        self.execute(sql)
        cnt = self.conn.fetchall()[0][0]
        self.LOGGER.info("item count: {}".format(cnt))
        return  cnt

    @db_connect()
    def add_item(cur,obj):
        sql = 'insert into {} (id, url, date,user,comment) values (?,?,?,?,?)'.format(obj.table)
        data = (obj.id, obj.url, obj.date,obj.user,obj.comment)
        cur.execute(sql, data)

    @db_connect()
    def remove_item(id):
        pass

    @db_connect()
    def get_items(self,tablename="music"): 
        self.cur.execute('SELECT * FROM {}',format(tablename))
        return cur.fetchall()  #全ての行をリストで取得する。

def make_newTable():
    df = pd.read_csv("music.csv",)

    dbname = 'music.db'

    conn = sqlite3.connect(dbname)
    cur = conn.cursor()

    # dbのnameをsampleとし、読み込んだcsvファイルをsqlに書き込む
    # if_existsで、もしすでにexpenseが存在していたら、書き換えるように指示
    df.to_sql('urls', conn, if_exists='replace',index=False)

    # 作成したデータベースを1行ずつ見る
    select_sql = 'SELECT * FROM urls'
    for row in cur.execute(select_sql):
        print(row)

    cur.close()
    conn.close()


if __name__ == "__main__":
    # make_newTable()
    h = db_handler()
    obj= dbvalue_urls(
        _id=6,
        _url="https://www.youtube.com/watch?v=uAqITu9ypDo",
        _date = datetime.today(),
        _user = "testman",
        _comment = "nice!"
    )
    h.add_item(obj)

    dbname = "music.db"
    conn = sqlite3.connect(dbname)
    cur = conn.cursor()

    # dbをpandasで読み出す。
    df = pd.read_sql('SELECT * FROM urls', conn)

    print(df)

    cur.close()
    conn.close()
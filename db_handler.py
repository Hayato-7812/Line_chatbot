from operator import getitem
import logging
from datetime import datetime as dt 
import psycopg2
import os
from youtube_utils import *
import random

DATABASE_URL = os.environ["DATABASE_URL"]

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.INFO)

class dbvalue_base():
    #self.attr[0] must be primary key
    def to_list(self):
        return [str(getattr(self,k)) for k in self.attr]
    def to_dict(self):
        return {k:str(getattr(self,k)) for k in self.attr}

class dbvalue_urls(dbvalue_base):
    def __init__(self,_id=-1,_rec_date="",_rec_by="",_title="",_uri="",_comment=None):
        self.id = _id
        self.rec_date = _rec_date
        self.rec_by = _rec_by
        self.title = _title
        self.uri = _uri
        self.comment = _comment
        self.attr= ["id","rec_date","rec_by","title","uri","comment"]
        self.table="A_MUSIC"

def dbopen():
    def recv_func(func):
        def wrapper(*args, **kwargs):
            # conn = sqlite3.connect("music.db")
            try:
                conn = psycopg2.connect(DATABASE_URL, sslmode='require')
                cur = conn.cursor()
            except Exception as e:
                print (e)
                print("retry connecting ...")
                conn = psycopg2.connect(DATABASE_URL, sslmode='require')
                cur = conn.cursor()
            result = func(conn,cur,*args)
            conn.commit()
            cur.close()
            conn.close()
            return result
        return wrapper
    return recv_func
 
@dbopen()
def add_item(conn,cur,obj:dbvalue_urls):
    # data = (obj.id, obj.uri,datetime.today(),obj.rec_by,obj.comment)
    # sql = 'INSERT INTO {} (ID,URL,USER,DATE,COMMENT) VALUES(?,?,?,?,?)'.format("urls")
    # cur.execute(sql,data)
    # sql = 'INSERT INTO {} (ID,URI,REC_BY,COMMENT) VALUES(?,?,?,?)'.format(obj.table)
    # data = (obj.id, obj.uri,obj.rec_by,obj.comment)
    # cur.execute(sql, data)
    cur.execute("INSERT INTO {} (ID,REC_DATE,REC_BY,TITLE,URI,COMMENT) VALUES ({}, '{}','{}','{}','{}','{}')".format(obj.table,obj.id,obj.rec_date,obj.rec_by,obj.title,obj.uri,obj.comment))
    print("add item('ID={},REC_DATE={},REC_BY={},TITLE={},URI={},COMMENT={}) to {}".format(obj.id,obj.rec_date,obj.rec_by,obj.title,obj.uri,obj.comment,obj.table))

@dbopen()
def get_data(conn,cur,tablename = "A_MUSIC"):
    sql = 'SELECT * FROM {}'.format(tablename)
    cur.execute(sql)

@dbopen()
def get_items(conn,cur,tablename="A_MUSIC"):  #as dict in list 
    # print("get db items")
    cur.execute("select * from {}".format(tablename))
    result = []
    for row in cur:
        # print("row:{}".format(row))
        result.append(dbvalue_urls(row[0],row[1],row[2],row[3],row[4],row[5]).to_dict())
    result.reverse()
    
    return result

@dbopen()
def get_next_id(conn,cur,tablename="A_MUSIC"):
    sql = 'SELECT count(*) FROM {}'.format(tablename)
    cur.execute(sql)
    result = cur.fetchall()
    # print (result)
    record_max = result[0][0]
    # print ('登録されている総レコード数 ==> ', record_max)
    return record_max+1



if __name__ == "__main__":
    input_url = "https://www.youtube.com/watch?v=n8cpqRJjumo"
    yt = get_yt_info(input_url)
    item_obj = dbvalue_urls(
                _id=get_next_id(),
                _rec_date = dt.today(),
                _rec_by = "Hayato",
                _title=yt["title"],
                _uri= input_url,
                _comment = "Just try when you have time!"
            )
    add_item(item_obj)
    
    # add_item(obj)
    # print(get_next_id())
    item = get_items()
    print(item)
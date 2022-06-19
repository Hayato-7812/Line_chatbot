from operator import getitem
import logging
from datetime import datetime as dt 
import psycopg2
import os

# DATABASE_URL = os.environ['DATABASE_URL']
DATABASE_URL = "postgres://kjzuxewitnsphz:44a69351639957534ac0f28bf0f16b24a6254a27c626b0a9faf3539df4a950d5@ec2-52-71-23-11.compute-1.amazonaws.com:5432/d93a1fm13467us"




LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.INFO)

class dbvalue_base():
    #self.attr[0] must be primary key
    def to_list(self):
        return [str(getattr(self,k)) for k in self.attr]
    def to_dict(self):
        return {k:str(getattr(self,k)) for k in self.attr}

class dbvalue_urls(dbvalue_base):
    def __init__(self,_id=-1,_rec_date="",_rec_by="",_title="",_uri="",_comment=""):
        self.id = _id
        self.rec_date = _rec_date
        self.rec_by = _rec_by
        self.title = _title
        self.uri = _uri
        self.comment = _comment
        self.attr= ["id","rec_date","rec_by","title","uri","comment"]
        self.table="F_MUSIC"

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
    cur.execute("INSERT INTO {} VALUES ({}, '{}','{}','{}','{}','{}')".format(obj.table,obj.id,obj.rec_date,obj.title,obj.rec_by,obj.uri,obj.comment))

@dbopen()
def get_data(conn,cur,tablename = "F_MUSIC"):
    sql = 'SELECT * FROM {}'.format(tablename)
    cur.execute(sql)

@dbopen()
def get_items(conn,cur,tablename="F_MUSIC"):  #as dict in list 
    # print("get db items")
    cur.execute("select * from {}".format(tablename))
    result = []
    for row in cur:
        # print("row:{}".format(row))
        result.append(dbvalue_urls(row[0],row[1],row[2],row[3],row[4],row[5]).to_dict())
    return result

@dbopen()
def get_next_id(conn,cur,tablename="F_MUSIC"):
    sql = 'SELECT count(*) FROM {}'.format(tablename)
    cur.execute(sql)
    result = cur.fetchall()
    # print (result)
    record_max = result[0][0]
    # print ('登録されている総レコード数 ==> ', record_max)
    return record_max+1



if __name__ == "__main__":
    # obj= dbvalue_urls(
    #         _id=3,
    #         _rec_date = dt.today(),
    #         _rec_by = "testman",
    #         _uri="https://www.youtube.com/watch?v=uAqITu9ypDo",
    #         _comment = "yeah!"
    #     )
    
    # add_item(obj)
    # print(get_next_id())
    item = get_items()[0]
    print("aaa")
import sqlite3
import random
import time

def create_sql():#创建数据库
    """
    创建数据库
    """
    sql = sqlite3.connect("userInformation.db")
    sql.execute(
        """create table if not exists
        %s(
        %s integer primary key autoincrement,
        %s varchar(128),
        %s varchar(128),
        %s varchar(128),
        %s varchar(128),
        %s varchar(128))"""
        % (
            "user",
            "NUM",
            "OPENID",
            "ID",
            "TIME",
            "CONTENT",
            "CONTINUOUSTIMES",
        ))
    sql.close()
    return sql

def generate_random_str(randomlength=3):
    """
    生成一个指定长度的随机字符串
    """
    random_str = ''
    base_str = 'ABCDEFGHIGKLMNOPQRSTUVWXYZabcdefghigklmnopqrstuvwxyz0123456789'
    length = len(base_str) - 1
    for i in range(randomlength):
        random_str += base_str[random.randint(0, length)]
    return random_str

def check_openId_exits(openId):
    sql = sqlite3.connect("userInformation.db")
    is_exits = sql.execute("select * from user where OPENID='%s'" % openId).fetchone()
    sql.close()
    return False if not is_exits else True

def check_id_exits(ID):
    sql = sqlite3.connect("userInformation.db")
    is_exits = sql.execute("select * from user where ID='%s'" % ID).fetchone()
    sql.close()
    return False if not is_exits else True

def select_id(openId):
    sql = sqlite3.connect("userInformation.db")
    ID = sql.execute("select ID from user where OPENID='%s'" % openId).fetchone()[0]
    sql.close()
    return ID

def update_content(content, openId):
    sql = sqlite3.connect("userInformation.db")
    sql.execute("update user set CONTENT = '%s' where OPENID = '%s'" % (content, openId))
    sql.commit()
    sql.close()

def update_time(openId):
    sql = sqlite3.connect("userInformation.db")
    sql.execute("update user set TIME = '%s' where OPENID = '%s'" % (int(time.time()), openId))
    sql.commit()
    sql.close()

def update_ID(openId):
    ID = generate_random_str(3)
    while check_id_exits(ID):
        ID = generate_random_str(3)
    sql = sqlite3.connect("userInformation.db")
    sql.execute("update user set ID = '%s' where OPENID = '%s'" % (ID, openId))
    sql.commit()
    sql.close()
    return ID

def select_content(openId):
    sql = sqlite3.connect("userInformation.db")
    content = sql.execute("select CONTENT from user where OPENID='%s'" % openId).fetchone()[0]
    sql.commit()
    sql.close()
    return content

def select_openId(ID):
    sql = sqlite3.connect("userInformation.db")
    openId = sql.execute("select OPENID from user where ID='%s'" % ID).fetchone()[0]
    sql.commit()
    sql.close()
    return openId

def select_time(openId):
    sql = sqlite3.connect("userInformation.db")
    times = sql.execute("select TIME from user where OPENID='%s'" % openId).fetchone()[0]
    sql.commit()
    sql.close()
    return times

def select_msg_times(openId):
    sql = sqlite3.connect("userInformation.db")
    times = sql.execute("select CONTINUOUSTIMES from user where OPENID='%s'" % openId).fetchone()[0]
    sql.commit()
    sql.close()
    return times

def create_correspond_id(openId):#创建对应ID
    ID = generate_random_str(3)
    while check_id_exits(ID):
        ID = generate_random_str(3)
    sql = sqlite3.connect("userInformation.db")
    sql.execute(
        "insert into user(OPENID, ID, TIME, CONTENT, CONTINUOUSTIMES) values(?,?,?,?,?)",
        (openId, ID, "", "", 0))
    sql.commit()
    sql.close()
    update_time(openId)
    return ID

def update_msg_times(openId):
    sql = sqlite3.connect("userInformation.db")
    times = sql.execute("select CONTINUOUSTIMES from user where OPENID='%s'" % openId).fetchone()[0]
    sql.execute("update user set CONTINUOUSTIMES = '%s' where OPENID = '%s'" % (int(times) + 1, openId))
    sql.commit()
    sql.close()

def reset_msg_times(openId):
    sql = sqlite3.connect("userInformation.db")
    sql.execute("update user set CONTINUOUSTIMES = '%s' where OPENID = '%s'" % (0, openId))
    sql.commit()
    sql.close()

def show_all_info():
    sql = sqlite3.connect("userInformation.db")
    info = sql.execute("select * from user " ).fetchall()
    sql.close()
    print(info)


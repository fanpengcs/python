#!/usr/bin/python
# -*- coding: UTF-8 -*-

import sys
import os
import MySQLdb
import time

def main():
    # 初始化日志
    path = os.path.abspath(os.path.dirname(__file__))
    type = sys.getfilesystemencoding()
    sys.stdout = Logger()
    print path, type
    
    # 打开数据库连接
    db = MySQLdb.connect("10.0.7.243", "root", "YhzJ=869", "ts_yhzj", charset='utf8')
    # 使用cursor()方法获取操作游标 
    cursor = db.cursor()

    sql = "select AccountId from globalaccountinfo00;"
    cursor.execute(sql)
    accountIds = cursor.fetchall()

    sql = "show tables;"
    cursor.execute(sql)
    tables = cursor.fetchall()

    times = 0;
    allt0 = time.time()
    for tb in tables:
        for acc in accountIds:
            times = times + 1
            try:
                sql = "select * from %s where AccountId = '%i';" %(tb[0], acc[0])
                t0 = time.time()
                cursor.execute(sql)
                results = cursor.fetchall()
                endtime = time.time() - t0
                print endtime, "seconds process time", results, tb[0], acc[0], times
            except Exception as e:
                print "Error: unable to fecth data :%s" % str(e), tb[0], acc[0], times
    print time.time() - allt0, "seconds process time", results, times

    # 关闭数据库连接
    db.close()

class Logger(object):
    def __init__(self, filename="fplog.txt"):
        self.terminal = sys.stdout
        self.log = open(filename, "a")

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)

    def flush(self):
        pass

if __name__ == "__main__":
    main()
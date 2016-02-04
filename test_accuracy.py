# -*- coding: utf-8 -*-
__author__ = 'hzdonghaoling'
import MySQLdb

# table label_sentiment_rst if is needed
def delete_table(db):
    cursor = db.cursor()
    sql_string_delete = """delete from label_sentiment_rst"""
    try:
        cursor.execute(sql_string_delete)
        db.commit()
    except:
        print "Delete Error"

def drop_table(db):
    cursor = db.cursor()
    sql_string_drop = """drop table label_sentiment_rst"""
    try:
        cursor.execute(sql_string_drop)
        db.commit()
    except:
        print "Drop Error"

def insert_into_table(db, task_id, ods_sentence_id, sentiment_rst, is_valid, is_contradict):
    cursor = db.cursor()
    sql_string_insert = """ insert into label_sentiment_rst (task_id, ods_sentence_id, sentiment_rst, is_valid, is_contradict) values ("%s","%s","%s","%s","%s") """
    data = (task_id, ods_sentence_id, sentiment_rst, is_valid, is_contradict)
    try:
        cursor.execute(sql_string_insert, data)
        db.commit()
    except:
        print "Insert Error"

def create_table(db):
    cursor = db.cursor()
    sql_string_create = """CREATE TABLE IF NOT EXISTS label_sentiment_rst(
        task_id BIGINT(11) NOT NULL,
        ods_sentence_id BIGINT(11) NOT NULL,
        sentiment_rst FLOAT NOT NULL,
        is_valid int(11),
        is_contradict int(11),
        is_irrelevent int(11),
        PRIMARY KEY(task_id, ods_sentence_id, sentiment_rst)
    );"""
    try:
        cursor.execute(sql_string_create)
        db.commit()
    except:
        print "Create Error"

db = MySQLdb.connect("223.252.211.186", "us_opinionmining", "wWCa5KqKhJnpbQSv", "us_opinion_mining")
#clear the table label_sentiment_rst to avoid repeated insert
drop_table(db)
cursor = db.cursor()
# 必须三个人的标注结果是一样的，才确定这条结果的sentiment, 并且保留这条结果。
# 如果三个人的标注结果都不一样，那么这条记录就被删除，否则记录添加到ground_truth
sql_string_sentiment = """SELECT * FROM label_ods_rst
    WHERE task_id IN
    (
    SELECT task_id FROM label_user_task
    WHERE is_finished = 1 GROUP BY task_id HAVING count(*) = 3
    )
    GROUP BY task_id, ods_sentence_id, sentiment
    HAVING COUNT(*) == 3 """
ground_truth = []
try:
    cursor.execute(sql_string_sentiment)
    results = cursor.fetchall()
    for i in range(0, len(results), 1):
        is_valid = 1
        is_contradict = 0
        if i == len(results)-1:
            if results[i][0] == results[i-1][0]:
                is_valid = 0
        else:
            if results[i][0] == results[i+1][0]:
                is_valid = 0
        task_id = results[i][1]
        ods_sentence_id = results[i][0]
        sentiment_rst = results[i][3]
        is_irrelevent = results[i][4]
        if results[i][4] == 1:
            is_valid = 0
        if sentiment_rst == 4:
            is_contradict = 1
        record = (task_id, ods_sentence_id, sentiment_rst, is_valid, is_contradict, is_irrelevent)
        ground_truth.append(record)
        #insert_into_table(db, task_id, ods_sentence_id, sentiment_rst, is_valid, is_contradict)
except:
    print "Get Data Error"
db.close()


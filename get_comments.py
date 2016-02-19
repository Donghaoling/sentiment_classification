# -*- coding: UTF-8 -*-
__author__ = 'hzdonghaoling'
import MySQLdb
import sys
import csv

def get_comments_three_differences(db):
    cursor = db.cursor()
    sql_string_select = """SELECT A.task_id, A.ods_sentence_id, B.content, B.src_content, B.concept_name, B.user_id, B.sentiment, B.is_irrelevent FROM
(
	SELECT
		*
	FROM
		(
			SELECT
				*
			FROM
				label_ods_rst
			WHERE
				task_id IN (
					/*return the task that three persons done*/
					SELECT
						task_id
					FROM
						label_user_task
					WHERE
						is_finished = 1
					GROUP BY
						task_id
					HAVING
						count(*) = 3
				)
			GROUP BY
				task_id,
				ods_sentence_id,
				sentiment,
				is_irrelevent
			HAVING
				COUNT(*) <= 2
		) C
	GROUP BY
		task_id,
		ods_sentence_id
	HAVING
		COUNT(*) = 3
) A
JOIN (
	SELECT
		src.task_id,
		src.ods_sentence_id,
		content,
		src_content,
		concept_name,
		T.sentiment,
		T.is_irrelevent,
		T.user_id
	FROM
		label_ods_src src
	JOIN (
		SELECT DISTINCT
			task_id,
			ods_sentence_id,
			sentiment,
			is_irrelevent,
			user_id
		FROM
			label_ods_rst
		WHERE
			task_id IN (
				/*return the task that three persons done*/
				SELECT
					task_id
				FROM
					label_user_task
				WHERE
					is_finished = 1
				GROUP BY
					task_id
				HAVING
					count(*) = 3
			) /*GROUP BY task_id, ods_sentence_id, sentiment*/
		GROUP BY
			task_id,
			ods_sentence_id,
			sentiment,
			is_irrelevent
		HAVING
			COUNT(*) <= 2
	) T ON src.task_id = T.task_id
	AND src.ods_sentence_id = T.ods_sentence_id
) B ON A.task_id = B.task_id
AND A.ods_sentence_id = B.ods_sentence_id"""
    try:
        cursor.execute(sql_string_select)
        results = cursor.fetchall() #现在是fetchone()来测试，之后别忘了改成fetchall()
        return results
    except:
        print "Get comment Error"

def get_comments_different(db):
    cursor = db.cursor()
    sql_string_select = """SELECT src.task_id, src.ods_sentence_id, content, src_content, concept_name, T.sentiment, T.is_irrelevent, T.user_id
FROM
	label_ods_src src
JOIN (
	SELECT DISTINCT
		task_id,
		ods_sentence_id,
		sentiment,
		is_irrelevent,
		user_id
	FROM
		label_ods_rst
	WHERE
		task_id IN (
			/*return the task that three persons done*/
			SELECT
				task_id
			FROM
				label_user_task
			WHERE
				is_finished = 1
			GROUP BY
				task_id
			HAVING
				count(*) = 3
		) /*GROUP BY task_id, ods_sentence_id, sentiment*/
	GROUP BY
		task_id,
		ods_sentence_id,
		sentiment,
		is_irrelevent
	HAVING
		COUNT(*) <= 2
) T ON src.task_id = T.task_id
AND src.ods_sentence_id = T.ods_sentence_id"""
    try:
        cursor.execute(sql_string_select)
        results = cursor.fetchall()
        return results
    except:
        print "Get comment Error"

db = MySQLdb.connect("223.252.211.186", "us_opinionmining", "wWCa5KqKhJnpbQSv", "us_opinion_mining", charset = "utf8")
results = get_comments_three_differences(db)
csvfile = file('E:\\requirement\\get_comments_three_differences.csv','wb')
writer = csv.writer(csvfile)
first_line = ('task_id', 'ods_sentence_id', 'content', 'content_src', 'concept_name', 'user_id', 'sentiment', 'is_irrelevent')
writer.writerow(first_line)
#按行写入csv文件
for item in results:
    #第3,4,5列是中文字符，要先encode成gbk编码再写入，windows是用gbk编码的，所以不要encode成utf8
    two = item[2].encode('gbk')
    three = item[3].encode('gbk')
    four = item[4].encode('gbk')
    string_csv = (item[0], item[1], two, three, four, item[5], item[6], item[7])
    writer.writerow(string_csv)
last_line = u"注：1，2，3，4分别是好评，中评，差评和矛盾，is_irrelevent = 0，1分别表示和主题无关，和主题有关"
last_line = last_line.encode('gbk')
#csvfile.write(last_line)
writer.writerow(last_line)
csvfile.close()

results = get_comments_different(db)
csvfile = file('E:\\requirement\\get_comments_different.csv','wb')
writer = csv.writer(csvfile)
first_line = ('task_id', 'ods_sentence_id', 'content', 'content_src', 'concept_name', 'sentiment', 'is_irrelevent', 'user_id')
writer.writerow(first_line)
for item in results:
    #第3,4,5列是中文字符，要先encode成gbk编码再写入，windows是用gbk编码的，所以不要encode成utf8
    two = item[2].encode('gbk')
    three = item[3].encode('gbk')
    four = item[4].encode('gbk')
    string_csv = (item[0], item[1], two, three, four, item[5], item[6], item[7])
    writer.writerow(string_csv)
last_line = u"注：sentiment = 1，2，3，4分别是好评，中评，差评和矛盾，is_irrelevent = 0，1分别表示和主题无关，和主题有关"
last_line = last_line.encode('gbk')
csvfile.write(last_line) #直接用csvfile.write而不是writer.writerow()来写最后一行，因为最后一行不需要csv格式，用writer.writerow()写会出错
csvfile.close()
db.close()
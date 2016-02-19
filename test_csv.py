# -*- coding: UTF-8 -*-
__author__ = 'hzdonghaoling'
import csv
csvfile = file('E:\\requirement\\test.csv','wb')
writer = csv.writer(csvfile)
s1 = u"啦啦啦"
s2 = u"烦烦烦"
s1 = s1.encode('gbk')
s2 = s2.encode('gbk')
first_line = (s1, s2)
#csvfile.write(first_line.encode('gbk'))
writer.writerow(first_line)
csvfile.close()
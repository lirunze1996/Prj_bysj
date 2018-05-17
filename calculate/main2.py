# -*- coding: utf-8 -*-

from snownlp import SnowNLP
import pandas as pd
import pylab as pl
import os
import MySQLdb as mysql

path = u'D:/bysj/data/'
files = os.listdir(path)

# conn = mysql.connect(host="127.0.0.1", user="arnold", passwd="a", db="mydatabase")
# cursor = conn.cursor()

for file in files:
    txt_path = path + file

    # 读取txt文件
    f = open(txt_path, 'r')
    text = f.readlines()

    count = len(text)
    f.close()
    sentences = []
    senti_score = []
    a = 0
    for i in text:
        a1 = SnowNLP(i.decode('utf-8'))
        a2 = a1.sentiments
        sentences.append(i)  # 语序...
        senti_score.append(a2)
        a = a + a2
    table = pd.DataFrame(sentences, senti_score)
    x = [i for i in range(1, count + 1)]

    name = file.split(".")[0]
    count = len(x)
    score = a / len(x)
    pl.mpl.rcParams['font.sans-serif'] = ['SimHei']
    cm = pl.cm.get_cmap('Dark2')
    # cm = pl.cm.get_cmap('Set1')
    # cm = pl.cm.get_cmap('Set2')
    sc = pl.scatter(x=x, y=senti_score, c=senti_score, s=7, cmap=cm)
    pl.colorbar(sc)
    pl.title(file.split(".")[0] + u'网评')
    pl.xlabel(u'评论用户')
    pl.ylabel(u'情感程度')
    # pl.show()
    pl.savefig(u'D:/bysj/result/sentiment/' + file.replace("txt", "png"))
    pl.close()

#     conn.set_character_set('utf8')
#     cursor.execute('SET NAMES utf8;')
#     cursor.execute('SET CHARACTER SET utf8;')
#     cursor.execute('SET character_set_connection=utf8;')
#
#
#     print name, count, score
#     cursor.execute("insert into movie(name, count, score) values('%s', %s, %s)" % (name, count, score,))
#     conn.commit()
#     print 'success'
#
# cursor.close()
# conn.close()

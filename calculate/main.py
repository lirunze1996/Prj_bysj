# -*- coding: utf-8 -*-
import os
import os.path
import jieba
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from scipy.misc import imread

path = u'D:/bysj/data/'
files = os.listdir(path)

for file in files:
    txt_path = path + file

    # 读取txt文件
    content = open(txt_path, 'r').read()
    # 使用Jieba进行分词
    cut_text = " ".join(jieba.cut(content, cut_all=False))
    # 字体
    font = r'D:/bysj/font/simfang.ttf'
    # 背景图片路径
    backgroud = imread("D:/bysj/image/3.jpg")
    # 停用词
    stopwords = {}.fromkeys([line.rstrip() for line in open('D:/bysj/stopword/stopword.txt')])

    final = ''
    for seg in cut_text:
        seg = seg.encode("utf-8")
        if seg not in stopwords:
            final += seg

    cut_text2 = " ".join(jieba.cut(final, cut_all=False))

    # 词云准备
    cloud = WordCloud(
        max_words=1000,
        background_color="white",
        mask=backgroud,
        font_path=font,
        width=1000,
        height=860,
        margin=2)

    # 生成词云
    word_cloud = cloud.generate(cut_text2)

    # 显示词云
    plt.imshow(word_cloud)
    plt.axis("off")
    # plt.show()
    cloud.to_file(u'D:/bysj/result/worldcloud/' + file.replace("txt", "png"))

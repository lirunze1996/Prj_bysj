# -*- coding: utf-8 -*-
import os
import sys, time
import pytesseract
from selenium import webdriver
from PIL import Image, ImageEnhance
from chaojiying import Chaojiying_Client


class Crawler(object):
    def __init__(self):
        self.driver = webdriver.Chrome(executable_path="chromedriver.exe")  # 驱动
        self.username = ""  # 豆瓣用户名
        self.pwd = ""  # 密码
        self.login_url = "https://accounts.douban.com/login"  # 豆瓣登录url
        self.base_url = "https://movie.douban.com/"  # 豆瓣主页
        self.dir = "D:/bysj/data/"  # 爬取的数据存放的目录
        self.cjy = Chaojiying_Client('', '', '')  # 超级鹰验证码识别接口
        self.verify_image = 'D:/bysj/VerifcationImage/1.png'  # 处理前的验证码图片地址
        self.result_image = 'D:/bysj/VerifcationImage/2.png'  # 处理后的验证码图片地址

    def do_login(self):
        self.driver.get(self.login_url)

        try:
            # 判断是否有验证码
            img_url = self.driver.find_element_by_xpath('//*[@id="captcha_image"]').get_attribute("src")
            self.driver.get(img_url)
            self.driver.get_screenshot_as_file(self.verify_image)  # 截图保存
            self.driver.back()

            code = self.getCode(self.verify_image)  # 获取验证码

            captcha = self.driver.find_element_by_xpath('//*[@id="captcha_field"]')
            captcha.send_keys(code)
        except Exception, e:
            pass

        username = self.driver.find_element_by_xpath('//*[@id="email"]')
        username.send_keys(self.username)
        pwd = self.driver.find_element_by_xpath('//*[@id="password"]')
        pwd.send_keys(self.pwd)

        submit = self.driver.find_element_by_name('login')
        # find_element_by_xpath('//*[@id="lzform"]/div[6]/input')
        submit.click()

    def getCode(self, imagePath):
        im_origin = Image.open(imagePath)
        box = (392, 268, 643, 308)
        im_region = im_origin.crop(box)  # 截取部分区域
        im_region.convert('L')  # 图像加强，二值化
        sharpness = ImageEnhance.Contrast(im_region)  # 对比度加强
        im_result = sharpness.enhance(2.0)  # 增加饱和度
        im_result.save(self.result_image)  # 保存处理后的验证码图片
        time.sleep(2)
        # 开始识别验证码
        im = open(self.result_image, 'rb').read()
        dict = self.cjy.PostPic(im, 1902)
        code = dict['pic_str'].strip()
        return code

    def parse_by_ocr(self):
        im = Image.open("D:/bysj/22.png")
        imgry = im.convert('L')  # 图像加强，二值化
        sharpness = ImageEnhance.Contrast(imgry)  # 对比度增强
        sharp_img = sharpness.enhance(2.0)
        sharp_img.save("D:/bysj/222.png")
        i2 = Image.open(r'D:/bysj/222.png')
        i2.convert('L')
        i2 = ImageEnhance.Contrast(i2)  # 增强对比度
        i2 = i2.enhance(2.0)  # 增加饱和度
        i2.save(r'D:/bysj/2222.png')

        i3 = Image.open(r'D:/bysj/ttt.png')
        text = pytesseract.image_to_string(i3).strip()
        print text

    def get_movies_url(self):
        self.driver.get(self.base_url)
        list = self.driver.find_elements_by_xpath('//*[@id="screening"]/div[2]/ul/li')
        length = len(list)
        dict = {}
        for i in range(0, length):
            list = self.driver.find_element_by_xpath('//*[@id="screening"]/div[2]/ul').find_elements_by_class_name(
                "ui-slide-item")
            if list[i].get_attribute("data-title") is not None:
                movie_name = list[i].get_attribute("data-title").strip()
                movie_url = list[i].find_element_by_class_name("poster").find_element_by_tag_name("a").get_attribute(
                    "href")

                # 去详情页查找影评的url
                self.driver.get(movie_url)
                comment_url = self.driver.find_element_by_xpath(
                    '//*[@id="comments-section"]/div[1]/h2/span/a').get_attribute("href")

                # 构造dict
                if movie_name not in dict:
                    dict.update({movie_name: comment_url})

                # 返回父页面
                self.driver.back()
        return dict

    def get_comment(self, dict):
        if dict is not None and len(dict) > 0:
            for k, v in dict.items():
                file_path = self.dir + unicode(k.replace(":", "") + ".txt")
                file = open(file_path, "a")

                # 获取评论
                base_comment_url = v[0:v.find("?") + 1]
                # 分页获取
                for i in range(0, 25):
                    url = base_comment_url + "start=" + str(i * 20) + "&limit=20&sort=new_score&status=P&percent_type="
                    self.driver.get(url)
                    try:
                        comments = self.driver.find_element_by_xpath('//*[@id="comments"]').find_elements_by_class_name(
                            "comment-item")
                        for item in comments:
                            content = item.find_element_by_tag_name("p").text
                            file.write(content + "\n")
                    except Exception, e:
                        break
                        pass
                file.close()


if __name__ == "__main__":
    reload(sys)
    sys.setdefaultencoding('utf-8')

    crawler = Crawler()
    crawler.do_login()
    dict = crawler.get_movies_url()
    crawler.get_comment(dict)

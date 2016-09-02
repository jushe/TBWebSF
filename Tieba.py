import math
import re

import requests


class Tieba:
    def __init__(self):

        #用于代码内需要的数据
        self.url = ""
        self.source = ""
        self.id = ""
        self.pageNum = 0
        self.starNum = 0
        self.themes = []
        #可能会用到的数据，暂不获取
        self.name = ""
        self.comment = ""
        self.classfication = ""
        self.themeNum = 0
        self.postNum = 0 #帖子数

    def init_data(self, url):
        """
        Before you start to use the Tieba class, you need to init it
        :param url: the Tieba's url
        :return:
        """
        r = requests.get(url)
        result = re.findall(re.compile(r'共有主题数<span class="red_text">' + "(\d+)" + r"</span>个"), r.text)
        self.themeNum = int(result[0])

        self.pageNum = int(math.ceil(self.themeNum / 50.0))

        result = re.findall(re.compile(r'"forum_id":' + "(\d+)" + r','), r.text)
        self.id = str(result[0])

        for page in range(self.pageNum):
            try:
                r = requests.get(url + '&pn=' + str(page * 50))
                self.source += r.text
            except ConnectionError as e:
                print(e)
        self.url = url

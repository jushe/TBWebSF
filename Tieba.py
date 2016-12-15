import math
import re

import requests


class Tieba:
    def __init__(self):

        # 用于代码内需要的数据
        self.url = ""  # 贴吧本身的url
        self.id = ""  # 贴吧id（百度所给出的id)
        self.pageNum = 0  # 贴吧页数（由主题/50）计算得出
        self.themes = []  # 贴吧的主题的url
        # 可能会用到的数据，暂不获取
        self.starNum = 0
        self.name = ""
        self.comment = ""
        self.classfication = ""
        self.themeNum = 0
        self.postNum = 0  # 帖子数

    def init_data(self, url):
        """
        Before you start to use the Tieba class, you need to init it
        :param url: the Tieba's url
        :return:
        """
        source = ""
        r = requests.get(url)
        result = re.findall(re.compile(r'共有主题数<span class="red_text">' + "(\d+)" + r"</span>个"), r.text)
        self.themeNum = int(result[0])

        self.pageNum = int(math.ceil(self.themeNum / 50.0))

        result = re.findall(re.compile(r'"forum_id":' + "(\d+)" + r','), r.text)
        self.id = str(result[0])

        """获取贴吧的源代码"""
        for page in range(self.pageNum):
            try:
                r = requests.get(url + '&pn=' + str(page * 50))
                source += r.text
            except ConnectionError as e:
                print(e)

        result = re.findall(re.compile(r'<a href="/p/(\d+)" title="'), source)
        for res in result:
            self.themes.append("http://tieba.baidu.com/p/" + str(res))

        self.url = url

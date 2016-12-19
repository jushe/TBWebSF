import json
import re
import time

import requests


class Theme:
    def __init__(self):
        # 帖子内置所需要的数据
        self.url = ""  # 主题url
        self.title = ""  # 主题标题
        self.content = []  # 主题内容(每层内容及其中楼主的回复)
        self.pageNum = 0  # 帖子页数
        self.tid = ""  # 帖子id
        self.source = ""  # 帖子源
        self.fid = ""  # 所属贴吧id
        self.userId = ""  # 楼主id
        self.status = 0  # 获取状态
        # 帖子内，关于小说的数据
        self.urlList = []  # 若为整合贴，则其内将存有各个章节或者小说的url
        self.sfTitle = ""  # 若为小说贴，则该值为该小说/章节标题（帖子标题）
        self.sfContent = ""  # 若为小说贴，则该值为小说具体内容
        self.sfTranslator = ""  # 若为小说贴，则该值为章节翻译者

    def init_data(self, url, fid, see_lz=1):

        result = re.findall(r"http://tieba.baidu.com/p/" + "(\d+)", url)
        self.tid = str(result[0])
        self.fid = str(fid)
        r = requests.get(url)
        if r.status_code == requests.codes.ok:
            result = re.findall(r"<title>" + "(.*?)" + "</title>", r.text)
            if result[0] != '贴吧404':
                self.status = 1
                result = re.findall(r'共<span class="red">' + "(\d+?)" + r'</span>页</li>', r.text)
                self.pageNum = int(result[0])

                result = re.findall(r'title: "' + r"(.*?)" + r'"', r.text)
                self.title = result[0]
                self.title = self.title.replace(' ', '')  # 去除标题内的空格防止非法命名

                result = re.findall(r'<li class="d_name" data-field=\'\{&quot;user_id&quot;:' + "(\d+?)" + r"}'>",
                                    r.text)
                self.userId = result[0]

                result = re.findall(r'author: "' + "(.*?)" + r'",', r.text)
                self.sfTranslator = result[0]

                if see_lz == 1:
                    """获取主题的源代码(只看楼主)"""
                    for page in range(self.pageNum):
                        try:
                            r = requests.get(url + '?pn=' + str(page + 1) + r'&see_lz=1')
                            self.source += r.text
                        except ConnectionError as e:
                            print(e)
                else:
                    """获取主题源代码(全部)"""
                    for page in range(self.pageNum):
                        try:
                            r = requests.get(url + '?pn=' + str(page + 1))
                            self.source += r.text
                        except ConnectionError as e:
                            print(e)

                result = re.findall(r'class="d_post_content j_d_post_content ">' + "(.*?)" + r'</div>', self.source)

                # 内容修正（res内含有一些带有超链接的内容）
                for res in result:
                    s = res
                    rex = re.compile(r"<a" + "(.*?)" + ">")
                    s = rex.sub('', s)  # 移除超链接
                    rex = re.compile(r"</a>")
                    s = rex.sub('', s)  # 移除超链接尾部
                    rex = re.compile(r"<br>")
                    s = rex.sub("\n", s)  # 移除<br>并替换为原来的换行
                    rex = re.compile(r"<img" + "(.*?)" + ">")
                    s = rex.sub('', s)  # 移除图片链接

                    self.content.append(s)

                # 获取帖子每页的回复
                if see_lz == 1:
                    for page in range(self.pageNum):
                        r = requests.get(
                            r"http://tieba.baidu.com/p/totalComment?t=" + str(int(time.time() * 1000)) + r"&tid="
                            + self.tid + r"&fid=" + self.fid + r'&pn=' + str(page + 1) + r'&see_lz=1')
                        json_result = json.loads(r.text)
                        if len(json_result['data']['comment_list']) > 0:  # 当存在回复贴（楼中楼）时
                            for (comment, index) in zip(sorted(json_result['data']['comment_list'].keys()),
                                                        range(len(json_result['data']['comment_list'].keys()))):
                                for floor in json_result['data']['comment_list'][comment]['comment_info']:
                                    if floor['user_id'] == self.userId:
                                        if len(self.content) > index + 1:
                                            self.content[index + 1] += ("\n" + floor['content'] + "\n")
                else:
                    for page in range(self.pageNum):
                        r = requests.get(
                            r"http://tieba.baidu.com/p/totalComment?t=" + str(int(time.time() * 1000)) + r"&tid="
                            + self.tid + r"&fid=" + self.fid + r'&pn=' + str(page + 1))
                        json_result = json.loads(r.text)
                        if len(json_result['data']['comment_list']) > 0:  # 当存在回复贴（楼中楼）时
                            for (comment, index) in zip(sorted(json_result['data']['comment_list'].keys()),
                                                        range(len(json_result['data']['comment_list'].keys()))):
                                for floor in json_result['data']['comment_list'][comment]['comment_info']:
                                    if floor['user_id'] == self.userId:
                                        if len(self.content) > index + 1:
                                            self.content[index + 1] += ("\n" + floor['content'] + "\n")
                self.url = url

    def get_tb_address(self):
        for con in self.content:
            result = re.findall(r'貼吧地址： ' + "(.*?)" + '\n', con)
            if len(result) != 0:
                for u in result:
                    self.urlList.append(u)
        return self.urlList

    def get_sf_address(self):
        for con in self.content:
            result = re.findall(r"http://tieba.baidu.com/p/" + "(\d+)", con)
            for res in result:
                self.urlList.append(r"http://tieba.baidu.com/p/" + res)
        return self.urlList

    def get_content(self):
        for con in self.content:
            self.sfContent += con
        return self.sfContent

    @staticmethod
    def pre_title(url):
        r = requests.get(url)
        result = re.findall(r'title: "' + r"(.*?)" + r'"', r.text)
        return result[0]

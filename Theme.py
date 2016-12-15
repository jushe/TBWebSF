import json
import re
import time

import requests


class Theme:
    def __init__(self):
        # 帖子内置所需要的数据
        self.url = ""  # 主题url
        self.title = ""  # 主题标题
        self.content = []  # 主题内容(每层内容及其回复)
        self.pageNum = 0  # 帖子页数
        self.tid = ""  # 帖子id
        self.source = ""  # 帖子源
        self.fid = ""  # 所属贴吧id
        self.userId = ""  # 楼主id

        # 帖子内，关于小说的数据
        self.urlList = []  # 若为整合贴，则其内将存有各个章节或者小说的url
        self.sfTitle = ""  # 若为小说贴，则该值为该小说/章节标题（帖子标题）
        self.sfContent = ""  # 若为小说贴，则该值为小说具体内容
        self.sfTranslator = ""  # 若为小说贴，则该值为章节翻译者

    def init_data(self, url, tid, fid):

        self.tid = tid
        self.fid = fid
        r = requests.get(url)

        result = re.findall(r'共<span class="red">' + "(\d+?)" + r'</span>页</li>', r.text)
        self.pageNum = int(result[0])

        result = re.findall(r'title: "' + r"(.*?)" + r'"', r.text)
        self.title = result[0]

        result = re.findall(r'<li class="d_name" data-field=\'\{&quot;user_id&quot;:' + "(\d+?)" + r"}'>", r.text)
        self.userId = result[0]

        """获取主题的源代码(一般只看楼主)"""
        for page in range(self.pageNum):
            try:
                r = requests.get(url + '?pn=' + str(page + 1) + r'&see_lz=1')
                self.source += r.text
            except ConnectionError as e:
                print(e)

        result = re.findall(r'class="d_post_content j_d_post_content ">' + "(.*?)" + r'</div>', self.source)

        # 内容修正（res内含有一些带有超链接的内容）
        for res in result:
            rex = re.compile(r"<a" + "(.*?)" + "</a>")
            s = rex.sub('', res)  # 移除超链接
            rex = re.compile(r"<br>")
            t = rex.sub("\r\n", s)  # 移除<br>并替换为原来的换行
            self.content.append(t)
        for page in range(self.pageNum):
            r = requests.get(r"http://tieba.baidu.com/p/totalComment?t=" + str(int(time.time() * 1000)) + r"&tid="
                             + self.tid + r"&fid=" + self.fid + r'&pn=' + str(page + 1))
            json_result = json.loads(r.text)
            for (comment, index) in zip(sorted(json_result['data']['comment_list'].keys()),
                                        range(len(json_result['data']['comment_list'].keys()))):
                for floor in json_result['data']['comment_list'][comment]['comment_info']:
                    if floor['user_id'] == self.userId:
                        self.content[index + 1] += ("\r\n" + floor['content'] + "\r\n")
                print(self.content[index + 1])

        self.url = url

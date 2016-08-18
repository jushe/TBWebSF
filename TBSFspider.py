import re

import requests


class TBSFspider:
    """
    贴吧轻小说爬虫
    提供功能：
    1. 爬取整个页面
    2. 从爬取的页面中提取url
    3. 从爬取页面中提取小说内容
    """
    def __init__(self):
        self.content = ""
        self.num = 0
        self.allurl = []

    def getContentInTheme(self, url):
        """
        This function will get the whole page from TB's Theme,
        and it will restore the text to @content
        @return: the @content
        @url: the url you need
        """

        TBSFspider.getTheNumOfPageForTheme(self, url)

        i = 0
        while(True):
            i += 1
            if i > self.num:
                break #get the whole page
            try:
                r = requests.get(url + '?pn=' + str(i))
                self.content += r.text
            except ConnectionError as e:
                if r.status_code == 404:
                    break #the page is not exists
                else:
                    print (e)

    def getContentInTB(self, url):
        """
          This function will get the whole page from a TB,
          and it will restore the text to @content
          @return: the @content
          @url: the url you need
          """
        self.getTheNumOfThemesForTB(url)
        while(self.num > 0):
            page = 0
            try:
                r = requests.get(url + '&pn=' + str(page))
                self.content = r.text
                self.num -= 50
                page += 50
            except ConnectionError as e:
                print(e)

    def getContentWithFeedback(self, url):
        pass
            
    def getContentByPattern(self, beginString = r'貼吧地址： <a href="'+ '(.*)' + r'"  target="_blank">', endString = '</a><br>書籍化：', index = 1):
        """
        This function will catch the string between begin and end in the self.content
        It will get the index of tieba defaultly
        Becareful: It will not check the url
         
        @beginString: the begin string
        @endString: the end string
        @index: if there are other pattern in the begin or end, you can use it to match you want(or you should input 0)
        """

        pattern = re.compile( beginString + '(.*)' + endString)
        allText = re.findall(pattern, self.content)
        for url in allText:
            self.allurl.append(url[index])
        return self.allurl

    def clearData(self):
        self.content = ""
        self.num = 0
        self.allurl = []

    #def getTheSFContent(self)

    def getTheNumOfPageForTheme(self, url):
        r = requests.get(url)
        nums = re.findall(r'共<span class="red">' + '(.*)' + r'</span>页</li>', r.text)
        self.num = int(nums[0])

    def getTheNumOfThemesForTB(self, url):
        r = requests.get(url)
        nums = re.findall(r'共有主题数<span class="red_text">' + '(.*)' + r'</span>个', r.text)
        self.num = int(nums[0])

if __name__ == '__main__':

    s = TBSFspider()
    s.getContentInTheme("http://tieba.baidu.com/p/4295900106")
    url_list = s.getContentByPattern()
    for url in url_list:
        print (url)
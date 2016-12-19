import os
import re

import Theme
import Tieba


def validate_title(title):
    rstr = r"[\/\\\:\*\?\"\<\>\|]"  # '/\:*?"<>|'
    new_title = re.sub(rstr, "", title)
    return new_title


if __name__ == "__main__":
    source = r"http://tieba.baidu.com/p/4295900106"
    source_theme = Theme.Theme()
    source_theme.init_data(source, 12113791)

    tb_list = source_theme.get_tb_address()
    num = 0
    cur_path = os.getcwd()
    for tb in tb_list:
        if re.match(r'^http:/{2}\w.+$', tb):  # url有效时
            t = Tieba.Tieba()  # 小说贴吧进入
            t.init_data(tb)
            print("开始写入贴吧： " + t.name + '\n')
            path = cur_path + "\\sf\\" + t.name
            if not os.path.exists(path):
                os.makedirs(path)  # 为该小说建立目录
                """此处开始为测试用，实际使用时，应该为已经建立目录的还要继续爬"""
                theme = Theme.Theme()
                if len(t.index_themes) > 0:  # 尝试进入整合贴
                    u_t, i_t = t.index_themes[0]
                    theme.init_data(u_t, t.id, see_lz=0)  # 整合贴内关闭仅楼主
                    if theme.status == 1:  # 当且仅当存在该帖子时写入文件(status默认为0)
                        for f in theme.get_sf_address():  # 尝试进入各个小说章节
                            sf = Theme.Theme()
                            sf.init_data(f, t.id, see_lz=1)
                            sf_title = validate_title(sf.title)
                            if not os.path.isfile(path + "\\" + sf_title + ".txt"):  # 查看是否已经下载该章节
                                f = open(path + "\\" + sf_title + ".txt", "w", errors='ignore')  # 为该章节建立一个文件
                                f.write(sf.get_content())  # 写入小说内容
                                f.close()
                                # print("已经写入小说: " + t.name + "章节： " + sf.title + "\n")
            print("已经写入该贴吧: " + t.name + '\n')

import TBSFspider

TBlist = []
TBSFIndexList = []

s = TBSFspider.TBSFspider()
s.getContent("http://tieba.baidu.com/p/4295900106")
TBlist = s.getContentByPattern()

for tb in TBlist:
    s.clearData()
    s.getContent(tb)
    TBSFIndexList.append("tieba.baidu.com" + s.getContentByPattern(r'<a href="', '" title="(.*)整合(.*)', 0)[0])

print(TBSFIndexList)




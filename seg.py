#encoding=utf-8  
import jieba  
  
def cut(s):
    seg_list = list(jieba.cut(s, cut_all = True))
    return '/'.join(seg_list)
    # return seg_list

# seg_list = jieba.cut("我来到北京清华大学",cut_all=True)

# seg_list = jieba.cut("我来到北京清华大学",cut_all=False)
# print "Default Mode:", "/ ".join(seg_list) #默认模式

# seg_list = jieba.cut("他来到了网易杭研大厦")
# print ", ".join(seg_list)

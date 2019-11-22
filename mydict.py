'''
@Descripttion: some behavior about the dictionary of comments
@version: 1.0
@Author: mopin1
@Date: 2019-11-12 21:37:28
@LastEditTime: 2019-11-22 20:58:20
@Coding: UTF-8
'''

import jieba.posseg
import winreg
from pyecharts import options as opts
from pyecharts.charts import Page, WordCloud
from pyecharts.globals import SymbolType

class mydict:

	'''生成空字典'''
	def __init__(self):
		self.comment_dictionary={}
		self.comment_numbers=50
	
	'''对评论精确拆分，生成列表，并保留其中的形容词，返回列表'''
	def divide_commint(self,str_comments):
		comments=jieba.posseg.cut(str_comments)
		list_comment=[]
		for comment in comments:
			if (comment.flag=='a' or comment.flag=='ad' or comment.flag=='an' or comment.flag=='ag' or comment.flag=='al') and len(comment.word)>1:
				list_comment.append(comment.word)
		return list_comment
		
	'''将评论列表中关键词添加到字典comment_dictionariy中'''
	def add_into_comment_dictionary(self,list_comment):
		for comment in list_comment:
			if comment in self.comment_dictionary:
				self.comment_dictionary[comment]+=1
			else:
				self.comment_dictionary[comment]=1

	'''对评论字典按照频度从大到小排序，并取前20个高频词'''
	def sort_dictionary(self):
		dictionary=self.comment_dictionary
		after_sort_dictionary= dict(sorted(dictionary.items(), key=lambda d:d[1], reverse = True))
		new_dictionary=zip([i for i in after_sort_dictionary.keys()][:self.comment_numbers],[i for i in after_sort_dictionary.values()][:self.comment_numbers])
		return new_dictionary
	
	def get_desktop(self):#获取桌面路径
		key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,r'Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders')
		return winreg.QueryValueEx(key, "Desktop")[0]

	'''绘出前20个高频词的柱状图'''
	def draw_dictionary(self,dictionary):
		dictionary=self.sort_dictionary()
		c = (
			WordCloud()
			.add("", dictionary, word_size_range=[20, 100])
			.set_global_opts(title_opts=opts.TitleOpts(title="HUAWEIP30评论高频词"))
		)
		WordCloud.render(c,self.get_desktop()+"\\jd.huaweiP30.comments.html")
		return True
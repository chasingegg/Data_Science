# -*- coding:utf-8 -*-

#Let's get the douban top 150 movies

import re
import string
import urllib2

class Douban(object):

	def __init__(self):
		self.page = 1
		self.cur_url = "http://movie.douban.com/top250?start={page}&filter=&type="
		self.data = []
		self.top_num = 1
		print("prepare to catch the data...")

	def get_page(self, cur_page):
		url = self.cur_url
		try:
			my_page = urllib2.urlopen(url.format(page = (cur_page - 1) * 25)).read().decode("utf-8")
		except urllib2.URLError, e:
			if hasattr(e, "code"):
				print("the server couldn't fulfill the request.")
				print("Error code: %s" %e.code)
			elif hasattr(e, "reason"):
				print("we fail to reach a server.")
				print("Reason: %s" %e.reason)
		return my_page

	def find_title(self, my_page):
		tmp = []
		movie = re.findall(r'<span.*?class="title">(.*?)</span>', my_page, re.S)
		for index, item in enumerate(movie):
			#print(item)
			if item.find("&nbsp") == -1:
				tmp.append("Top" + str(self.top_num) + " " + item)
				self.top_num += 1
		self.data.extend(tmp)

	def start_spider(self):
		while self.page <= 6:
			my_page = self.get_page(self.page)
			self.find_title(my_page)
			self.page += 1

def main():
	print("come on a simple spider on douban movies\n")
	s = Douban()
	s.start_spider()
	for item in s.data:
		print(item)
	print("crawler end!")

if __name__ == "__main__":
	main()

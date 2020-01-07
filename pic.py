import urllib as UL
import urllib.request
from bs4 import BeautifulSoup
import re
import random
import os
from retrying import retry
import socket #比urlretrieve快且稳定

def agent_select():

	user_agent_list = [
		# "Mozilla/5.0(Macintosh;IntelMacOSX10.6;rv:2.0.1)Gecko/20100101Firefox/4.0.1",
		"Mozilla/4.0(compatible;MSIE6.0;WindowsNT5.1)",
		"Opera/9.80(WindowsNT6.1;U;en)Presto/2.8.131Version/11.11",
		"Mozilla/5.0(Macintosh;IntelMacOSX10_7_0)AppleWebKit/535.11(KHTML,likeGecko)Chrome/17.0.963.56Safari/535.11",
		"Mozilla/4.0(compatible;MSIE7.0;WindowsNT5.1)",
		"Mozilla/4.0(compatible;MSIE7.0;WindowsNT5.1;Trident/4.0;SE2.XMetaSr1.0;SE2.XMetaSr1.0;.NETCLR2.0.50727;SE2.XMetaSr1.0)"
	]

	header={
		"User-Agent":random.choice(user_agent_list)
	}
	print("%s selected" % header )
	return header

# @retry(stop_max_attempt_number=5, wait_fixed=2000) #这个装饰器很好的处理了request经常超时的问题，下同urlretrieve
# def request_url(url,timeout=20, num_retries=5):
def request_url(url, num_retries=5):
	socket.setdefaulttimeout(30)
	print(url)
	try:
		request = UL.request.Request(url, None, agent_select())
		response = UL.request.urlopen(request)
		if response.getcode() == 200:
			response.encoding = 'utf-8'
			data = response.read()
			data = data.decode('utf-8','ignore').replace(u'\xa9', u'').replace(u'\xae', u'')
			response.close()
		else: #处理ConnectionResetError: [WinError 10054] 远程主机强迫关闭了一个现有的连接。 服务器认为是dos攻击
			time.sleep(2)
			if num_retries > 0:
				return request_url(url, num_retries-1)
			else:
				fail_list.append(str(i))
				print("request failed")
				return 'failed'
	except socket.timeout:
		time.sleep(2)
		if num_retries > 0:
			return request_url(url, num_retries-1)
		else:
			fail_list.append(str(i))
			print("request failed")
			return 'failed'
	print("request finished")
	return data

def find_pic(source):
	url = re.findall(r'src="(.+?\.jpg)"',source) #图片资源正则表达式
	print("pic url ready")
	return url

#@retry(stop_max_attempt_number=5, wait_fixed=2000)
def download_all_pic(url, dir, num_retries=2):
	# global i
	socket.setdefaulttimeout(30)
	for j in url:
		try:
			UL.request.urlretrieve(j, dir + str(i) + ".jpg")
		except socket.timeout:
			if num_retries > 0:
				return download_all_pic( url,dir,num_retries-1)
			else:
				fail_list.append(str(i))
				print("download failed")
	print(str(j), "finished")

def check(dir):
	socket.setdefaulttimeout(30)
	for n in range(start_page, end_page):
		if os.path.exists('%s\\%s.jpg' % (dir,n)) == False:
			try:
				html_code = request_url("https://www.manhuadb.com/manhua/384/5144_85938_p%s.html" % n)
			except socket.timeout:
				print('%s.jpg failed' % str(n))
				continue
		else:
			continue

def _main_(start_page, end_page):
	global i
	for i in range(start_page, end_page):
		url_ture = ''.join(['https://www.manhuadb.com/manhua/384/5144_85938_p', str(i), '.html'])
		html_code = request_url(url_ture)
		if html_code == 'failed':
			continue
		pic_url = find_pic(html_code)
		download_all_pic(pic_url,'D:\\project\\ML\\webspider\\anhei\\1\\')
		print(fail_list)


fail_list = []
start = 36
end = 202
_main_(start, end)
check('D:\\project\\ML\\webspider\\anhei\\1')



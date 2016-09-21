import urllib2
from urllib2 import urlopen
from link_finder import LinkFinder
from general import *

class Spider:
	"""docstring for Spider"""

	projectname = ''
	base_url = ''
	domain_name = ''
	queue_file = ''
	crawled_file = ''
	queue = set()
	crawled = set()


	def __init__(self,projectname,base_url,domain_name):
		# self.arg = argc
		Spider.projectname = projectname
		Spider.base_url = base_url
		Spider.domain_name = domain_name
		Spider.queue_file = Spider.projectname + '/queue.txt'
		Spider.crawled_file = Spider.projectname + '/crawled.txt'
		self.boot()
		self.crawl_page('First Spider',Spider.base_url)

	@staticmethod
	def boot():
		create_project_dir(Spider.projectname)
		create_data_files(Spider.projectname,Spider.base_url)
		Spider.queue = file_to_set(Spider.queue_file)
		Spider.crawled = file_to_set(Spider.crawled_file)	


	@staticmethod
	def crawl_page(thread_name,page_url):
		if page_url not in Spider.crawled:
			print thread_name,'crawling',page_url
			print('Queue '+str(len(Spider.queue)) + ' | Crawled ' + str(len(Spider.crawled)))
			Spider.add_links_to_queue(Spider.gather_links(page_url))
			Spider.queue.remove(page_url)
			Spider.crawled.add(page_url)
			Spider.update_files()


	@staticmethod
	def gather_links(page_url):
		html_string = ''
		try:
			request = urllib2.Request(page_url)
			response = urllib2.urlopen(request)
			# response = urllib2.urlopen(page_url)
			print response.info().getheader('Content-Type')
			if response.info().getheader('Content-Type').startswith('text/html'):

				html_bytes = response.read()
				html_string = html_bytes.decode('utf-8')
			finder = LinkFinder(Spider.base_url,page_url)
			finder.feed(html_string)
		except Exception,err:
			# print('Error: cannot crawl page')
			print Exception,err
			return set()
		return finder.page_links()

	@staticmethod
	def add_links_to_queue(links):
		for url in links:
			if url in Spider.queue:
				continue
			if url in Spider.crawled:
				continue
			if Spider.domain_name not in url:
				continue
			Spider.queue.add(url)

	@staticmethod
	def update_files():
		set_to_file(Spider.queue,Spider.queue_file)
		set_to_file(Spider.crawled,Spider.crawled_file)


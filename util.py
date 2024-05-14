import requests
from bs4 import BeautifulSoup
from collections import namedtuple
MemeEntry = namedtuple('MemeEntry', ('url', 'title', 'timestamp'))

class Page:
	def __init__(self, url: str, session: requests.Session = None) -> None:
		self.url = url
		self.page = session.get(self.url, headers={ 'User-Agent': '' }) if session else requests.get(self.url, headers={ 'User-Agent': '' })
		if self.page.status_code != 200 or '提示信息' in self.page.text:
			raise Exception(f'Invalid response from server for url: {url}')
		self.soup = BeautifulSoup(self.page.text, 'html.parser')

	def __repr__(self) -> str:
		return f'<Page for url: {self.url}>'
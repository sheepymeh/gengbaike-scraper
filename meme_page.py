import requests
from util import Page, MemeEntry

class MemePage(Page):
	def __init__(self, url: str, session: requests.Session) -> None:
		super().__init__(url, session)

		self.title = self.soup.find('h1', attrs={'id': 'doctitle'}).get_text()
		self.views = int(''.join([x for x in self.soup.select('.columns.ctxx')[0].find('li').get_text() if x.isnumeric()]))
		self.likes = int(self.soup.find('p', 'useful_for_me').find('a')['data-num'])

		self.explanation, self.history, self.usage, self.other_data = '', '', '', {}
		for header, text in zip(
			self.soup.select('#content-body h2'),
			self.soup.select('#content-body h2 + div')
		):
			header, text = header.get_text(), '\n'.join([x.get_text() for x in text])
			if '是什么梗' in header or '意思' in header:
				self.explanation += '\n\n'
				self.explanation += text
			elif '来历' in header or '来源' in header or '出处' in header or '经历' in header:
				self.history += '\n\n'
				self.history += text
			elif '用法' in header or '使用' in header:
				self.usage += '\n\n'
				self.usage += text
			else:
				self.other_data[header] = text

		self.explanation, self.history, self.usage = self.explanation.strip(), self.history.strip(), self.usage.strip()

		self.similar = [
			MemeEntry(
				url=x.find('a')['href'],
				title=x.find('a').get_text(),
				timestamp=None
			) for x in self.soup.find('ul', attrs={'id': 'related_doc'}).find_all('li')
		]
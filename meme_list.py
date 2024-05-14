import requests
from util import Page, MemeEntry
from datetime import datetime

class MemeList(Page):
	def __init__(self, url: str, session: requests.Session) -> None:
		super().__init__(url, session)

		self.list_parent = self.soup.find('dl', attrs={'class': 'col-dl'})
		self.list_elems = self.list_parent.find_all('dd')
		self.list = [
			MemeEntry(
				url=entry.find('a')['href'],
				title=entry.find('a').get_text(),
				timestamp=datetime.strptime(entry.get_text()[len(entry.find('a').get_text()):], '%Y-%m-%d %H:%M'),
			) for entry in self.list_elems
		]

		next_button = self.soup.find('div', attrs={'id': 'fenye'}).find_all('a')
		if next_button:
			next_button = next_button[-1]
			self.next = next_button['href'] if next_button.get_text() == '››' else None
		else:
			self.next = None
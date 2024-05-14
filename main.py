import csv
import requests
from meme_page import MemePage
from json import dumps
from tqdm import trange
from time import sleep

with open('output.csv', 'w', newline='') as f:
	csv_writer = csv.writer(f)
	csv_writer.writerow(('id', 'title', 'views', 'likes', 'explanation', 'history', 'usage', 'other', 'similar'))
	with requests.Session() as session:
		for i in trange(10, 1159):
			try:
				page = MemePage(f'https://gengbaike.cn/doc-view-{str(i)}.html', session)
				csv_writer.writerow((
					str(i),
					page.title,
					page.views,
					page.likes,
					page.explanation,
					page.history,
					page.usage,
					dumps(page.other_data),
					page.similar
				))
			except:
				pass
			sleep(15)
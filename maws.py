from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import os
import time
from collections import defaultdict
import json

class AwardWinners:

	# main page
	URL = 'https://en.wikipedia.org/wiki/Category:Music_award_winners'

	# relevant awards
	AWARDS = {k: {'url': None, 
					'artists': set()} 
					for k in 
			  			['americana music honors & awards',
			  			'anugerah',       
			  			'apra award',     
			  			'aria award',
			  			'brit award',
			  			'echo',
			  			'eurovision',
			  			'golden globe',
			  			'grammy',
			  			'independent music awards',
			  			'kerrang! awards',
			  			'korean music award',
			  			'latin grammy',
			  			'melon music award',
			  			'mnet asian music award',
			  			'nme awards',
			  			'pacific music award',
			  			'world music awards']}

	ARTISTS = defaultdict(list)

	def __init__(self):
		
		self.STORAGE_DIR = 'collected'

	def get(self):

		self.DRIVER = webdriver.Chrome('webdriver/chromedriver')

		self.DRIVER.get(AwardWinners.URL)

		h = self.DRIVER.find_element_by_id('mw-subcategories')

		for _ in h.find_elements_by_class_name('CategoryTreeItem'):

			awards_ = []

			for a in AwardWinners.AWARDS:
				if a.lower() in _.text.lower().strip():
					l = _.find_element_by_xpath('a').get_attribute('href')
					awards_.append((a, l))

			if awards_:

				a, _ = max(awards_, key=lambda x: len(x[0].split()))
				AwardWinners.AWARDS[a]['url'] = _

		for k in AwardWinners.AWARDS:
			if not AwardWinners.AWARDS[k]['url']:
				print(AwardWinners.AWARDS[k]['url'])

		for k in AwardWinners.AWARDS:

			print(f'award: {k}...')

			try:
				self.DRIVER.get(AwardWinners.AWARDS[k]['url'])
			except:
				continue

			scrape_ = True

			while scrape_:

				div_ = self.DRIVER.find_element_by_id('mw-pages')
	
				for p in div_.find_elements_by_class_name('mw-category-group'):
	
					isLetter = False
	
					try:
						isLetter = p.find_element_by_xpath('.//h3').text.strip()
					except:
						continue
	
					if isLetter and isLetter.replace('-','').isalnum():
						for i in p.find_elements_by_xpath('.//li'):
							AwardWinners.AWARDS[k]['artists'].add(i.text.lower().split('(')[0].strip())
					else:
						# go to the next block
						continue
	
				# is there next page
				try:
					next_page_ = div_.find_element_by_partial_link_text('next page')
					self.DRIVER.get(next_page_.get_attribute('href'))
				except:
					scrape_ = False


		self.DRIVER.close()

		# fill in a dictionary with artists as keys and awards as a list of values 

		for award in AwardWinners.AWARDS:
			for artist in AwardWinners.AWARDS[award]['artists']:
				AwardWinners.ARTISTS[artist].append(award)

		return self

	def save(self, f):

		if not os.path.exists(self.STORAGE_DIR):
			os.mkdir(self.STORAGE_DIR)

		json.dump(AwardWinners.ARTISTS, open(f'{self.STORAGE_DIR}/{f}','w'))

		print(f'saved {len(AwardWinners.ARTISTS)} artists to {f}')

if __name__ == '__main__':

	aw = AwardWinners()
	aw.get()
	aw.save('award_winners.json')


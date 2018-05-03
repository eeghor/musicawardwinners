from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import os
import time
from collections import defaultdict

class AwardWinners:

	# main page
	URL = 'https://en.wikipedia.org/wiki/Category:Music_award_winners'

	# relevant awards
	AWARDS = {k: {'url': None, 
					'artists': set()} 
					for k in 
			  			['americana music honors & awards',    # since 2002
			  			'anugerah',           # since 1997
			  			'australasian performing right association music award',     # apra
			  			'australian recording industry association music award',
			  			'brit awards',
			  			'echo music prize',
			  			'eurovision',
			  			'golden globe',
			  			'grammy',
			  			'independent music awards',
			  			'kerrang! awards',
			  			'korean music award',
			  			'latin grammy award',
			  			'melon music award',
			  			'mnet asian music award',
			  			'nme awards',
			  			'pacific music award',
			  			'world music awards']}

	def __init__(self):
		
		self.ARTISTS = defaultdict(set)

	def get(self):

		# ChromeDriver is 2.38 available at https://chromedriver.storage.googleapis.com/2.38/chromedriver_mac64.zip
		self.DRIVER = webdriver.Chrome('webdriver/chromedriver')

		self.DRIVER.get(AwardWinners.URL)

		h = self.DRIVER.find_element_by_id('mw-subcategories')

		for _ in h.find_elements_by_class_name('CategoryTreeItem'):
			for a in AwardWinners.AWARDS:
				if a.lower() in _.text.lower():
					l = _.find_element_by_xpath('a').get_attribute('href')
					AwardWinners.AWARDS[a]['url'] = l
					break

		for k in AwardWinners.AWARDS:

			try:
				self.DRIVER.get(AwardWinners.AWARDS[k]['url'])
			except:
				continue

			for p in self.DRIVER.find_elements_by_class_name('mw-category-group'):

				letter = None

				try:
					letter = p.find_element_by_xpath('h3').text.strip()
				except:
					continue

				if letter and letter.isalnum():
					for i in p.find_elements_by_xpath('.//li'):
						AwardWinners.AWARDS[k]['artists'].add(i.text.lower().strip())
				else:
					continue
				
		print(AwardWinners.AWARDS)


		self.DRIVER.close()

		return self

if __name__ == '__main__':

	aw = AwardWinners()
	aw.get()


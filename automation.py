from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import unittest


class SearchFunctions(unittest.TestCase):

	def setUp(self):
		self.browse = webdriver.Chrome()

	def test_serach(self):
		browse = self.browse
		try:
			browse.get('https://www.farfetch.com')
		except Exception as e:
			print(e)
		else:	
			browse.maximize_window()
			assert 'FARFETCH - Abrindo portas para o mundo da moda' in browse.page_source
			search_txt = browse.find_element_by_id('search')
			search_txt.send_keys('Relógios')
			search_txt.send_keys(Keys.ENTER)


	def tearDown(self):
		time.sleep(5)
		self.browse.quit;

if __name__ == "__main__":
	unittest.main()




from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time
import unittest
import requests
import json


class filipeTest(unittest.TestCase):

	def setUp(self):
		self.browse = webdriver.Chrome('./chromedriver')

	def googleSearch(self, browse):
		search_google = browse.find_element_by_xpath("//input[@name='q']")
		search_google.send_keys('Amazon Brasil')
		search_google.send_keys(Keys.ENTER)

	def googleResultsFindAmazon(self, browse):
		for element in browse.find_elements_by_xpath('//div[@class="GyAeWb"]'):
				try:
					link = element.find_element_by_xpath(".//div[@class='d5oMvf']/a")
				except Exception as e:
					print('This element do not exist...')
		link.click()

	def amazonSearchForIphone(self, browse):
		search_amazon = browse.find_element_by_xpath("//input[@id='twotabsearchtextbox']")	
		search_amazon.send_keys('iPhone')
		search_amazon.send_keys(Keys.ENTER)

	def amazonResultsFindByIphoneCards(self, browse):	
		ads_data = []
		count = 0
		for i in range(1,8):
			browse.get(f'https://www.amazon.com.br/s?k=iPhone&page={i}&__mk_pt_BR=%C3%85M%C3%85%C5%BD%C3%95%C3%91&qid=1629651034&ref=sr_pg_2')
			html = browse.page_source

			soup = BeautifulSoup(html, 'lxml')
			cards = soup.find_all('div', {'data-asin': True, 'data-component-type': 's-search-result'})

			for card in cards:
				h2 = card.h2
				title = h2.text.strip()
				url = h2.a.get('href')
				try:
					price = card.find('span', class_='a-price-whole').text
					fraction = card.find('span', class_='a-price-fraction').text
					full_price = (price + fraction)
				except Exception as e:
					print('This card dont have a price...')


				title_temp = title.split(' ')

				if title_temp[0].lower() == 'iphone':
					if title not in ads_data:
						data = {'title': title, 'price': full_price}
						ads_data.append(data)
						count += 1

		print('Total numbers of iphone is: ' + str(count))
		return ads_data

	def amazonGreatestCardValue(self, ads_data):
		price_temp = 0.00
		title = ""
		url = ""
		for data in ads_data:		
			price_s = data.get('price').replace('.','')
			price_s = price_s.replace(',','.')
			price_f = float(price_s)

			if price_temp < price_f:
				price_temp = price_f
				title = data.get('title')
				url = data.get('URL')

		print(title + ' R$:' + str(price_temp))
		return price_temp

	def exchangeGeneratesApi(self, base, symbols, amount):
		endpoint = 'latest'
		URL = 'http://api.exchangeratesapi.io/v1/' + endpoint
		PARAMS = {'access_key':'d33aeeb8ae102f93d64cfe185dcd9d5d',
				  'base': base,
				  'symbols': symbols}

		r = requests.get(url = URL, params = PARAMS)
		data = r.json()
		#print(datas)

		rates = data['rates']
		convert = float(rates['BRL'])
		total_euro = convert * amount
		print('Product value in EUR is: ' + '%.2f' % total_euro + '€')
		

	def test1(self):
		
		browse = self.browse
		try:
			browse.get('https://www.google.com')
		except Exception as e:
			print(e)
		else:	
			browse.maximize_window()

			assert 'Google' in browse.page_source
			self.googleSearch(browse)

			self.googleResultsFindAmazon(browse)
			
			self.amazonSearchForIphone(browse)	
						
			ads_data = self.amazonResultsFindByIphoneCards(browse)

			expensive = self.amazonGreatestCardValue(ads_data)
		
			self.exchangeGeneratesApi('EUR','BRL', expensive)


	def tearDown(self):
		time.sleep(2)
		self.browse.quit;



if __name__ == "__main__":
	unittest.main()
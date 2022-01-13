from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import InvalidArgumentException
from selenium.common.exceptions import WebDriverException
import requests
import time
import random


### Get html contents of a given website.
def get_html_contents(homepage, site):
	global soup

	url = site

	## Creates a browser via Selenium
	browser = webdriver.Chrome()
	browser.minimize_window()

	homepage = true_homepage(homepage)

	## Attempts to load the website via Selenium. If it can't load, there are "except" statements to solve that.
	try:
		browser.get(url)
		print('Visiting ' + url)
	except InvalidArgumentException: ## Takes care of the issue when you run a sublink through this function.
									 ## Sometimes the sublink only contains the portion after ".com".
									 ## For example the sublink might only be "/products/laser-system."
									 ## This except statement then combines the sublink to the homepage to
									 ## get a valid url.
		try:
			browser.get(homepage + url)
			print('Visiting ' + homepage + url)
		except WebDriverException:   ## This exception occurs if the above try statement fails. This means that
									 ## the website truly cannot be found. Therefore, this function returns
									 ## "dummy" values that imply that nothing was found on this website
			return [0], sample_html, 0
	except WebDriverException:		 ## This exception combats a "TypeError" that used to crash the program. This
									 ## error is resolved by returning "dummy" values that imply that nothing was
									 ## found on this website. Very similar to the above exception.
		return [0], sample_html, 0

	time.sleep(1 * random_offset(10))

	## Uses BeautifulSoup to begin extracting and saving the html contents of the website
	html = browser.page_source
	soup = BeautifulSoup(html, 'html.parser')

	## This code finishes the extraction and saving of html contents. If there are issues, there are "except"
	## statements to solve that
	try:
		html_contents = soup.body.contents
	except: ## Tries to get around the rare error: "AttributeError 'NoneType' object has no attribute 'contents'". The code
			## below is very similar to the code found above.
		try:
			browser.get(url)
		except InvalidArgumentException:
			browser.get(homepage + url)
			print('Visiting ' + homepage + url)
		try: ## Gives the website a bit more time to load before trying to extract html contents
			time.sleep(2)
			html = browser.page_source
			time.sleep(2)
			soup = BeautifulSoup(html, 'html.parser')
			time.sleep(2)
			html_contents = soup.body.contents
		except: ## Returns "dummy" values that imply nothing was found on this website
			return [0], sample_html, 0

	return html_contents


### Extract all the text from html_contents and save it to "all_text"
def get_all_website_text(html_contents, html_contents_length):
	all_text = []

	for i in range(html_contents_length):
		line_to_add = ['', ''] 
		if html_contents[i] != '\n' and not (str(type(html_contents[i])) == "<class 'bs4.element.Comment'>"):
			try:
				line_to_add[0] = html_contents[i].get_text() ## 27/7
			except AttributeError:
				line_to_add[0] = ''	
		all_text.append(line_to_add)

	return all_text


### The website text received from get_all_website_text() is then saved to website_lines.txt
def save_website_text(num_sections_of_website, all_text):
	file = open('website_lines.txt', 'w')
	for i in range(num_sections_of_website):
		try:
			for j in range(len(all_text[i])):
				file.write(str(all_text[i][j]))
		except UnicodeEncodeError as bad_char:
			for k in range(len(all_text[i])):
				for l in range(len(all_text[i][k])):
					try:
						file.write(str(all_text[i][k][l]))
					except UnicodeEncodeError:
						file.write('*')
	file.close()


### Takes a link and gets the true homepage. True homepage is the website without any "/" subsections attatched.
def true_homepage(homepage):
	for i in range(len(homepage[9:])):
		if homepage[9 + i] == '/':
			return homepage[:i + 9]

	return homepage


### Gets a random offset depending on the percentage given. E.g. percentage = 10 will return random number between 0.9 and 1.1.
def random_offset(percentage):
	offset = 0.01 * random.randint(100 - percentage, 100 + percentage)
	return offset


def get_amazon_entry_html_contents(entry_number):
	entry_number = str(entry_number)
	tag_name = "MAIN-SEARCH_RESULTS-" + entry_number
	specific_html_contents = soup.find(attrs = {'cel_widget_id': tag_name})
	return specific_html_contents


def get_components_of_amazon_entry(specific_html_contents):
	components = {}
	title = specific_html_contents.find(class_ = 'a-size-medium a-color-base a-text-normal')
	components['Title'] = title.get_text()

	prices_and_availability = specific_html_contents.find_all(class_ = 'sg-col-inner')[2]
	components['Prices and Availability'] = prices_and_availability
	return components


def sort_data_from_prices_and_availability(prices_and_availability):
	print(prices_and_availability)
	number_of_items = len(prices_and_availability)
	item_index = 0
	primary_section = []
	secondary_section = []
	for item in prices_and_availability:
		subtexts = get_list_of_separate_texts(item)
		if item_index >= number_of_items - 1:
			secondary_section.extend(subtexts)
		else:
			primary_section.extend(subtexts)
		item_index += 1
	print_get_text_of_all_sections_in_desired_html_contents(primary_section)
	print_get_text_of_all_sections_in_desired_html_contents(secondary_section)


def print_get_text_of_all_sections_in_desired_html_contents(desired_html_contents):
	for item in desired_html_contents:
		for sub_item in item:
			try:
				print(sub_item.get_text())
			except AttributeError:
				print('Attribute Error')


def get_list_of_separate_texts(item):
	subtexts = []
	texts = item.find_all(class_ = 'a-row a-size-base a-color-base')
	print(texts)
	for text in texts:
		subtexts.extend(text)
	texts = item.find_all(class_ = 'a-row a-size-base a-color-secondary')
	print(texts)
	for text in texts:
		subtexts.extend(text)
	return subtexts

def main():
	homepage = 'https://www.amazon.com/s?k=the+empty+box+and+the+zeroth+maria+3&ref=nb_sb_noss_1'
	site = 'https://www.amazon.com/s?k=the+empty+box+and+the+zeroth+maria+3&ref=nb_sb_noss_1'
	html_contents = get_html_contents(homepage, site)
	all_text = get_all_website_text(html_contents, len(html_contents))
	save_website_text(len(all_text), all_text)
	specific_html_contents = get_amazon_entry_html_contents(3)
	components = get_components_of_amazon_entry(specific_html_contents)

	sort_data_from_prices_and_availability(components['Prices and Availability'])

	'''
	print(components['Prices and Availability'])
	print(len(components['Prices and Availability']))
	for item in components['Prices and Availability']:
		print(item.get_text())
	'''


main()
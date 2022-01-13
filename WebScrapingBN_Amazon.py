from selenium import webdriver
from selenium.common.exceptions import InvalidArgumentException
from selenium.common.exceptions import WebDriverException
from bs4 import BeautifulSoup
import requests
import time
import random
from csv import writer


### Get html contents of a given website.
def get_html_contents_and_soup(homepage, site):

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

	return html_contents, soup



def get_refreshed_html_contents_and_soup(homepage, site):

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
	browser.refresh()
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

	return html_contents, soup


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


def AMZ_get_entry_html_contents(entry_number, soup):
	entry_number = str(entry_number)
	tag_name = "MAIN-SEARCH_RESULTS-" + entry_number
	specific_html_contents = soup.find(attrs = {'cel_widget_id': tag_name})
	return specific_html_contents


def AMZ_get_components_of_entry(specific_html_contents):
	components = {}
	title = specific_html_contents.find(class_ = 'a-size-medium a-color-base a-text-normal')
	components['Title'] = title.get_text()
	print('Title fetched:')
	print(components['Title'])

	prices_and_availability = specific_html_contents.find_all(class_ = 'sg-col-inner')[2]
	components['Prices and Availability'] = prices_and_availability
	return components


def AMZ_sort_data_from_prices_and_availability(prices_and_availability):
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


def AMZ_print_get_text_of_all_sections_in_desired_html_contents(desired_html_contents):
	for item in desired_html_contents:
		for sub_item in item:
			try:
				print(sub_item.get_text())
			except AttributeError:
				print('Attribute Error')


def AMZ_get_list_of_separate_texts(item):
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


def COMBINED_FUNC_AMZ(list_of_titles):
	for title in list_of_titles:
		link = get_amz_link(title)
		html_contents, soup = get_html_contents_and_soup(link, link)
		all_entries_html_contents = AMZ_get_all_entries_html_contents(soup)
		for entry_html_contents in all_entries_html_contents:
			components = AMZ_get_components_of_entry(entry_html_contents)


def AMZ_get_all_entries_html_contents(soup):
	all_entries_html_contents = []
	i = 0
	all_entries_scraped = False
	while not all_entries_scraped:
		entry_html_contents = AMZ_get_entry_html_contents(i, soup)
		if entry_html_contents == None:
			all_entries_scraped = True
			continue
		i += 1
		all_entries_html_contents.append(entry_html_contents)

	return all_entries_html_contents
		

def get_amz_link(title):
	title = title.strip('\n')
	title = title.replace(' ', '+')
	random_int = random.randint(1, 2)
	if random_int == 1:
		link = 'https://www.amazon.com/s?k=' + title + '&ref=nb_sb_noss_1'
	else:
		link = 'https://www.amazon.com/s?k=' + title + '&ref=nb_sb_noss_2'
	return link


def YP_find_html_contents_with_titles(html_contents, soup):
	titles = soup.find_all(class_ = 'series-title')
	return titles


def YP_get_titles_from_html_contents_with_titles(html_contents_with_titles):
	list_of_titles = []
	for html_content in html_contents_with_titles:
		list_of_titles.append(html_content.get_text().strip('\n'))
	return list_of_titles


def save_list_to_file(file_name, list_to_save):
	file = open(file_name, 'w')
	for item in list_to_save:
		try:
			file.write(item + '\n')
		except UnicodeEncodeError:
			continue
	file.close()



def is_valid_entry(html_contents):
	return str(type(html_contents)) != "<class 'bs4.element.NavigableString'>"



def get_volume_number(text_describing_volume):
	if not does_string_contain_number(text_describing_volume):
		volume_number = 1
		return volume_number
	text_describing_volume = text_describing_volume.lower()
	if 'vol.' in text_describing_volume:
		length_of_volume_signifier = len('vol.')
		index_of_volume_word = text_describing_volume.index('vol.')
		first_index_after_volume_word = index_of_volume_word + length_of_volume_signifier
		beggining_index_of_number = find_beggining_index_of_number(text_describing_volume, first_index_after_volume_word)
		end_index_of_number = find_end_index_of_number(text_describing_volume, beggining_index_of_number)
	elif 'vol' in text_describing_volume:
		length_of_volume_signifier = len('vol')
		index_of_volume_word = text_describing_volume.index('vol')
		first_index_after_volume_word = index_of_volume_word + length_of_volume_signifier
		beggining_index_of_number = find_beggining_index_of_number(text_describing_volume, first_index_after_volume_word)
		end_index_of_number = find_end_index_of_number(text_describing_volume, beggining_index_of_number)
	elif 'volume' in text_describing_volume:
		length_of_volume_signifier = len('volume')
		index_of_volume_word = text_describing_volume.index('volume')
		first_index_after_volume_word = index_of_volume_word + length_of_volume_signifier
		beggining_index_of_number = find_beggining_index_of_number(text_describing_volume, first_index_after_volume_word)
		end_index_of_number = find_end_index_of_number(text_describing_volume, beggining_index_of_number)
	else:
		first_index_after_volume_word = 0
		beggining_index_of_number = find_beggining_index_of_number(text_describing_volume, first_index_after_volume_word)
		end_index_of_number = find_end_index_of_number(text_describing_volume, beggining_index_of_number)
	volume_number = text_describing_volume[beggining_index_of_number:end_index_of_number + 1]
	try:
		volume_number = int(volume_number)
	except:
		volume_number = float(volume_number)
	return volume_number


def does_string_contain_number(text):
	if not isinstance(text, str):
		return False
	for ch in text:
		try:
			int(ch)
			return True
		except:
			continue
	return False


def get_float_version_of_price(price):
	if isinstance(price, float):
		return price
	else:
		price_without_currency_symbol = price[1:]
		float_price = float(price_without_currency_symbol)
	return float_price

'''
def get_string_version_of_price_w_currency_symbol(price):
	if '$' in price and instanceof(price, str):
		return price
	str_price = str(price)
	str_price_w_currency_symbol = '$' + str_price
	return str_price_w_currency_symbol
'''



def create_list_from_txt(file_name):
	the_list = []
	file = open(file_name, 'r')
	for line in file:
		line = line.strip('\n')
		the_list.append(line)
	file.close()
	return the_list



def main(get_titles_from_source):
	txt_for_book_titles = 'Book Titles.txt'

	if get_titles_from_source:
		list_of_titles = COMBINED_FUNC_get_book_titles()
	else:
		list_of_titles = create_list_from_txt(txt_for_book_titles)


	COMBINED_FUNC_AMZ(list_of_titles)


main(get_titles_from_source = False)
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


def COMBINED_FUNC_get_book_titles():
	homepage = 'https://yenpress.com/books/'
	site = 'https://yenpress.com/books/'
	html_contents, soup = get_html_contents_and_soup(homepage, site)

	html_contents_with_titles = YP_find_html_contents_with_titles(html_contents, soup)
	list_of_titles = YP_get_titles_from_html_contents_with_titles(html_contents_with_titles)
	print(list_of_titles)
	save_list_to_file('Book Titles.txt', list_of_titles)

	return list_of_titles


def COMBINED_FUNC_get_bookfinder_results(list_of_titles, country_code):
	book_finder_results = BF_setup_dict_with_blank_dicts_from_titles(list_of_titles)
	all_titles_titles_links_volumes = BF_setup_dict_with_blank_dicts_from_titles(list_of_titles)
	for i in range(2): ## Go through titles twice because sometimes the bookfinder subpages don't load all of the prices correctly. Doing twice reduces error. 
		for title in list_of_titles:
			soup = BF_fetch_html_contents_of_overarching_search(title, country_code)
			try:
				rough_titles_links_volumes = BF_find_titles_links_volumes(soup)
			except Exception as e: ## If the overarching search didn't load properly, the try section will lead to an exception
				if i == 0:
					print('Exception found: ', end = str(e) + '\n')
					book_finder_results[title] = None
					all_titles_titles_links_volumes[title] = None
					continue
				if i == 1:
					print('Exception found: ', end = str(e) + '\n')
					if book_finder_results[title] == None: ## Crude way of checking if iteration i == 0 loaded properly
						book_finder_results[title] = None
						all_titles_titles_links_volumes[title] = None
					else:
						continue
			refined_titles_links_volumes = BF_refine_titles_links_volumes(rough_titles_links_volumes)
			print(refined_titles_links_volumes)
			book_finder_data_all_subpages = BF_get_results_all_subpages(refined_titles_links_volumes)
			print(book_finder_data_all_subpages)
			if i == 0:
				book_finder_results[title] = book_finder_data_all_subpages
				all_titles_titles_links_volumes[title] = refined_titles_links_volumes
			if i == 1: ## Second iteration considers the two book_finder_data_all_subpages and the two titles_links_volumes and creates new versions that are the best of the two.
				book_finder_results_previous_iteration = book_finder_results[title]
				book_finder_data_all_subpages = BF_keep_best_results(book_finder_results_previous_iteration, book_finder_data_all_subpages)
				book_finder_results[title] = book_finder_data_all_subpages

				titles_links_volumes_previous_iteration = all_titles_titles_links_volumes[title]
				refined_titles_links_volumes = BF_keep_best_titles_links_volumes(titles_links_volumes_previous_iteration, refined_titles_links_volumes)
				all_titles_titles_links_volumes[title] = refined_titles_links_volumes
			print(book_finder_results[title])
			print(refined_titles_links_volumes)
	return book_finder_results, all_titles_titles_links_volumes


def BF_setup_dict_with_blank_dicts_from_titles(list_of_titles):
	book_finder_results = {}
	for title in list_of_titles:
		book_finder_results[title] = {}
	return book_finder_results


def BF_fetch_html_contents_of_overarching_search(title, country_code):

	special_formatted_title = title.replace(' ', '+')

	homepage = 'https://bookfinder.com/'
	site = 'https://www.bookfinder.com/search/?keywords=' + special_formatted_title +\
		'&currency=USD&destination=' + country_code+ '&mode=basic&classic=off&lang=en&st=sh&ac=qr&submit='

	html_contents, soup = get_html_contents_and_soup(homepage, site)

	return soup


def BF_find_titles_links_volumes(soup):
	titles_links_volumes = dict()
	first_box_of_results = soup.find(class_ = 'select-titlenames')
	for entry in first_box_of_results.children:
		if is_valid_entry(entry):
			link = find_first_sublink(entry)
			title = entry.get_text()
			volume = BF_find_volume(entry)
			titles_links_volumes[title] = {
			'Volume' : volume,
			'Links' : [link]
			}
	return titles_links_volumes


def is_valid_entry(html_contents):
	return str(type(html_contents)) != "<class 'bs4.element.NavigableString'>"


def find_first_sublink(html_contents):
	list_of_sublinks = []
	if str(type(html_contents)) == "<class 'bs4.element.Comment'>":
		return ''

	all_a_html = html_contents.find_all('a')
	for a in all_a_html:
		link = a.get('href')
		if link != None and 'javascript:void' not in link:
			list_of_sublinks.append(link)
	return list_of_sublinks[0]


def BF_find_volume(entry):
	html_contents_title_without_volume = entry.find(class_ = 'select-titlename-highlight')
	text_title_without_volume = html_contents_title_without_volume.string
	try:
		text_describing_volume = html_contents_title_without_volume.parent.contents[1].string
	except IndexError:
		text_describing_volume = None
	print(text_title_without_volume)
	print(text_describing_volume)
	volume_number = get_volume_number(text_describing_volume)
	print(volume_number)
	return volume_number


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


def find_beggining_index_of_number(text_describing_volume, first_index_after_volume_word):
	beggining_of_num_found = False 
	end_reached = False
	i = 0
	index_of_num = -1
	while not beggining_of_num_found and not end_reached:
		try:
			int(text_describing_volume[first_index_after_volume_word + i])
			index_of_num = first_index_after_volume_word + i
			beggining_of_num_found = True
		except:
			pass
		i += 1
		if first_index_after_volume_word + i >= len(text_describing_volume):
			end_reached = True
	return index_of_num


def find_end_index_of_number(text_describing_volume, beggining_index_of_number):
	reached_char_signifying_end = False ## End of number is tracked
	end_reached = False ## End of text_describing_volume tracked
	i = 0
	while not reached_char_signifying_end and not end_reached:
		current_char = text_describing_volume[beggining_index_of_number + i]
		try:
			int(current_char)
		except:
			if current_char != '.':
				end_index_of_num = beggining_index_of_number + i - 1
				reached_char_signifying_end = True
		i += 1
		if beggining_index_of_number + i >= len(text_describing_volume):
			if reached_char_signifying_end:
				break
			end_reached = True
			end_index_of_num = len(text_describing_volume) - 1
	return end_index_of_num


def BF_refine_titles_links_volumes(titles_links_volumes):
	volume_to_all_titles_stage1 = BF_remove_duplicates_and_create_volumes_to_titles(titles_links_volumes)
	volume_to_all_titles_stage2 = BF_remove_wrong_volumes_from_volume_to_all_titles(titles_links_volumes,\
		volume_to_all_titles_stage1)
	refined_titles_links_volumes = BF_implement_info_from_volume_to_all_titles_to_titles_links_volumes(\
		volume_to_all_titles_stage2, titles_links_volumes)
	return refined_titles_links_volumes
	


def BF_remove_wrong_volumes_from_volume_to_all_titles(titles_links_volumes, volume_to_all_titles):
	list_of_volumes = []
	for title in titles_links_volumes:
		book_info = titles_links_volumes[title]
		volume_number = book_info['Volume']
		list_of_volumes.append(volume_number)
	list_of_volumes = sorted(list_of_volumes)
	highest_volume = max(list_of_volumes)

	wrong_volumes = []
	for i in range(0, len(list_of_volumes) - 1):
		if list_of_volumes[i + 1] > 1 + list_of_volumes[i] * 1.5:
			wrong_volumes.append(list_of_volumes[i + 1])

	for volume in wrong_volumes:
		volume = str(volume)
		if len(volume) == 2:
			volume_number_to_test_legitimacy = float(volume[0:1] + '.' + volume[1:2])
			if volume_number_to_test_legitimacy in list_of_volumes:
				wrong_volume = float(volume)
				right_volume = volume_number_to_test_legitimacy
				BF_move_links_from_one_volume_to_another(wrong_volume, right_volume, volume_to_all_titles)
		elif len(volume) == 3:
			volume_number_to_test_legitimacy = float(volume[0:2] + '.' + volume[2:3])
			if volume_number_to_test_legitimacy in list_of_volumes:
				wrong_volume = float(volume)
				right_volume = volume_number_to_test_legitimacy
				BF_move_links_from_one_volume_to_another(wrong_volume, right_volume, volume_to_all_titles)

	return volume_to_all_titles


def BF_move_links_from_one_volume_to_another(wrong_volume, right_volume, volume_to_all_titles):
	links_to_move = volume_to_all_titles[wrong_volume]
	volume_to_all_titles[right_volume].extend(links_to_move)
	del volume_to_all_titles[wrong_volume]
	return volume_to_all_titles


def BF_remove_duplicates_and_create_volumes_to_titles(titles_links_volumes):
	volume_to_all_titles = {}
	for title in titles_links_volumes:
		book_info = titles_links_volumes[title]
		volume_number = book_info['Volume']
		if volume_number in volume_to_all_titles:
			volume_to_all_titles[volume_number].append(title)
		else:
			volume_to_all_titles[volume_number] = [title]
	

	return volume_to_all_titles
			

def BF_implement_info_from_volume_to_all_titles_to_titles_links_volumes(volume_to_all_titles, titles_links_volumes):
	for volume in volume_to_all_titles:
		title_to_keep = volume_to_all_titles[volume][0]
		titles_to_move = volume_to_all_titles[volume][1:]
		book_info_title_to_keep = titles_links_volumes[title_to_keep]
		for title in titles_to_move:
			book_info_title_to_move = titles_links_volumes[title]
			link = book_info_title_to_move['Links']
			book_info_title_to_keep['Links'].extend(link)
			del titles_links_volumes[title]
	return titles_links_volumes


def BF_get_results_all_subpages(titles_links_volumes):
	results_all_subpages = {}
	for volume_title in titles_links_volumes:
		book_info = titles_links_volumes[volume_title]
		links = book_info['Links']
		title_sublink_info = BF_create_empty_title_sublink_info_dict()
		for link in links:
			soup = BF_fetch_html_contents_of_sublink(link)
			cheapest_price, cheapest_store = BF_get_cheapest_price_and_store(soup)
			print(cheapest_price, cheapest_store)
			cheapest_price = get_float_version_of_price(cheapest_price)
			cheapest_amazon_price, cheapest_amazon_store = BF_get_cheapest_given_store_price_and_given_store_store_name(soup)
			print(cheapest_amazon_price, cheapest_amazon_store)
			cheapest_amazon_price = get_float_version_of_price(cheapest_amazon_price)
			title_sublink_info['Cheapest price'].append(cheapest_price)
			title_sublink_info['Cheapest store'].append(cheapest_store)
			title_sublink_info['Cheapest Amazon price'].append(cheapest_amazon_price)
			title_sublink_info['Cheapest Amazon store'].append(cheapest_amazon_store)
		title_sublink_info = BF_refine_title_sublink_info(title_sublink_info)
		results_all_subpages[volume_title] = title_sublink_info
		title_sublink_info = BF_create_empty_title_sublink_info_dict()
	return results_all_subpages


def BF_refine_title_sublink_info(title_sublink_info):
	if len(title_sublink_info['Cheapest price']) == 1:
		return title_sublink_info

	lst = title_sublink_info['Cheapest price']
	min_price = min(lst)
	index_of_min_price = lst.index(min_price)
	cheapest_store = title_sublink_info['Cheapest store'][index_of_min_price]

	lst = title_sublink_info['Cheapest Amazon price']
	min_amazon_price = min(lst)
	index_of_min_amazon_price = lst.index(min_amazon_price)
	cheapest_amazon_store = title_sublink_info['Cheapest Amazon store'][index_of_min_amazon_price]

	title_sublink_info['Cheapest price'] = [min_price]
	title_sublink_info['Cheapest store'] = [cheapest_store]
	title_sublink_info['Cheapest Amazon price'] = [min_amazon_price]
	title_sublink_info['Cheapest Amazon store'] = [cheapest_amazon_store]

	return title_sublink_info


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

def BF_create_empty_title_sublink_info_dict():
	title_sublink_info = {
	'Cheapest price': [],
	'Cheapest store': [],
	'Cheapest Amazon price': [],
	'Cheapest Amazon store': []
	}
	return title_sublink_info


def BF_create_arbitrarily_filled_title_sublink_info_dict():
	title_sublink_info = {
	'Cheapest price': [999],
	'Cheapest store': [None],
	'Cheapest Amazon price': [999],
	'Cheapest Amazon store': [None]
	}
	return title_sublink_info


def BF_keep_best_results(dict_version1, dict_version2):
	if dict_version1 == None and dict_version2 != None:
		return dict_version2

	best_version = {}
	for volume_title in dict_version1:
		title_sublink_info = BF_create_empty_title_sublink_info_dict()
		best_version[volume_title] = title_sublink_info

	for volume_title in dict_version1:
		title_sublink_info = best_version[volume_title]

		try:
			cheapest_price_version1 = dict_version1[volume_title]['Cheapest price'][0]
		except KeyError:
			cheapest_price_version1 = 999
		try:
			cheapest_price_version2 = dict_version2[volume_title]['Cheapest price'][0]
		except KeyError:
			cheapest_price_version2 = 999

		try:
			cheapest_store_version1 = dict_version1[volume_title]['Cheapest store'][0]
		except KeyError:
			cheapest_store_version1 = None
		try:
			cheapest_store_version2 = dict_version2[volume_title]['Cheapest store'][0]
		except KeyError:
			cheapest_store_version2 = None

		if cheapest_price_version1 <= cheapest_price_version2:
			title_sublink_info['Cheapest price'].append(cheapest_price_version1)
			title_sublink_info['Cheapest store'].append(cheapest_store_version1)
		else:
			title_sublink_info['Cheapest price'].append(cheapest_price_version2)
			title_sublink_info['Cheapest store'].append(cheapest_store_version2)

		try:
			cheapest_specific_store_price_version1 = dict_version1[volume_title]['Cheapest Amazon price'][0]
		except KeyError:
			cheapest_specific_store_price_version1 = 999
		try:
			cheapest_specific_store_price_version2 = dict_version2[volume_title]['Cheapest Amazon price'][0]
		except KeyError:
			cheapest_specific_store_price_version2 = 999

		try:
			cheapest_specific_store_store_version1 = dict_version1[volume_title]['Cheapest Amazon store'][0]
		except KeyError:
			cheapest_specific_store_store_version1 = None
		try:
			cheapest_specific_store_store_version2 = dict_version2[volume_title]['Cheapest Amazon store'][0]
		except KeyError:
			cheapest_specific_store_store_version2 = None

		if cheapest_specific_store_price_version1 <= cheapest_specific_store_price_version2:
			title_sublink_info['Cheapest Amazon price'].append(cheapest_specific_store_price_version1)
			title_sublink_info['Cheapest Amazon store'].append(cheapest_specific_store_store_version1)
		else:
			title_sublink_info['Cheapest Amazon price'].append(cheapest_specific_store_price_version2)
			title_sublink_info['Cheapest Amazon store'].append(cheapest_specific_store_store_version2)
		best_version[volume_title] = title_sublink_info

	return best_version


def BF_keep_best_titles_links_volumes(titles_links_volumes_previous_iteration, refined_titles_links_volumes):
	if titles_links_volumes_previous_iteration == None and refined_titles_links_volumes != None:
		return refined_titles_links_volumes
	return titles_links_volumes_previous_iteration



def BF_fetch_html_contents_of_sublink(sublink):
	homepage = 'https://bookfinder.com/'
	site = sublink

	html_contents, soup = get_html_contents_and_soup(homepage, site)

	return soup


def BF_fetch_refreshed_html_contents_of_sublink(sublink):
	homepage = 'https://bookfinder.com/'
	site = sublink

	html_contents, soup = get_refreshed_html_contents_and_soup(homepage, site)

	return soup

def BF_get_cheapest_price_and_store(soup):
	first_in_stock_html_contents = BF_get_first_in_stock_html_contents(soup)
	if first_in_stock_html_contents == None:
		return '$999', None
	price = first_in_stock_html_contents.find(class_ = 'results-price').get_text()
	price = change_price_format(price, 'metric', 'customary')
	store_html_content = first_in_stock_html_contents.find('img')
	store = store_html_content.get('title')
	return price, store


def BF_get_first_in_stock_html_contents(soup):
	soup = BF_get_html_contents_specified_book_condition(soup, 'New books: ')
	if soup == None:
		return None
	in_stock_entry_found = False
	checked_all_results = False
	first_entry_html_contents = soup.find(class_ = 'results-table-first-LogoRow has-data')
	first_entry_all_text = first_entry_html_contents.get_text().lower()
	#print(first_entry_all_text)
	if 'out of stock' or 'in stock soon' not in first_entry_all_text:
		in_stock_entry_found = True
		return first_entry_html_contents
	potential_first_entries_html_contents = soup.find_all(class_ = 'results-table-LogoRow has-data')
	i = 0
	while not in_stock_entry_found and not checked_all_results:
		if i == len(potential_first_entries_html_contents):
			checked_all_results = True
			return None
		current_entry_to_check_if_in_stock = potential_first_entries_html_contents[i]
		current_entry_all_text = current_entry_to_check_if_in_stock.get_text().lower()
		if 'out of stock' or 'in stock soon' not in current_entry_all_text:
			in_stock_entry_found = True
			continue
		i += 1
	first_in_stock_html_contents = current_entry_to_check_if_in_stock
	return first_in_stock_html_contents


def BF_get_html_contents_specified_book_condition(soup, type = 'New books: '):
	html_contents_list = soup.find_all('td')
	reached_end_of_html_contents_list = False
	found_desired_type = False
	i = 0
	while not reached_end_of_html_contents_list and not found_desired_type:
		entry = html_contents_list[i]
		if type in entry.get_text():
			found_desired_type = True
			continue
		if i == len(html_contents_list) - 1:
			reached_end_of_html_contents_list = True
			continue
		i += 1
	if found_desired_type:
		return entry
	else:
		html_contents_with_only_type_mentioned = soup.find(class_ = 'results-section-heading')
		try:
			if type in html_contents_with_only_type_mentioned.get_text():
				html_contents = soup.find(class_ = 'results-table-Logo')
				entry = html_contents
				found_desired_type = True
				return entry
		except AttributeError:
			return None
		return None


def BF_get_cheapest_given_store_price_and_given_store_store_name(soup, store = 'amazon'):
	first_in_stock_html_contents = BF_get_first_in_stock_html_contents_given_store(soup, store)
	if first_in_stock_html_contents == None:
		return '$999', None
	price = first_in_stock_html_contents.find(class_ = 'results-price').get_text()
	price = change_price_format(price, 'metric', 'customary')
	store_html_content = first_in_stock_html_contents.find('img')
	store = store_html_content.get('title')
	return price, store


def BF_get_first_in_stock_html_contents_given_store(soup, store = 'amazon'):
	soup = BF_get_html_contents_specified_book_condition(soup, 'New books: ')
	if soup == None:
		return None
	in_stock_entry_found = False
	checked_all_results = False
	first_entry_html_contents = soup.find(class_ = 'results-table-first-LogoRow has-data')
	first_entry_all_text = first_entry_html_contents.get_text().lower()
	if 'out of stock' or 'in stock soon' not in first_entry_all_text:
		company_name = BF_get_company_name(first_entry_html_contents)
		if store in company_name:
			in_stock_entry_found = True
			return first_entry_html_contents
	potential_first_entries_html_contents = soup.find_all(class_ = 'results-table-LogoRow has-data')
	i = 0
	while not in_stock_entry_found and not checked_all_results:
		if i == len(potential_first_entries_html_contents):
			checked_all_results = True
			return None
		current_entry_to_check_if_in_stock = potential_first_entries_html_contents[i]
		current_entry_all_text = current_entry_to_check_if_in_stock.get_text().lower()
		if 'out of stock' or 'in stock soon' not in current_entry_all_text:
			company_name = BF_get_company_name(current_entry_to_check_if_in_stock).lower()
			if store in company_name:
				in_stock_entry_found = True
				continue
		i += 1
	first_in_stock_html_contents = current_entry_to_check_if_in_stock
	return first_in_stock_html_contents


def BF_get_company_name(html_contents):
	store_html_content = html_contents.find('img')
	store = store_html_content.get('title')
	return store


def COMBINED_FUNC_get_analyzed_results(book_finder_results1, book_finder_results2,\
	all_titles_titles_links_volumes1, all_titles_titles_links_volumes2, list_of_titles):
	combined_results_volume_to_prices = AN_get_combined_results_volume_to_prices(book_finder_results1,\
	book_finder_results2, all_titles_titles_links_volumes1, all_titles_titles_links_volumes2, list_of_titles)
	print('combined_results_volume_to_prices:')
	print(combined_results_volume_to_prices)
	price_discrepancies = AN_get_price_discrepancies(combined_results_volume_to_prices, list_of_titles)
	print(price_discrepancies)
	return price_discrepancies


def AN_get_combined_results_volume_to_prices(book_finder_results1, book_finder_results2,\
	all_titles_titles_links_volumes1, all_titles_titles_links_volumes2, list_of_titles):
	combined_results_volume_to_prices = BF_setup_dict_with_blank_dicts_from_titles(list_of_titles)

	for title in all_titles_titles_links_volumes1:
		for volume_title in all_titles_titles_links_volumes1[title]:
			volume = all_titles_titles_links_volumes1[title][volume_title]['Volume']
			combined_results_volume_to_prices[title][volume] = {}
			combined_results_volume_to_prices[title][volume]['Results 1'] = book_finder_results1[title][volume_title]

	for title in all_titles_titles_links_volumes2:
		for volume_title in all_titles_titles_links_volumes2[title]:
			volume = all_titles_titles_links_volumes2[title][volume_title]['Volume']
			if volume not in combined_results_volume_to_prices[title]:
				combined_results_volume_to_prices[title][volume] = {}
				combined_results_volume_to_prices[title][volume]['Results 2'] = book_finder_results2[title][volume_title]
			else:
				combined_results_volume_to_prices[title][volume]['Results 2'] = book_finder_results2[title][volume_title]

	return combined_results_volume_to_prices


def AN_get_price_discrepancies(combined_results_volume_to_prices, list_of_titles):
	price_discrepancies = BF_setup_dict_with_blank_dicts_from_titles(list_of_titles)
	for title in combined_results_volume_to_prices:
		for volume_number in combined_results_volume_to_prices[title]:
			print(combined_results_volume_to_prices[title][volume_number])

			try:
				results_from_country1 = combined_results_volume_to_prices[title][volume_number]['Results 1']
			except KeyError:
				results_from_country1 = BF_create_arbitrarily_filled_title_sublink_info_dict()
			try:
				results_from_country2 = combined_results_volume_to_prices[title][volume_number]['Results 2']
			except KeyError:
				results_from_country2 = BF_create_arbitrarily_filled_title_sublink_info_dict()

			country1_cheapest_amazon_minus_cheapest_store = results_from_country1['Cheapest Amazon price'][0] - results_from_country1['Cheapest price'][0]
			country1_cheapest_amazon_minus_cheapest_store = float("{:.2f}".format(country1_cheapest_amazon_minus_cheapest_store))
			country2_cheapest_amazon_minus_cheapest_store = results_from_country2['Cheapest Amazon price'][0] - results_from_country2['Cheapest price'][0]
			country2_cheapest_amazon_minus_cheapest_store = float("{:.2f}".format(country2_cheapest_amazon_minus_cheapest_store))
			if results_from_country2['Cheapest price'][0] > results_from_country1['Cheapest price'][0]:
				price_discrepancy_cheapest_store_both_countries = results_from_country2['Cheapest price'][0] - results_from_country1['Cheapest price'][0]
				price_discrepancy_cheapest_store_both_countries = float("{:.2f}".format(price_discrepancy_cheapest_store_both_countries))
				cheapest_country = "Country 1"
			else:
				price_discrepancy_cheapest_store_both_countries = results_from_country1['Cheapest price'][0] - results_from_country2['Cheapest price'][0]
				price_discrepancy_cheapest_store_both_countries = float("{:.2f}".format(price_discrepancy_cheapest_store_both_countries))
				cheapest_country = "Country 2"
			if results_from_country2['Cheapest Amazon price'][0] > results_from_country1['Cheapest Amazon price'][0]:
				price_discrepancy_cheapest_amazon_store_both_countries = results_from_country2['Cheapest Amazon price'][0] - results_from_country1['Cheapest Amazon price'][0]
				price_discrepancy_cheapest_amazon_store_both_countries = float("{:.2f}".format(price_discrepancy_cheapest_amazon_store_both_countries))
				cheapest_amazon_country = "Country 1"
			else:
				price_discrepancy_cheapest_amazon_store_both_countries = results_from_country1['Cheapest Amazon price'][0] - results_from_country2['Cheapest Amazon price'][0]
				price_discrepancy_cheapest_amazon_store_both_countries = float("{:.2f}".format(price_discrepancy_cheapest_amazon_store_both_countries))
				cheapest_amazon_country = "Country 2"
			cheapest_amazon_country1_minus_cheapest_store_country2 = results_from_country1['Cheapest Amazon price'][0] - results_from_country2['Cheapest price'][0]
			cheapest_amazon_country1_minus_cheapest_store_country2 = float("{:.2f}".format(cheapest_amazon_country1_minus_cheapest_store_country2))
			price_discrepancies[title][volume_number] = {
			'Cheapest Amazon price country 1 minus cheapest price': country1_cheapest_amazon_minus_cheapest_store,
			'Cheapest store country 1': results_from_country1['Cheapest store'][0],
			'Cheapest Amazon store country 1': results_from_country1['Cheapest Amazon store'][0],
			'Cheapest Amazon price country 2 minus cheapest price': country2_cheapest_amazon_minus_cheapest_store,
			'Cheapest store country 2': results_from_country2['Cheapest store'][0],
			'Cheapest Amazon store country 2': results_from_country2['Cheapest Amazon store'][0],
			'Price discrepancy both countries': price_discrepancy_cheapest_store_both_countries,
			'Cheapest country': cheapest_country,
			'Price discrepancy Amazon both countries': price_discrepancy_cheapest_amazon_store_both_countries,
			'Cheapest Amazon country': cheapest_amazon_country,
			'Cheapest Amazon country 1 minus cheapest store country 2' : cheapest_amazon_country1_minus_cheapest_store_country2 
			}
	return price_discrepancies



def save_results(price_discrepancies):
	csv_file = open('BookResults.csv', 'w')
	csv_writer = writer(csv_file, delimiter = ';')
	for title in price_discrepancies:
		csv_writer.writerow([title])
		for volume_number in price_discrepancies[title]:
			csv_writer.writerow([volume_number])
			row_data_entry_titles = []
			row_data_entry_numbers = []
			for data_entry_title in price_discrepancies[title][volume_number]:
				data_entry_value = price_discrepancies[title][volume_number][data_entry_title]
				row_data_entry_titles.append(data_entry_title)
				row_data_entry_numbers.append(data_entry_value)
			csv_writer.writerow(row_data_entry_titles)
			csv_writer.writerow(row_data_entry_numbers)
		csv_writer.writerow([''])
	csv_file.close()


def change_price_format(price, from_type = 'metric', to_type = 'customary'):
	if from_type == 'metric':
		return price.replace(',', '.')
	else:
		return price.replace('.', ',')


def create_list_from_txt(file_name):
	the_list = []
	file = open(file_name, 'r')
	for line in file:
		line = line.strip('\n')
		the_list.append(line)
	file.close()
	return the_list



def main(get_titles_from_source):
	print('**********')
	print('Did you set the appropriate value for get_titles_from_source?')
	print('**********')
	foreign_country_code = 'uk'
	your_country_code = 'us'
	txt_for_book_titles = 'Book Titles.txt'

	if get_titles_from_source:
		list_of_titles = COMBINED_FUNC_get_book_titles()
	else:
		list_of_titles = create_list_from_txt(txt_for_book_titles)

	book_finder_results_your_country, all_titles_titles_links_volumes_your_country = \
		COMBINED_FUNC_get_bookfinder_results(list_of_titles, your_country_code)
	book_finder_results_foreign_country, all_titles_titles_links_volumes_foreign_country = \
		COMBINED_FUNC_get_bookfinder_results(list_of_titles, foreign_country_code)
	price_discrepancies = COMBINED_FUNC_get_analyzed_results(book_finder_results_your_country, book_finder_results_foreign_country,\
		all_titles_titles_links_volumes_your_country, all_titles_titles_links_volumes_foreign_country, list_of_titles)
	save_results(price_discrepancies)


main(get_titles_from_source = True)
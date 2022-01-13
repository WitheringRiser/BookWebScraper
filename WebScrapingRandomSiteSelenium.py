###                         Web Scraper Program by Lukas Brazdeikis                      
###                                     Created 5/7/21                                  
###                                  Last modified 29/7/21                              
### The purpose of this program is to scrape websites looking for keywords and basic website structure.
### The prevalence of keywords, tabs, bad tabs/text, and website size is then turned into various metrics 
### that are saved in various text files.
### Inputs: 
###		- interested_tabs, thoroughness, _bad_tabs_and_bad_text from RunEntireProgram.py
###		- websites_to_scrape.txt
### 	- keywords.txt
### Outputs:
###		- website_lines.txt
###		- list_of_product_links.txt
###		- points_from_website.txt
###		- keyword_matches_from_website_to_website.txt
###		- tab_matches_to_website.txt
### Functions:
###		- get_html_contents()								  - random_offset()
###		- find_html_contents_where_products_pages_can_be()	  - search_through_multiple_links_to_find_keyword_matches()
###		- find_tab_matches()								  - write_product_links()
###		- find_bad_tabs_and_bad_text()						  - calculate_website_structure_score()
###		- get_all_website_text()							  - find_html_content_of_a_given_html_text()
###		- calculate_website_size()							  - find_sublinks()
###		- save_website_text()								  - refine_list()
###		- find_keyword_matches_on_website()					  - search_a_website_and_the_sublinks()
###		- add_keyword_matches_to_points()					  - read_website_links()
###		- add_tab_matches_to_points()						  - save_points_from_website()
###		- add_bad_tab_and_bad_text_matches_to_points()		  - save_keyword_matches()
###		- add_website_size_to_points()						  - save_tab_matches()
###		- get_keywords_list()								  - reset_bad_tabs_bad_text()
### 	- true_homepage()									  - main()


from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import InvalidArgumentException
from selenium.common.exceptions import WebDriverException
import requests
from csv import writer
import time
import os.path
import random

global score_values
score_values = {}
global scores
scores = {}
global website_structure
website_structure = {}
global num_404_pages
num_404_pages = [0]
global points
points = {}
global list_of_possible_scores_to_add
list_of_possible_scores_to_add = []


### Get html contents of a given website.
def get_html_contents(homepage, site):

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


### Searches through the html content and takes note of certain keyword mentions (from "interested tabs").
### The index in the html contents where this keywords is found is saved.
def find_html_contents_where_products_pages_can_be(html_contents, html_contents_length,\
 do_you_want_to_know_indices_where_product_pages_can_be, interested_tabs):
	html_contents_indices_where_products_pages_can_be = []

	for i in range(html_contents_length):
		line_to_add = ['', ''] 
		if html_contents[i] != '\n' and not (str(type(html_contents[i])) == "<class 'bs4.element.Comment'>"):
			try:
				line_to_add[0] = html_contents[i].get_text() ## 27/7
			except AttributeError:
				line_to_add[0] = ''
			if do_you_want_to_know_indices_where_product_pages_can_be:
				for tab in interested_tabs:
					if tab in line_to_add[0]:
						if i not in html_contents_indices_where_products_pages_can_be:
							html_contents_indices_where_products_pages_can_be.append(i)

	return html_contents_indices_where_products_pages_can_be


### Searches through the html content and takes note of certain keyword mentions (from "interested tabs").
### The tab match is then saved.
def find_tab_matches(html_contents, html_contents_length, interested_tabs, do_you_want_to_know_indices_where_product_pages_can_be):
	for i in range(html_contents_length):
		line_to_add = ['', ''] 
		if html_contents[i] != '\n' and not (str(type(html_contents[i])) == "<class 'bs4.element.Comment'>"):
			try:
				line_to_add[0] = html_contents[i].get_text() ## 27/7
			except AttributeError:
				line_to_add[0] = ''
			if do_you_want_to_know_indices_where_product_pages_can_be:
				for tab in interested_tabs:
					if tab in line_to_add[0]:
						tab_matches.append(tab)


### Searches through the html content and takes note of certain keyword mentions (from "bad_tabs_and_bad_text").
### The bad tab/bad text is then saved.
def find_bad_tabs_and_bad_text(html_contents, html_contents_length, do_you_want_to_know_indices_where_product_pages_can_be):
	for i in range(html_contents_length):
		line_to_add = ['', ''] 
		if html_contents[i] != '\n' and not (str(type(html_contents[i])) == "<class 'bs4.element.Comment'>"):
			try:
				line_to_add[0] = html_contents[i].get_text() ## 27/7
			except AttributeError:
				line_to_add[0] = ''
			if do_you_want_to_know_indices_where_product_pages_can_be:
				for key in bad_tabs_and_bad_text:
					if key in line_to_add[0]:
						bad_tabs_and_bad_text[key] += 1


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


### Calculates the website size based on the number of links found in the html contents.
### The website size is then saved to total_number_of_all_sublinks
def calculate_website_size(html_contents):
	global total_number_of_all_sublinks
	total_number_of_all_sublinks = [0]
	for i in range(len(html_contents)):
		if str(type(html_contents[i])) == "<class 'bs4.element.Comment'>" or\
		 str(type(html_contents[i])) == "<class 'bs4.element.NavigableString'>":
			continue
		all_a_html = html_contents[i].find_all('a')
		total_number_of_all_sublinks[0] += len(all_a_html)
	print('Website size (total number of sublinks): ' + str(total_number_of_all_sublinks[0]))


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


### Calls several other functions related to finding keywords, tabs, bad tabs/bad text.
def find_keyword_matches_on_website(homepage, site, do_you_want_to_know_indices_where_product_pages_can_be,\
num_websites_checked, list_of_keywords, interested_tabs):

	html_contents = get_html_contents(homepage, site)
	
	all_text = []
	html_contents_length = len(html_contents)
	html_contents_indices_where_products_pages_can_be = []
	num_sections_of_website = 0

	html_contents_indices_where_products_pages_can_be = find_html_contents_where_products_pages_can_be(html_contents,\
	 html_contents_length, do_you_want_to_know_indices_where_product_pages_can_be, interested_tabs)
	find_tab_matches(html_contents, html_contents_length, interested_tabs, do_you_want_to_know_indices_where_product_pages_can_be)
	find_bad_tabs_and_bad_text(html_contents, html_contents_length, do_you_want_to_know_indices_where_product_pages_can_be)
	all_text = get_all_website_text(html_contents, html_contents_length)
	num_sections_of_website = len(all_text)


	if do_you_want_to_know_indices_where_product_pages_can_be: ## If on the homepage, calculate website size
		calculate_website_size(html_contents)
	
	save_website_text(num_sections_of_website, all_text)

	num_lines_of_website = 0
	num_matches = 0
	
	
	with open('website_lines.txt', 'r') as website_lines:
		current_line = 0
		for line in website_lines:
			current_line += 1
			if current_line == 1:
				continue
			for keyword in list_of_keywords:
				if keyword in line:
					score = score_values[keyword]
					list_of_possible_scores_to_add.append(score)
					num_matches += 1
					keyword_matches.append(keyword)

	list_of_possible_scores_to_add.sort(key=lambda x: x, reverse=True)
	print(list_of_possible_scores_to_add)
	
	num_websites_checked[0] += 1
	print('Num matches: ' + str(num_matches))

	return html_contents_indices_where_products_pages_can_be, html_contents, num_matches


### For each keyword match (up to 4 most valuable) points are tallied
def add_keyword_matches_to_points(list_of_possible_scores_to_add, homepage):
	score = 0
	if len(list_of_possible_scores_to_add) > 4:
		score += 5 * list_of_possible_scores_to_add[0] + 5 * list_of_possible_scores_to_add[1] + 5 * list_of_possible_scores_to_add[2]\
		+ 5 * list_of_possible_scores_to_add[3]
	else:
		for scr in list_of_possible_scores_to_add:
			score += 5 * scr
	print('Score: ' + str(score))
	try:
		points[true_homepage(homepage)] += 1
		points[true_homepage(homepage)] -= 1
	except:
		points[true_homepage(homepage)] = 0

	points[true_homepage(homepage)] += score
	print(str(score) + ' points added')
	

### For each tab match (up to 3) points are tallied
def add_tab_matches_to_points(homepage):
	true_hmpg = true_homepage(homepage)
	num_tab_matches = website_structure[true_hmpg]

	try:
		points[true_hmpg] += 1
		points[true_hmpg] -= 1
	except:
		points[true_hmpg] = 0

	if num_tab_matches == 1:
		points[true_hmpg] += 50
		print('+50 points')
	elif num_tab_matches == 2:
		points[true_hmpg] += 75
		print('+75 points')
	elif num_tab_matches >= 3:
		points[true_hmpg] += 100
		print('+100 points')


def add_bad_tab_and_bad_text_matches_to_points(homepage):
	true_hmpg = true_homepage(homepage)

	total_category_matches = 0 # Max one match per item in bad_tab_and_bad_text
	for key in bad_tabs_and_bad_text:
		if bad_tabs_and_bad_text[key] > 1:
			total_category_matches += 1
	if total_category_matches >= 3:
		points[true_hmpg] -= 75
		print('-75 points')
	elif total_category_matches >= 2:
		points[true_hmpg] -= 50
		print('-50 points')
	elif total_category_matches == 1:
		points[true_hmpg] -= 25
		print('-25 points')


### For each tab match (up to 3) points are tallied
def add_website_size_to_points(homepage):
	true_hmpg = true_homepage(homepage)
	total_number_of_all_sublinks = total_number_of_all_sublinks[0]

	try:
		points[true_hmpg] += 1
		points[true_hmpg] -= 1
	except:
		points[true_hmpg] = 0

	if total_number_of_all_sublinks >= 500:
		points[true_hmpg] -= 150
		print('-100 points')
	elif total_number_of_all_sublinks >= 300:
		points[true_hmpg] -= 100
		print('-100 points')
	elif total_number_of_all_sublinks >= 200:
		points[true_hmpg] -= 50
		print('-50 points')
	elif total_number_of_all_sublinks >= 150:
		points[true_hmpg] -= 25
		print('-25 points')


### Takes the "keywords.txt" file and creates a list of these keywords. Also makes sure to get the lowercase version of these keywords
def get_keywords_list():
	with open('keywords.txt') as keywords:
		list_of_keywords = []
		for line in keywords:
			line = line.strip('\n')
			list_of_keywords.append(line[:-2]) ## 27/7
			score_values[line[:-2]] = int(line[-1:]) ## 27/7
			list_of_keywords.append(line.lower()[:-2])
			score_values[line[:-2].lower()] = int(line[-1:])

	return list_of_keywords


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


### Searches through the sublinks of a website.
### Search is based on thoroughness. i.e. thoroughness of 1 means every sublink is scraped, thoroughness of 3 means every third sublink is scraped.
def search_through_multiple_links_to_find_keyword_matches(homepage, _2D_list_of_sublinks, thoroughness, num_websites_checked,\
 num_matches, list_of_keywords, interested_tabs): ##
	results = []
	for list_of_sublinks in _2D_list_of_sublinks:
		for i in range(len(list_of_sublinks)):
			if i % thoroughness == 0:
				html_contents_indices_where_products_pages_can_be, html_contents, matches = find_keyword_matches_on_website(homepage, list_of_sublinks[i],\
					False, num_websites_checked, list_of_keywords, interested_tabs)
				other_options = False
				for j in range(len(html_contents)):
					if html_contents[j] != '\n' and not (str(type(html_contents[j])) == "<class 'bs4.element.Comment'>")\
					and not (str(type(html_contents[j])) == "<class 'bs4.element.NavigableString'>")\
					and not isinstance(html_contents[j], str):
						if not other_options:
							if '404' in html_contents[j].get_text():
								try:
									print(list_of_sublinks)
									print('Error 404: ' + list_of_sublinks[i])
									print('Next link tried in its place: ' + list_of_sublinks[i + 1])
									html_contents_indices_where_products_pages_can_be, html_contents, matches = find_keyword_matches_on_website(homepage, list_of_sublinks[i + 1],\
									False, num_websites_checked, list_of_keywords, interested_tabs)
									num_websites_checked[0] -= 1
									num_matches[1] += matches
									num_404_pages[0] += 1
									other_options = True
								except IndexError:
									pass
				if other_options == False:
					num_matches[1] += matches


### Writes all the sublinks to "list_of_product_links.txt".
### Note that every new website deletes all previous content in "list_of_product_links.txt". 
def write_product_links(_2D_list_of_sublinks, interested_tabs): ##
	with open('list_of_product_links.txt', 'w') as file:
		for i in range(len(_2D_list_of_sublinks)):
			file.write(interested_tabs[i] + '\n')
			list_of_sublinks = _2D_list_of_sublinks[i]
			for link in list_of_sublinks:
				file.write(link + '\n')


### Calculates the number of actual tabs found on the website from "interested_tabs".
### An actual tab has sublinks attatched to the tab.
def calculate_website_structure_score(_2D_list_of_sublinks, interested_tabs, true_hmpg):
	for i in range(len(_2D_list_of_sublinks)):
		list_of_sublinks = _2D_list_of_sublinks[i]
		if len(list_of_sublinks) >= 1:
			website_structure[true_hmpg] += 1


### Finds all sublinks of the page tab that contains the text "parents_html_text".
def find_html_content_of_a_given_html_text(parents_html_text, html_contents, indices_where_text_can_be_found): ## ---
	_2D_list_of_sublinks = []
	list_of_sublinks = []

	for parent_html_text in parents_html_text:
		for i in indices_where_text_can_be_found:
			relevant_html_contents = html_contents[i]
			for child in relevant_html_contents.descendants:
				if child.string != None:
					if parent_html_text in child.string or parent_html_text.lower() in child.string:
						find_sublinks(child, i, list_of_sublinks)
		_2D_list_of_sublinks.append(list_of_sublinks)
		list_of_sublinks = []
	print('---')
	print(_2D_list_of_sublinks)

	return _2D_list_of_sublinks


### Helper function for find_html_content_of_a_given_html_text()
def find_sublinks(html_contents, i, list_of_sublinks): ## ---
	if str(type(html_contents)) == "<class 'bs4.element.Comment'>":
		return

	if html_contents.parent.name == 'a':
		html_contents = html_contents.parent

	try:
		link = html_contents.get('href')
		if link != '#' and link != None and 'javascript:void' not in link:
			list_of_sublinks.append(link)
	except:
		pass

	try:
		new_parent = html_contents.find_next_sibling()
	except TypeError:
		return
	except AttributeError:
		new_parent = html_contents


	if new_parent == None:
		return

	all_a_html = new_parent.find_all('a')
	for a in all_a_html:
		link = a.get('href')
		if link != None and 'javascript:void' not in link:
			list_of_sublinks.append(link)

	return list_of_sublinks


### Takes the list of sublinks and reformats it into a more convenient format
def refine_list(_2D_list_of_sublinks): ##
	new_2D_list_of_sublinks = []
	new_list_of_sublinks = []
	for list_of_sublinks in _2D_list_of_sublinks:
		for i in range(len(list_of_sublinks)):
			try:
				sub_section_length = len(list_of_sublinks[i])
			except TypeError:
				sub_section_length = 0
			for j in range(sub_section_length):
				new_list_of_sublinks.append(list_of_sublinks[i][j])
		new_2D_list_of_sublinks.append(new_list_of_sublinks)
	return new_2D_list_of_sublinks


### Uses several other functions in this program to aggregate their tasks
### Searches a website's homepage. Finds the product links and searches those too. Calculates the score of the company.
def search_a_website_and_the_sublinks(homepage, interested_tabs, thoroughness):
	global num_matches
	num_matches = [0, 0]
	global num_websites_checked
	num_websites_checked = [0]
	do_you_want_to_know_indices_where_product_pages_can_be = True

	list_of_keywords = get_keywords_list()

	true_hmpg = true_homepage(homepage)

	scores[true_hmpg] = 0
	website_structure[true_hmpg] = 0

	html_contents_indices_where_products_pages_can_be, html_contents, num_matches[0] = find_keyword_matches_on_website(homepage, homepage, True,\
	 num_websites_checked, list_of_keywords, interested_tabs)
	_2D_list_of_sublinks = find_html_content_of_a_given_html_text(interested_tabs, html_contents, html_contents_indices_where_products_pages_can_be)

	write_product_links(_2D_list_of_sublinks, interested_tabs)
	calculate_website_structure_score(_2D_list_of_sublinks, interested_tabs, true_hmpg)

	search_through_multiple_links_to_find_keyword_matches(homepage, _2D_list_of_sublinks, thoroughness, num_websites_checked, num_matches,\
	 list_of_keywords, interested_tabs)

	print('Number websites checked: ' + str(num_websites_checked[0]))

	scores[true_hmpg] /= num_websites_checked[0]


### Takes "websites_to_scrape.txt" and returns a list of the websites in this file.
def read_website_links():
	websites = []

	file = open('websites_to_scrape.txt', 'r')
	for line in file:
		websites.append(line.strip('\n'))
	return websites


def save_points_from_website():
	file = open('points_from_website.txt', 'w')
	for website in points:
		file.write(str(website) + ' ' + str(points[website]) + '\n')
	file.close


def save_keyword_matches(website):
	true_hmpg = true_homepage(website)
	file = open('keyword_matches_from_website_to_website.txt', 'a')
	if len(keyword_matches) > 0:
		file.write(true_hmpg)
		for keyword in keyword_matches:
			file.write(' ' + keyword)
		file.write('\n')
	file.close()


def save_tab_matches(website):
	print('***')
	print(tab_matches)
	true_hmpg = true_homepage(website)
	file = open('tab_matches_to_website.txt', 'a')
	if len(tab_matches) > 0:
		file.write(true_hmpg)
		for tab in tab_matches:
			file.write(' ' + tab)
		file.write('\n')
	file.close()


def reset_bad_tabs_bad_text():
	for key in bad_tabs_and_bad_text:
		bad_tabs_and_bad_text[key] = 0


###Main function. This is where the program starts.
def main(interested_tabs, thoroughness, _bad_tabs_and_bad_text):
	global bad_tabs_and_bad_text
	bad_tabs_and_bad_text = _bad_tabs_and_bad_text

	### Temporarily opened to allow the files to be appended to later ('a' vs. 'w')
	file = open('keyword_matches_from_website_to_website.txt', 'w')
	file.close()
	file = open('tab_matches_to_website.txt', 'w')
	file.close()

	### Goes through all the websites and runs "search_a_website_and_the_sublinks" for each site.
	### Sets and resets various values for each website too
	websites = read_website_links()
	for website in websites:
		if website != '' and website != None:
			print('Checking website: ' + website)
			global list_of_possible_scores_to_add
			list_of_possible_scores_to_add = [] ### All scores from all keywords in all sublinks
			global keyword_matches
			keyword_matches = [] ### List of keywords that show up for the website in question. Only used to save to file
			global tab_matches
			tab_matches = [] ### List of tab matches that show up for the website in question. Only used to save to file
			reset_bad_tabs_bad_text()
			try:
				search_a_website_and_the_sublinks(website, interested_tabs, thoroughness)
			except Exception as e:
				print('Failed to search website: ' + website)
				print('Exception received: ')
				print(e)
				print('')
				list_of_possible_scores_to_add = [0]
				website_structure[true_homepage(website)] = 0

			add_keyword_matches_to_points(list_of_possible_scores_to_add, website)
			add_bad_tab_and_bad_text_matches_to_points(website)
			add_tab_matches_to_points(website)
			save_keyword_matches(website)
			save_tab_matches(website)
	
	time.sleep(0.1)

	save_points_from_website()

	print(points)


#main(['Products', 'Services', 'Applications', 'Industries', 'Sectors'], 1000)
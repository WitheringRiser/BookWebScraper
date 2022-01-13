###                             VPN Tester by Lukas Brazdeikis                      
###                                     Created 6/8/21                                  
###                                  Last modified 6/8/21                              
### Run this program before you start scraping to see if your VPN's IP address is valid. 
### If you don't check if your VPN's IP address is valid, the program may crash due to inability
### to google company names. 
### Inputs: 
###		- None
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


from googlesearch import search
import random

### A list of random search terms to test whether the IP address won't be blocked by google when you run RunEntireProgram.py
global google_search_test_terms
google_search_test_terms = ['Siemens AG', 'Ecolab USA Inc', 'Atotech Deutschland GmbH', 'Belenos Clean Power Holding AG', \
'Imertech SAS', 'Tubacex Innovacion AIE', 'Chongqing Dayou Surface Technology Co Ltd', \
'Chongqing Dayou Surface Technology Co Ltd', 'Hyundai Motor Co', 'Johnson and Johnson Surgical Vision Inc', \
'Molecular Templates Inc', 'Herzberg, Mark C.', 'Nitto Belgium NV', 'Contemporary Amperex Technology Co Ltd', \
'Hitachi GE Nuclear Energy Ltd', 'Huawei Technologies Co Ltd', 'BASF SE', 'Marrone Bio Innovations Inc', \
'Telefonaktiebolaget LM Ericsson AB', 'JFE Steel Corp', 'JFE Steel Corp', \
'Federal State Unitary Enterprise "Mining and Chemical Combine" (FSUE "MCC")', 'Tyco Electronics Raychem GmbH', \
'Hexagon Technology Center GmbH', 'Popit Oy', 'Kone Corp', 'Hewlett Packard Enterprise Development LP', 'LG Electronics Inc', \
'Comelit Group SpA', 'Spacelabs Healthcare LLC', 'Philip Morris Products SA', 'Murata Machinery Ltd', \
'Kawasaki Heavy Industries Co Ltd', 'Korea Hydro and Nuclear Power Co Ltd', 'Honeywell International Inc', 'Ethicon LLC', \
'Kaipo Chen', 'Beijing Surgerii Technology Co Ltd', 'LG Electronics Inc', 'Koninklijke Philips NV']


### Input: num_searches_to_check (int), google_pause_length (int)
### Output: boolean
def is_IP_valid(num_searches_to_check, google_pause_length):
	for i in range(num_searches_to_check):
		try:
			run_google_search(google_search_test_terms[i], google_pause_length)
		except RuntimeError:
			print(e)
			return False
	return True


### Input: percentage value (int between 0 and 100)
### Output: offset (int close to 1)
###		- offset is a random number close to 1 with an offset between 0 and the percentage.
def random_offset(percentage):
	offset = 0.01 * random.randint(100 - percentage, 100 + percentage)
	return offset


### Takes a company name, does a google search, and returns a list of the top 10 search results.
### Input: query (string), google_pause_length (int)
### Output: None. However, global variable good_links is modified with the addition of the best link from the search
def run_google_search(query, google_pause_length):
	links = ['Google search for "' + query + '" in this sublist.']
	for result in search(query, tld="com", num=10, stop=10, pause=google_pause_length * random_offset(10)):
		links.append(result)


### Input: is_valid (boolean)
### Output: None. However, a print statement is made
def print_validity(is_valid):
	print('Is IP address valid?: ' + str(is_valid))


### Input: None.
### Output: None
def main():
	num_searches_to_check = 10 ## Number of google searches to make to determine if IP is valid. 10 is recommended. Max 40
	google_pause_length = 5 ## Pause between each google search. Recommended to keep between 3 and 5.

	is_valid = is_IP_valid(num_searches_to_check, google_pause_length)
	print_validity(is_valid)


main()
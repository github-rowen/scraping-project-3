import requests
from bs4 import BeautifulSoup
import time
import pandas as pd

base_url = 'https://webscraper.io'
start_url = 'https://webscraper.io/test-sites/e-commerce/static'

r = requests.get(start_url)
soup = BeautifulSoup(r.content, 'lxml')
#main navigation menu
menu = []
#sub-navigation menu of main nav menu
sub_menu = []
#get all the links in side-menu and store in the list 'menu'
side_menu = soup.find('ul', id='side-menu').find_all('li')
for href_val in side_menu:
	menu.append(base_url + href_val.a['href'])
#loop in all the links in main menu
#get all links in sub menu
#start loop in second item
for nav_link in menu[1:]:
	r = requests.get(nav_link)
	soup = BeautifulSoup(r.content, 'lxml')
	#get all sub menu links in the active menu
	#then store the links in the list 'sub_menu'
	active_nav = True
	while active_nav:
		li_active = soup.find('li', class_='active').find('ul').find_all('li')
		for sub_nav in li_active:
			sub_menu.append(base_url + sub_nav.a['href'])
		#set to False if done getting links of sub menu
		#to exit while loop	
		active_nav = False

names = []
prices = []
descriptions =[]
ratings = []
categories = []
for item in sub_menu:
		#store item in page for update later
		page = [item]
		#get the category name
		name_type = page[0].split('/')
		category = name_type[-2] + '/' + name_type[-1]

		print(item)#for debugging
			
		loop_page = True
		while loop_page:
			#use while loop to get all sub menu page
			r = requests.get(page[0])
			soup = BeautifulSoup(r.content, 'lxml')
			
			div = soup.find_all('div', class_='col-sm-4 col-lg-4 col-md-4')
			#get all the desired data	
			for data in div:
				name = data.find('a', class_='title')['title']
				names.append(name)
				
				price = data.find('h4', class_='price').text
				prices.append(price)
				
				description = data.find('p', class_='description').text
				descriptions.append(description)
				
				rating = data.find('div', class_='ratings').find('p', class_='pull-right').text.split()[0]
				ratings.append(int(rating))
				
				categories.append(category)
			#check if the next button is disabled
			pagination = soup.find('ul', class_='pagination').find_all('li')
			#accessing the next button
			#and getting the value of its attribute 'class'
			nxt_page_btn = pagination[-1]['class']
			if 'disabled' not in nxt_page_btn:
				#uodate/change the value of page first item 'page[0]'
				page[0]= base_url  + pagination[-1].a['href']
				
				print(page[0])#for debugging
				#time.sleep(4)
			else:
				#set to False to exit in the while loop
				loop_page = False

df = pd.set_option('max_rows', None, 'max_columns', None)
#create a data frame
df = pd.DataFrame({
	'category': categories,
	'names': names,
	'prices': prices,
	'descriptions': descriptions,
	'ratings': ratings
})
		
#print(df)
#df.to_csv('product.csv', index=False)
df.to_excel('product.xlsx', index=False)

print('done!')
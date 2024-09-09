#!/usr/bin/env python
# coding: utf-8

# In[1]:


from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException, TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
import time
from random import randint
from playsound import playsound


# In[5]:


def login():
	path = '/Users/inika/Selenium Webdrivers/chromedriver'
	driver = webdriver.Chrome(path)

	username = " "
	password = " "

	driver.get('https://discord.com')
	wait = WebDriverWait(driver, 10)
	time.sleep(3)
	
	retries = 3
	for i in range(retries):
		try:
			print("Attempting Login #{}..".format(i+1))
			driver.find_element_by_link_text("Login").click()
			time.sleep(2)
			mail = driver.find_element_by_name("email")
			pwd = driver.find_element_by_name("password")
			mail.send_keys(username)
			pwd.send_keys(password)
			pwd.submit()
			break

		# except NoSuchElementException:
		# 	driver.find_element_by_link_text("Open").click() 

		except (TimeoutException, NoSuchElementException) as e:
			print("Failed. Retrying...")
			time.sleep(2)
			continue

	return driver,wait

def goToServer(server):
	servers = wait.until(ec.presence_of_all_elements_located((By.XPATH,"//div[@class = 'listItem-2P_4kh']")))[2:-4]
	for s in servers:
		a = s.find_element_by_tag_name('a')
		try:
			if a.get_attribute("aria-label")==server:
				a.click()
				break
		except StaleElementReferenceException:
			print("No such Server")
			
def goToChannel(channel):
	channels = wait.until(ec.presence_of_all_elements_located((By.CLASS_NAME,"name-3_Dsmg")))
	for c in channels:
		if c.text == channel.lower():
			c.click()
			
def sendMessage(message): #sends message and for bot messages, checks if it triggered an event
	current_channel = driver.find_element_by_xpath("//h3[@class = 'title-29uC1r base-1x0h_U size16-1P40sf']").text
	textbox = wait.until(ec.presence_of_element_located((By.XPATH,'//div[@aria-label = "Message #'+current_channel+'"]')))
	textbox.send_keys(message)
	textbox.send_keys(Keys.RETURN)
	if 'pls' in message and 'why my pls rich' not in message:
		time.sleep(1)
		events()
	
def clear(n=10):
	n = len(driver.find_elements_by_xpath("//div[@class = 'markup-2BOw-j messageContent-2qWWxC']"))
	if n>0:
		# while(n!=0):
		sendMessage('!clear '+str(n))
		time.sleep(4)
			# n = len(driver.find_elements_by_xpath("//div[@class = 'markup-2BOw-j messageContent-2qWWxC']"))

def frogSearch(safe):
	sendMessage('pls dep all')
	clear()
	sendMessage('pls search')
	unsafes = ['sewer','dumpster','car','street','hospital','dog']
	good_places = ['dresser','bed','mailbox','couch']
	places = [i.text for i in driver.find_elements_by_xpath("//div[@class = 'markup-2BOw-j messageContent-2qWWxC']//code")]
	for i in unsafes:
		if i in places:
			places.remove(i)
	if len(places)!=0:
		i=-1
		for p in good_places:
			if p in places:
				i = places.index(p)
				break
		if i<0:
			randint(0,len(places)-1)
		sendMessage(places[i])
	else:
		sendMessage('pls pet pat')
	time.sleep(1)
	#result
	msgs = driver.find_elements_by_xpath("//div[@class = 'markup-2BOw-j messageContent-2qWWxC']")
	for msg in msgs:
		if 'area searched' in  msg.text.lower():
			print("Result: ",msg.text.split('\n')[-1])

def postMeme():
	memes = ['n','e','r','d']
	sendMessage('pls pm')
	sendMessage(memes[randint(0,len(memes)-1)])
	events()
	time.sleep(1)
	msgs = driver.find_elements_by_xpath("//div[@class = 'markup-2BOw-j messageContent-2qWWxC']")
	for msg in msgs:
		if 'your meme' in  msg.text.lower():
			print("Result: ",msg.text)
			if 'laptop is broken' in msg.text.lower():
				sendMessage('pls withdraw 1000')
				sendMessage('pls buy laptop')
				print("Bought laptop for 1000 coin")

def fish():
	sendMessage('pls fish')
	time.sleep(1)
	msgs = driver.find_elements_by_xpath("//div[@class = 'markup-2BOw-j messageContent-2qWWxC']")
	for msg in msgs:
		if 'fish is too strong' in  msg.text.lower():
			t = msg.find_element_by_xpath("./code").text
			sendMessage(t)
			print(msg.text)
			playsound('/Users/inika/Downloads/notify.mp3')
			print("Typed: ",t)
			msgs = driver.find_elements_by_xpath("//div[@class = 'markup-2BOw-j messageContent-2qWWxC']")
			
	#result
	for msg in msgs:
		if 'cast out your line' in  msg.text.lower():
			print("Result: ",msg.text.split('\n')[0])

def events():
	event = False
	try:
		time.sleep(2)
		li = driver.find_elements_by_xpath("//div[@class = 'markup-2BOw-j messageContent-2qWWxC']")
		for i in range(len(li)):
			x = li[i].text.lower()
			if "event " in  x or "common event" in x or "rare event" in x and "lookout for " not in x:
				event = True
				playsound('/Users/inika/Downloads/notify.mp3')
				break

		if event:
			event1=li[i]
			event2=li[i+1]
			print(event1.text)
			print(event2.text)
			response = event2.find_element_by_xpath(".//code").text
			sendMessage(response)
			
			if "hit" in event2.text or 'boss' in event2.text.lower():
				for _ in range(7):
					sendMessage(response)           

			wait_long = WebDriverWait(driver, 40)
			try:
				msgs = wait_long.until(ec.presence_of_all_elements_located((By.XPATH,"//div[@class = 'embedFieldValue-nELq2s']")))
			except TimeoutException:
				clear()
				return
			for msg in msgs:
				if 'Morticia' in msg.text:
					print("Result: ",msg.text) 
					clear()      
				
	except NoSuchElementException:
			pass
		
	except StaleElementReferenceException:
		pass


def bot():
	clear(100)
	prefix = 'pls '
	commands = [prefix+c for c in ['beg','fish','pm','search']]
	petcommands = [prefix+'pet '+c for c in ['feed','wash','play','pat']] 
	while True:
		for com in commands:
			clear()
			if 'pm' in com:
				postMeme()
			elif 'search' in com:
				frogSearch(safe = True)
			elif 'fish' in com:
				fish()
			else:
				sendMessage(com)        
		time.sleep(7)


# In[ ]:


driver,wait = login()
goToServer('sandcastle')
goToChannel('spam')
bot()


# In[ ]:





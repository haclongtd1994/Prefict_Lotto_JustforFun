from selenium import webdriver as wd
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

class Interactive_Website:
	def __init__(self):
		self.driver = wd.Firefox()

	def open_url(self, URL_Link):
		self.driver.get(URL_Link)
		self.url = URL_Link

	def Wait_page_load(self, type, element, timeout):
		fail = 0
		try:
			if type=="id":
				element_present = EC.presence_of_element_located((By.ID, element))
			elif type=="classname":
				element_present = EC.presence_of_element_located((By.CLASS_NAME, element))
			elif type=="xpath":
				element_present = EC.presence_of_element_located((By.XPATH, element))
			elif type=="xpath_click":
				element_present = EC.element_to_be_clickable((By.XPATH, element))
			elif type=="id_invi":
				element_present = EC.invisibility_of_element_located((By.ID, element))
			WebDriverWait(self.driver, timeout).until(element_present)
		except TimeoutException:
			print("Page loaded too much time, timeout !!")
			fail = 1
		finally:
			if(fail!=1):
				print("Page loaded: "+self.url+"\r\n Find with Type: "+type+"\t Element: "+element)

	def Click_Event(self, type, element):
		if type=="xpath":
			Target = self.driver.find_element_by_xpath(element)
		elif type=="id":
			Target = self.driver.find_element_by_id(element)
		elif type=="atag":
			Target = self.driver.find_element_by_link_text(element)
		Target.click()

#iw = Interactive_Website()
#URL = "https://stackoverflow.com/questions/18421280/selenium-python-click-on-element-nothing-happens"
#iw.open_url(URL)
#iw.Wait_page_load("id", "nav-tags", 5)
#iw.Click_Event("id", "nav-tags")


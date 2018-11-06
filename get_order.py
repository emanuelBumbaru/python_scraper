from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
import time
from sets import Set

def savetUrls(links, file):
  f=open(file, "w")
  for url in links:
    f.write(url+"\n")
  f.close()

    

links=set()
options = Options()
options.headless = True
driver = webdriver.Firefox(options=options, executable_path=r'/usr/bin/geckodriver')
driver.get('https://www.thermofisher.com/uk/en/home/order/lab-instruments-equipment.html')


html = driver.page_source
f=open("test_order.html", "w")
f.write(unicode(html).encode('utf-8'))
f.close()

continue_link = driver.find_element_by_tag_name('a')
elems = driver.find_elements_by_xpath("//a[@href]")
for elem in elems:
    el=elem.get_attribute("href")
    print("url", el)
    links.add(el)
savetUrls(links, "links.txt")
   
driver.quit()



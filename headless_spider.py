from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from tinydb import TinyDB, Query
import time
from furl import furl
import json

def getFilename(url):
  url=str(url)
  try:
    ind=url.rfind('/')
    if ind=='-1':
      return url
    else:
      return url[ind+1:len(url)]
  except ValueError:
   pass
   print ("error, incorrect url")


def saveUrl(url, filename, sourcex):
  if filename=="":
    """get the name of downloaded file"""
    filename=getFilename(url)
    if filename[len(filename)-5:len(filename)]!=".html":
      filename=filename+".html"  
    #filename=filename.replace(".", "_")
    print ("filename: data/"+filename)

  if filename=="":
    filename="index.html"
  
  with open("data/"+filename, "w") as f: 
    f.write(str(sourcex))

def sameDomain(url, url_ref):
  if url.strip().find(url_ref)==0:
    return '1'
  else:
    return '0'

def to_absolute(url, base):
    """If given ``url`` is a relative path,
    make it relative to the ``base``.
    """
    furled = furl(url)
    if not furled.scheme:
        return furl(base).join(url).url
    return url


def is_same_origin(*urls):
    """Check whether URLs are from the same origin (host:port)."""
    origins = set(url.netloc for url in map(furl, urls))
    return len(origins) <= 1


def ParseProductPage(source_page):
  print ("ok")
    
def getPageLinks(extUrl):
  #print ("url:", extUrl)

  links=set()
  options = Options()
  options.headless = True
  driver = webdriver.Firefox(options=options, executable_path=r'/usr/bin/geckodriver')
  driver.get(extUrl) 
  source_page=driver.page_source
  #print ("source_page:", source_page)

  """save the downloaded url for future analyze"""
  saveUrl(extUrl, "", source_page)

  """open small local .json db for rapid indexed search and easy data manipulation"""
  db = TinyDB('db.json')
  Urls = Query()
  #check if the url in database!?
  resp_dbi=db.search(Urls.url == str(extUrl))
  if str(resp_dbi)=="[]":
    db.insert({'url': str(extUrl), 'same_domain': '1', 'downloaded':'1', 'tmst':str( int(time.time()) ) })
  else:
    db.update({'downloaded':'1', 'tmst':str( int(time.time()) )}, Urls.url == str(extUrl))

  """search for links"""
  continue_link = driver.find_element_by_tag_name('a')
  elems = driver.find_elements_by_xpath("//a[@href]")
  for elem in elems:
    el=elem.get_attribute("href")
    """remove duplicated urls from the list in the same page"""
    print ("url extracted:", el)
    links.add(el)
  
  for link in links:  
    #print("url", link)
    same_domain=sameDomain(link, 'https://www.thermofisher.com/')
    resp_db=db.search(Urls.url == str(link))
    if str(resp_db)=="[]":
      db.insert({'url': str(url), 'same_domain': same_domain, 'downloaded':'0', 'tmst':''})
    """parse product attributes"""
    if "/product/" in url:
      getParseProductPage(source_page)


  """get the next URLs from database"""
  resp_dbi=db.search( (Urls.same_domain == '1') &  (Urls.downloaded == '0'))[0]
  resp_dbi=str(resp_dbi).replace("'", "\"")
  #print ("resp_dbi:", resp_dbi)
  text = json.loads(resp_dbi.strip())
  #print ("search url:", text['url'])
  getPageLinks(text['url'])
  

  """close the http connection""" 
  driver.quit()

#init the crawler
url='https://www.thermofisher.com/uk/en/home/order/lab-instruments-equipment.html'
getPageLinks(url)








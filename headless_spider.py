from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
import sqlite3
import time
import json
import subprocess
from bs4 import BeautifulSoup

def parseBreadcrumb(cont):
  soup = BeautifulSoup(cont, 'html.parser')
  """ search for div container with class container-breadcrumb """
  breadcrumb = soup.find("div", { "class" : "container-breadcrumb" })
  #print (breadcrumb)
  soup = BeautifulSoup(str(breadcrumb), 'html.parser')
  text = soup.get_text()
  text=text.strip()
  text=text.replace("\n", "")
  text=text.replace("\t", "")
  text=text.replace("  ", "")
  return text

def parseSpecs(cont):
  l=list()
  soup = BeautifulSoup(cont, 'html.parser')
  specs = soup.find("table", id="pdp-specifications-table")
  soupb = BeautifulSoup(str(specs), 'html.parser')
  attr_list=soupb.find_all('tr')
  for el in attr_list:
    soupc = BeautifulSoup(str(el), 'html.parser')
    attr_name_tag=soupc.find('th')
    attr_name=attr_name_tag.get_text()
    atrr_name=str(attr_name).strip()
    attr_value_tag=soupc.find('td')
    attr_value=attr_value_tag.get_text()
    attr_value=str(attr_value).strip()
    print ("attr_name:", "Specifications - "+attr_name, ", attr_value:", attr_value)
    #print ("*el:*", el)
    l.append([attr_name, attr_value])
  return l 


def parseCatalog(source):
  soup = BeautifulSoup(cont, 'html.parser')
  specs = soup.find("table", id="pdp-catalog-table")



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

  
  
  #looking for attribute and value
  

   

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
    return 1
  else:
    return 0


def ParseProductPage(source_page):
  print ("ok")
    
def getPageLinks(extUrl):
  print ("url:", extUrl)

  links=set()
  options = Options()
  options.headless = True
  driver = webdriver.Firefox(options=options, executable_path=r'/usr/bin/geckodriver')
  driver.get(extUrl)
  time.sleep(15) 
  source_page=driver.page_source
  #print ("source_page:", source_page)

  """save the downloaded url for future analyze"""
  saveUrl(extUrl, "", source_page)

  """open small local sqlite db for rapid indexed search and easy data manipulation"""
  conn = sqlite3.connect('data.db')
  c = conn.cursor()
  db_url=""
  #check if the url in database!?
  for row in c.execute("select url from links where url ='"+str(extUrl)+"'"):
    db_url = row[0]
    #print ("*db_url", db_url)

  if db_url=="" and str(extUrl)!="":
    qi="insert into links(url, same_domain, downloaded, tmst) values ('"+str(extUrl)+"', 1, 1, '"+str( int(time.time()) )+"')"
    #print ("qix:", qi)
    c.execute(qi)
    conn.commit()
  if db_url!="" and str(extUrl)!="":
    qu="update links set same_domain=1, downloaded=1, tmst='"+str( int(time.time()) )+"' WHERE url= '"+str(extUrl)+"'"
    c.execute(qu)
    conn.commit()
 
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
    dbxu_url=""
    cursor = c.execute("select url from links where url='"+str(link).strip()+"'")
    for row in cursor:
      dbxu_url=row[0]
    
    #print ("dbxu_url", dbxu_url)
    if dbxu_url=="" and link!="":
      try:
        qi="insert into links(url, downloaded, same_domain, tmst) values ('"+str(link)+"', 0, "+str(same_domain)+",  '')"
        #print ("qi:", qi)
        c.execute(qi)
        conn.commit()
      except ValueError as e:
        pass
        #print link+" url already existing into db" #sqlite3.IntegrityError: UNIQUE constraint failed: links.url
        print ('My exception occurred, value:', e.value)
      

    """parse product attributes"""
    if "/product/" in url:
      getParseProductPage(source_page)      
 
  """close the http connection""" 
  driver.quit()
  subprocess.call("killall -9 /usr/lib/firefox/firefox", shell=True)
  subprocess.call("killall -9 /usr/bin/geckodriver", shell=True)



  """get the next URLs from database"""
  dbx_url=""
  for row in c.execute("select url from links where same_domain='1' and downloaded = 0"):
    dbx_url = row[0]

  c.close()
  conn.close()
  

  print ("dbx_url:", dbx_url)
  getPageLinks(dbx_url)
  


#init the crawler
url='https://www.thermofisher.com/uk/en/home/order/lab-instruments-equipment.html'
getPageLinks(url)








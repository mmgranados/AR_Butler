from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import urllib3
import ast

# options = EdgeOptions()
# options.use_chromium = True

# driver = Edge(options = options)
async def get_url_contents():

  # open json file, get name and ronin address
  
  url = 'https://axiesworld.firebaseapp.com/updateSpecific?wallet=0xb84f6ce22ab46d5204935ff212ac32f0a49267c4'

  http = urllib3.PoolManager()
  response = http.request('GET', url)
  soup = BeautifulSoup(response.data.decode('utf-8'), features="html5lib")
  
  # body = soup.find('body').contents
  body = str(soup.find('body').string)
  
  # the_contents_of_body_without_body_tags = body.findChildren(recursive=False)
  print(type(body))
  print(body)

  dict = ast.literal_eval(body)
  print(type(dict))
  print(dict)

  elo = dict.get('walletData').get('pvpData').get('elo')
  print(elo)
  

  




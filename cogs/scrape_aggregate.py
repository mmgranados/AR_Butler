from discord.ext import commands
from bs4 import BeautifulSoup
import pandas as pd
import urllib3
import ast

import json


SCHOLAR_LIST_NAME = []
SCHOLAR_LIST_AVGSLP = []
SCHOLAR_LIST_MMR = []
SCHOLAR_DATA_COMBINED = []

# options = EdgeOptions()
# options.use_chromium = True

# driver = Edge(options = options)
async def get_url_contents_aggregate(ctx, ronin_list):

  # open json file, get name and ronin address
  # leaderboards = {}

  # scholar_scraped = 0
  # loop = 0
  # error = 0

  url_combined_addresses = "https://game-api.axie.technology/mmr/"
  address = 0
  
  for ronin_address in ronin_list:

    print(ronin_address)

    url_combined_addresses += ronin_address
    if  address < len(ronin_list)-1:
      url_combined_addresses += ","

    address += 1

    # http = urllib3.PoolManager()
    # response = http.request('GET', url)
    # soup = BeautifulSoup(response.data.decode('utf-8'), features="html5lib")
    
    # # body = soup.find('body').contents
    # body = str(soup.find('body').string)
    
    # # the_contents_of_body_without_body_tags = body.findChildren(recursive=False)
    # # print(type(body))
    # # print(body[1:-1])

    # # print(body[0])
    
    # try:
    #   dict = json.loads(str(body[1:-1]))
    #   # print(type(dict))
    #   # print(dict)

    # except Exception as e:
    #   error += 1
    #   print(e)

    # if scholar_scraped % 25 == 0:
    #   await ctx.send("Scraped {} scholar MMR info".format(scholar_scraped), delete_after = 3)

    # print(elo)
    
  http = urllib3.PoolManager()
  response = http.request('GET', url_combined_addresses)
  print(response)

  soup = BeautifulSoup(response.data.decode('utf-8'), features="html5lib")
  print(soup)

  body = str(soup.find('body').string)
  # print(type(body))
  # body2 = body.replace("false", "False")
  # body2 = body2.replace("true", "True")
  # print(body2)
  # body3 = eval(str(body2))
  
  list_of_dicts = json.loads(body)
  # print(body2)
  print(list_of_dicts)
  print(type(list_of_dicts))
  
  # print(list_of_dicts)
  
  leaderboards = {}
  error = 0
  scholar_scraped = 0
  for dict in list_of_dicts: 
    try:
        
        # print(type(dict))
        # print(dict)        
        name = dict.get('items')[1].get('name')
        elo = dict.get('items')[1].get('elo')
        leaderboards[name] = elo
        scholar_scraped += 1

    except Exception as e:
      error += 1
      print(e)

    if scholar_scraped % 25 == 0:
      await ctx.send("Scraped {} scholar MMR info".format(scholar_scraped), delete_after = 3)

  print("error")
  print(error)
  print(leaderboards)
    
  # await ctx.send("Scraped {} scholar MMR info, failed to get {}".format(scholar_scraped, error))

  # sort_leaderboards = sorted(leaderboards.items(), key = lambda x:x[1], reverse = True)
  # print(sort_leaderboards)

  # return sort_leaderboards
  return leaderboards
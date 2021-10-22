from discord.ext import commands
from bs4 import BeautifulSoup
import pandas as pd
import urllib3

import json


SCHOLAR_LIST_NAME = []
SCHOLAR_LIST_AVGSLP = []
SCHOLAR_LIST_MMR = []
SCHOLAR_DATA_COMBINED = []

# options = EdgeOptions()
# options.use_chromium = True

# driver = Edge(options = options)
async def get_url_contents(ctx, ronin_table):

  # open json file, get name and ronin address
  leaderboards = {}

  scholar_scraped = 0
  loop = 0
  error = 0

  for ronin_address in ronin_table:

    print(ronin_address)

    url = f"https://game-api.axie.technology/mmr/0x{ronin_address}"
    http = urllib3.PoolManager()
    response = http.request('GET', url)
    soup = BeautifulSoup(response.data.decode('utf-8'), features="html5lib")
    
    # body = soup.find('body').contents
    body = str(soup.find('body').string)
    
    # the_contents_of_body_without_body_tags = body.findChildren(recursive=False)
    # print(type(body))
    # print(body[1:-1])

    # print(body[0])
    
    
    try:
      dict = json.loads(str(body[1:-1]))
      # print(type(dict))
      # print(dict)
      
      
      name = dict.get('items')[1].get('name')
      elo = dict.get('items')[1].get('elo')
      leaderboards[name] = elo
      scholar_scraped += 1
      loop += 1

    except Exception as e:
      error += 1
      print(e)

    if scholar_scraped % 25 == 0:
      await ctx.send("Scraped {} scholar MMR info".format(scholar_scraped), delete_after = 3)

    # print(elo)
    
    
  await ctx.send("Scraped {} scholar MMR info, failed to get {}".format(scholar_scraped, error))

  sort_leaderboards = sorted(leaderboards.items(), key = lambda x:x[1], reverse = True)
  print(sort_leaderboards)

  return sort_leaderboards

  

  




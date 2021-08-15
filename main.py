# import discord related library - discord.py
import discord
import aiohttp
import asyncio
from discord.ext import tasks, commands

# login thru token
import os

# initializes a discord api client
intents = discord.Intents().all()
intents.members = True
bot = commands.Bot(command_prefix='!', intents=intents)


import gspread
import pandas as pd

# for multithreading of scheduled tasks
# datetime - determine date and time
import threading
from threading import Timer
from datetime import datetime, timedelta

TIME_DAILY_RESET = 18 # 18TH HR, 6PM
# contains name and user ID 
RECORDS_DISCORD_SCHOLARS = {}
# 
DICT_ROLES_SCHOLAR = {}
SCHOLAR_LIST_AVGSLP = []
SCHOLAR_LIST_NAME = []
DIAMOND = 300
PLATINUM = 250
GOLD = 200
SILVER = 150
BRONZE = 100
IRON = BRONZE - 0.000000000001

# AxieReinassance server/Guild ID
AR = 864496916317995058

SCHOLAR_ROLE_ID = 864513212027895851



#######################
# Credentials code
gc = gspread.service_account(filename='nifty-expanse-322112-bd87c03b16c7.json')
########################

# standalone message sending function
# does not require action from discord client
# uses tasks extension from discord
# client.wait_until_ready() to avoid RunTimeWarning
# source here: "https://stackoverflow.com/questions/54518397/multiple-get-request-using-asyncio-and-aiohttp-with-timeout-period"
# async def send_message():
#   # waits until client is ready 
#   await client.wait_until_ready()
#   channel = client.get_channel(867560997673762837)
#   msg_sent = False
#   if not msg_sent:
#     try:  
#       await channel.send('testing send_message function')
#       msg_sent = True
#     except Exception:
#       print("Something went wrong in send_message")
#       return
#   return



## General function for spreadsheet retrieval
def get_info(): 
  # get the instance of the Spreadsheet
  # open by means of URL
  sheet_scholars = gc.open_by_url('https://docs.google.com/spreadsheets/d/1baDqcluSAw_jbbwBoPFvzkCrV84jn0wkBUzl0rl9Do0/edit#gid=0')
  
  if sheet_scholars:
    print("google sheet file accessed")

  # get the first sheet of the Spreadsheet
  sheet_scholars_instance = sheet_scholars.get_worksheet(0)

  if sheet_scholars_instance:
    print("1st sheet accessed")

  # get all the records of the scholars data
  records_data = sheet_scholars_instance.get_all_records()


  # view scholars data
  #records_data

  # converts the scholar data from json to dataframe
  records_df = pd.DataFrame.from_dict(records_data)
  global SCHOLAR_LIST_NAME
  global SCHOLAR_LIST_AVGSLP
  SCHOLAR_LIST_NAME = records_df['Name'].tolist()
  SCHOLAR_LIST_AVGSLP = records_df["Average per day"] 
  
  print("finished get_info test")


  # view top records
  # records_df.head()
  # t2 = threading.Thread(target = send_message)
  # t2.start()
  # return

# Iterate through name list and avgslp list at the same time
# set role for every item - scholar
def eval_ranks():
  for name, slp_avg in zip(SCHOLAR_LIST_NAME, SCHOLAR_LIST_AVGSLP):
    if avg >= DIAMOND:
      set_rank(name, "Diamond")
    elif avg >= PLATINUM:
      set_rank(name, "Platinum")
    elif avg >= GOLD:
      set_rank(name, "Gold")
    elif avg >= SILVER:
      set_rank(name, "Silver")
    elif avg >= BRONZE:
      set_rank(name, "Bronze") 
    elif avg < IRON:
      set_rank(name, "Iron") 
    
#    
def set_rank(name, rank):
  DICT_ROLES_SCHOLAR[name] = rank

def set_roles_discord(name, rank):

  print("set roles function not yet implemented")
  pass

@bot.command(name = 'update')
@commands.has_permissions(manage_roles=True)
async def get_channel_members(ctx):
  #Get info of users
  # access global record of discord scholars
  global RECORDS_DISCORD_SCHOLAR
  global AR
  guild = bot.get_guild(AR)
  await ctx.send("Fetching roles from Discord...")
  for member in guild.get_role(SCHOLAR_ROLE_ID).members:
    RECORDS_DISCORD_SCHOLARS[member.name] = member.id

  t1 = threading.Thread(target = eval_ranks)
  t1.start()

  t1.join()

  #  try to update 
  try:
    await ctx.send("Trying to update scholar info from gsheets...")
    get_info()
  except Exception:
    await ctx.send("Something went wrong while retrieving info from google sheets")
  await ctx.send("Internal scholar list updated")


   
  for member in bot.get_all_members():
    pass
  #   if member.name in guild.role.members:
  #     print(member)
  #   break
    # if 'Scholar' in member.roles:
    #   RECORDS_DISCORD_SCHOLARS[member.name] = member.id

  
  print(RECORDS_DISCORD_SCHOLARS)  

# called everytime to refresh timer
# timer is set to go off 6 PM every time
# https://stackoverflow.com/questions/15088037/python-script-to-do-something-at-the-same-time-every-day
# timedelta(days=1) to account for end of month transition days
def set_timer_interval():
  x = datetime.today()
  y = x.replace(day=x.day, hour=18, minute=0, second=0, microsecond=0) + timedelta(days=1)
  delta_t = y - x
  secs = delta_t.total_seconds()
  return secs


@bot.event
async def on_ready():
  print("We have logged in as {0.user}".format(bot))
  

# @bot.event
# async def on_message(message):
#   if message.author == bot.user:
#     return

#   if message.content.startswith('$hello'):
#     try:
#       await message.channel.send('hello')
#     except Exception:
#       return

#   if "fuck you" in message.content:
#     await message.channel.send('you motherfucker')
#     return

#     asyncio.sleep(30)
#   # TO DO 
#   # reply to DMs 
#   # reply to DMS with their stats for the week

# Loop for reset timer
# after t1 thread stops, 1s passes then another loop of t1 stars
@tasks.loop(seconds = 3600) # repeat every after 
async def rank_reset_timer_loop():

  await bot.wait_until_ready()
  # channel = client.get_channel(867560997673762837)
  # msg_sent = False
  # if not msg_sent:
  #   try:  
  #     await channel.send('testing send_message function')
  #     msg_sent = True
  #   except Exception:
  #     print("Something went wrong in send_message")
  #     return

  # secs = set_timer_interval()
  # t1 = Timer(30, get_info)
  # t1.start()
  # await asyncio.sleep(30)
  # print("sleep done")
  # print("left off on line 144, find way for async loop to finish after thread 1 finishes")

  # rank_reset_timer_loop.change_interval(seconds=5)
  # documentation of change_interval at "https://discordpy.readthedocs.io/en/stable/ext/tasks/index.html?highlight=sleep#discord.ext.tasks.Loop.change_interval"



# background task
# answer at : "https://stackoverflow.com/a/66753449/14691207"
rank_reset_timer_loop.start()
my_secret = os.environ['TOKEN']
bot.run(my_secret)




if __name__ == "__main__":
  main()



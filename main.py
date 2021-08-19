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
DICT_ROLES_CHANGE_SCHOLAR = {}
SCHOLAR_LIST_AVGSLP = []
SCHOLAR_LIST_NAME = []
# AR_ROLE_LIST = ["Diamond", "Platinum", "Gold", "Silver", "Bronze", "Iron"]
AR_ROLE_LIST = []
DICT_ROLENAME_TO_ID = {'Diamond': 870158644686245949, 'Platinum': 870158382613544980, 'Gold': 870157782282813500, 'Silver': 870157342447128656, 'Bronze': 870157202701299712, 'Iron': 870156327824011275}
DIAMOND = 210
PLATINUM = 160
GOLD = 125
SILVER = 100
BRONZE = 75
IRON = BRONZE - 0.000000000001

# AxieReinassance server/Guild ID
AR = 864496916317995058

SCHOLAR_ROLE_ID = 864513212027895851


#######################
# Credentials code
gc = gspread.service_account(filename='nifty-expanse-322112-bd87c03b16c7.json')
########################


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

  # converts the scholar data from json to dataframe
  records_df = pd.DataFrame.from_dict(records_data)
  global SCHOLAR_LIST_NAME
  global SCHOLAR_LIST_AVGSLP
  # split usernames on the # sign. 
  new_name = records_df['Name'].str.split('#', 1, expand=True)
  
  SCHOLAR_LIST_NAME = new_name[0].tolist()
  print(SCHOLAR_LIST_NAME)
  SCHOLAR_LIST_AVGSLP = records_df["Average per day"].tolist()
  # for name, slpavg in zip(SCHOLAR_LIST_NAME, SCHOLAR_LIST_AVGSLP):
  #   print("{}, {}".format(name, slpavg)) 
  
  print("finished get_info test")


# Iterate through name list and avgslp list at the same time
# set role for every item - scholar
def eval_ranks():
  for name, slp_avg in zip(SCHOLAR_LIST_NAME, SCHOLAR_LIST_AVGSLP):
    if slp_avg >= DIAMOND:
      set_rank(name, "Diamond")
    elif slp_avg >= PLATINUM:
      set_rank(name, "Platinum")
    elif slp_avg >= GOLD:
      set_rank(name, "Gold")
    elif slp_avg >= SILVER:
      set_rank(name, "Silver")
    elif slp_avg >= BRONZE:
      set_rank(name, "Bronze") 
    elif slp_avg < IRON:
      set_rank(name, "Iron") 


# assigns rank - name becomes key and value becomes rank
# Dictionary
def set_rank(name, rank):
  DICT_ROLES_CHANGE_SCHOLAR[name] = rank


async def set_roles_discord(scholar, rank):
  try:
    for role in AR_ROLE_LIST:
      await scholar.remove_roles(role, atomic=True)
    await scholar.add_roles(rank)

    print("Changed the rank of {} to {}".format(scholar, rank.name))
  except Exception as e:
    print(e)
    # print("Scholar is of {}".format(type(scholar)))
    print("Failed to Change the rank of {}".format(scholar))


# used by typing !update
@bot.command(name = 'update')
@commands.has_any_role("Admin", "Facilitator")  # Checks if user has Admin or Facilitator role
async def get_channel_members(ctx):
  #Get info of users
  # access global record of discord scholars
  global RECORDS_DISCORD_SCHOLAR
  global AR
  guild = bot.get_guild(AR)
  await ctx.send("Fetching roles from Discord...")
  for member in guild.get_role(SCHOLAR_ROLE_ID).members:
    RECORDS_DISCORD_SCHOLARS[member.name] = member.id

  #  try to update from gsheets
  try:
    await ctx.send("Trying to update scholar info from gsheets...")
    get_info()
    print("Scholar info from gsheets loaded")
  except Exception as e:
    print("Something went wrong while retrieving info from google sheets")
    print(str(e))
    await ctx.send("Something went wrong while retrieving info from google sheets")
  await ctx.send("Internal scholar list updated")

  # Initiates eval_ranks
  # catches error 
  try:
    eval_ranks()
    await ctx.send("Successfully evaluated new ranks")
    print(DICT_ROLES_CHANGE_SCHOLAR)
  except Exception as eval_error:
    print(eval_error)
    await ctx.send("Error in evaluating ranks")

  # Get equivalent discord id of each scholar
    # use id to get Member object/user object
    # pass on Member/User object to use remove_roles
  global AR_ROLE_LIST
  AR_ROLE_LIST = [] # EMPTY LIST OF ROLES
  for value in DICT_ROLENAME_TO_ID.values():
    role = guild.get_role(value)
    AR_ROLE_LIST.append(role)
  print(AR_ROLE_LIST)

  # While computing, displays a typing status in Discord
  async with ctx.typing():
    for key, value in DICT_ROLES_CHANGE_SCHOLAR.items():
      try:
        scholar_id = RECORDS_DISCORD_SCHOLARS[key]
        # print("checkpoint 0") ########### CHECKPOINT 0 #########
        # return member object from id
        scholar = guild.get_member(scholar_id)
        # print("checkpoint 1")
        rank = guild.get_role(DICT_ROLENAME_TO_ID[value]) # guild.get_role to get role object
        await set_roles_discord(scholar, rank)  # function for changing roles in discord 
      except Exception as error: 
        ...
        pass
        print(error)
        await ctx.send("Error changing the role of {}".format(error))
        print("Something went wrong while changing roles")

  await asyncio.sleep(1)
  print(RECORDS_DISCORD_SCHOLARS)  
  await ctx.send("Done assigning ranks")


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


my_secret = os.environ['TOKEN']
bot.run(my_secret)


if __name__ == "__main__":
  main()



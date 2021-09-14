
from discord.ext import commands

import asyncio
import time

import cogs.scholar_data as scdata
import cogs.rank_module as rank_mod

RECORDS_DISCORD_SCHOLARS = {}
# 
SCHOLAR_LIST_AVGSLP = []
SCHOLAR_LIST_NAME = []
# AR_ROLE_LIST = ["Diamond", "Platinum", "Gold", "Silver", "Bronze", "Iron"]
AR_ROLE_LIST = []
DICT_ROLENAME_TO_ID = {'Diamond': 870158644686245949, 'Platinum': 870158382613544980, 'Gold': 870157782282813500, 'Silver': 870157342447128656, 'Bronze': 870157202701299712, 'Iron': 870156327824011275}

DICT_ROLES_CHANGE_SCHOLAR = {}
SCHOLAR_LIST_NAME = []
SCHOLAR_LIST_AVGSLP = []
server = None


SCHOLAR_ROLE_ID = 864513212027895851

servers = []

class guild_data(commands.Cog):

  def __init___(self, bot):
    self.bot = bot


  # Async function
  # takes scholar (Object) and rank (object) as parameter
  async def set_roles_discord(self, scholar, rank):
    """
    1. Removes all rank-related roles
    2. add rank-related role that's passed on as rank parameter 
    """
    try:
      # Remove all roles of the member that belongs to the AR_ROLE_LIST list (list of objects)
      # set intersections
      list_to_set_scholar_roles = set(scholar.roles) 
      list_to_set_ranks = set(AR_ROLE_LIST)
      await asyncio.sleep(0.1)
    
      # Checks for common role in the scholar role and the ranks set by the bot
      # if intersection is not empty, remove element.
      list_common_role = list(list_to_set_ranks.intersection(list_to_set_scholar_roles))
      if list_common_role:
        for common_role in list_common_role:
          await scholar.remove_roles(common_role, atomic=True)
        
      # https://stackoverflow.com/questions/59825/how-to-retrieve-an-element-from-a-set-without-removing-it
      try:
        await scholar.add_roles(rank)
      except Exception as role_change_error:
        print(role_change_error)

      print("Updated the rank of {} to {}".format(scholar, rank.name))
    except Exception as e:
      print(e)
      # print("Scholar is of {}".format(type(scholar)))
      print("Failed to Change the rank of {}".format(scholar))


  # command issued by typing !update
  @commands.command(name = 'roleupdate')
  @commands.has_any_role("Admin", "Facilitator")  # Checks if user has Admin or Facilitator role
  async def get_channel_members(self, ctx):
    """ 
    Updates the rank of members in server
    Steps:
    1. identify server in which the command originates
    2. Fetches the members in the discord server
    3. Obtains data from gsheets of scholar that comes from the scholarship tracker
    4. Evaluate ranks of scholar based on data from sheets
    5. get rolename ids from global var
    6. update roles for each scholar
    """

    # 1. identify server in which the command originates
    print(ctx)
    print(ctx.guild)
    global SERVER
    SERVER = ctx.guild
    print(SERVER)
    await ctx.send(SERVER)
    # global servers
    # for guild in self.bot.guilds:
    #   servers.append(guild)
    # print(servers)
      # self.servers.append(guild)
      # await ctx.send(guild)
  #   #Get info of users
  #   # access global record of discord scholars
    global RECORDS_DISCORD_SCHOLAR
    global AR
    
    # 2. Fetches the members in the discord server
    for member in SERVER.get_role(SCHOLAR_ROLE_ID).members:
      RECORDS_DISCORD_SCHOLARS[member.name] = member.id

    # 3. Obtains data from gsheets of scholar that comes from the scholarship tracker
    #  try to update from gsheets
    try:
      await ctx.send("Trying to update scholar info from gsheets...")
      big_array = scdata.get_info()
      
      global SCHOLAR_LIST_NAME
      global SCHOLAR_LIST_AVGSLP

      SCHOLAR_LIST_NAME = big_array[0]
      SCHOLAR_LIST_AVGSLP = big_array[1]

      print("Scholar info from gsheets loaded")
    except Exception as e:
      print("Something went wrong while retrieving info from google sheets")
      print(str(e))
      await ctx.send("Something went wrong while retrieving info from google sheets")
    await ctx.send("Internal scholar list updated")

    # 4. Evaluate ranks of scholar based on data from sheets
    # Initiates eval_ranks
    try:
      global DICT_ROLES_CHANGE_SCHOLAR
      DICT_ROLES_CHANGE_SCHOLAR = rank_mod.eval_ranks(SCHOLAR_LIST_NAME, SCHOLAR_LIST_AVGSLP)

      await ctx.send("Successfully evaluated new ranks")
      print(DICT_ROLES_CHANGE_SCHOLAR)
    except Exception as eval_error:
      print(eval_error)
      await ctx.send("Error in evaluating ranks")

    # Get equivalent discord id of each scholar
      # use id to get Member object/user object
      # pass on Member/User object to use remove_roles
    # 5. get rolename ids from global var  
    global AR_ROLE_LIST
    AR_ROLE_LIST = [] # EMPTY LIST OF ROLES
    for value in DICT_ROLENAME_TO_ID.values():
      role = SERVER.get_role(value)
      AR_ROLE_LIST.append(role)
    print(AR_ROLE_LIST)

    # 6. update roles for each scholar
    # While computing, displays a typing status in Discord
    async with ctx.typing():
      # initialize timer on current time
      start_time = time.time()
      i_scholar = 0 # count scholars
      print(DICT_ROLES_CHANGE_SCHOLAR)
      for key, value in DICT_ROLES_CHANGE_SCHOLAR.items():
        i_scholar += 1
        print(i_scholar)
        try:
          scholar_id = RECORDS_DISCORD_SCHOLARS[key]
          # print("checkpoint 0") ########### CHECKPOINT 0 #########
          # return member object from id
          scholar = SERVER.get_member(scholar_id)
          print(scholar)
          # print("checkpoint 1")
          rank = SERVER.get_role(DICT_ROLENAME_TO_ID[value]) # guild.get_role to get role object
          await self.set_roles_discord(scholar, rank)  # function for changing roles in discord 
        except Exception as error: 
          ...
          pass
          print(error)
          await ctx.send("Error changing the role of {}".format(error))
          print("Something went wrong while changing roles")

    time_elapsed = time.time() - start_time
    print("the time needed for {} scholars is {}, average time is {} per scholar".format(time_elapsed, i_scholar, time_elapsed / i_scholar))
    await asyncio.sleep(1)

    print(RECORDS_DISCORD_SCHOLARS)  
    await ctx.send("Done assigning ranks")


def setup(bot):
    bot.add_cog(guild_data(bot))
    print('I am being loaded!')
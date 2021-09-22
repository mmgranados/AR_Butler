import discord
from discord.ext import commands

import asyncio
import time

import cogs.scholar_data as scdata
import cogs.rank_module as rank_mod
import cogs.scrape as scrape

RECORDS_DISCORD_SCHOLARS = {}
# 
SCHOLAR_LIST_AVGSLP = []
SCHOLAR_LIST_NAME = []
# AR_ROLE_LIST = ["Diamond", "Platinum", "Gold", "Silver", "Bronze", "Iron"]
ROLE_LIST = []

AR = {'Diamond Dragon': 870158644686245949, 'Platinum Wand': 870158382613544980, 'Gold Battle Axe': 870157782282813500, 'Silver Axe': 870157342447128656, 'Bronze Hammer': 870157202701299712, 'A Little Chick': 870156327824011275}

CRIMROO = {"Diamond Dragon": 889041995337703456, "Platinum Wand": 889045017740607508,  "Gold Battle Axe": 889046161728622612, "Silver Axe": 889092868050919536, "Bronze Hammer": 889093021214339093,  
"A Little Chick": 889093193050779708}

# Use guild.name as key to access roles
DICT_ROLENAME_TO_ID = {"AxieRenaissance Scholarship Program": AR, "Crimroo Axie Tambayan": CRIMROO}

DICT_ROLES_CHANGE_SCHOLAR = {}
SCHOLAR_LIST_NAME = []
SCHOLAR_LIST_AVGSLP = []
SCHOLAR_LIST_MMR = []
SCHOLAR_LIST_RONIN = []
SERVER = None

AR_SCHOLAR_ID = 864513212027895851
CRIMROO_SCHOLAR_ID = 880113245367697419
SCHOLAR_ROLE_ID = {"AxieRenaissance Scholarship Program": AR_SCHOLAR_ID, "Crimroo Axie Tambayan": CRIMROO_SCHOLAR_ID}


servers = []

# class Servers():

#   def __init___(self):
#     self.serverlist = {}
  
#   def add(self, guild):
#     if guild not in self.serverlist:
#       rolelist = guild.roles


class GuildData(commands.Cog):

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
      list_to_set_ranks = set(ROLE_LIST)
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

  async def identify_server(self, ctx):
    print(ctx)
    print(ctx.guild)
    global SERVER
    SERVER = ctx.guild
    print(SERVER)
    await ctx.send(SERVER)


  async def fetch_data_discord(self, ctx):
    """
    1. Fetches the members in the discord server
    2. assigns them in the dictionary with display_name as key and 
    member id as value
    """
    
    # access global record of discord scholars
    global RECORDS_DISCORD_SCHOLAR
    global AR

    for member in SERVER.get_role(SCHOLAR_ROLE_ID.get(SERVER.name)).members:
      RECORDS_DISCORD_SCHOLARS[member.display_name] = member.id
      

  async def fetch_data_gsheets(self, ctx):
    try:
      await ctx.send("Trying to update scholar info from gsheets...")
      big_array = scdata.get_info()
      
      global SCHOLAR_LIST_NAME
      global SCHOLAR_LIST_AVGSLP
      global SCHOLAR_LIST_MMR 
      global SCHOLAR_LIST_RONIN

      SCHOLAR_LIST_NAME = big_array[0]
      SCHOLAR_LIST_AVGSLP = big_array[1]
      SCHOLAR_LIST_MMR = big_array[2]
      SCHOLAR_LIST_RONIN = big_array[3]

      # print(SCHOLAR_LIST_MMR) # DEBUGGING PURPOSES
      # print(SCHOLAR_LIST_RONIN) # DEBUGGING PURPOSES
      # print("mmr list size is {}".format(len(SCHOLAR_LIST_MMR)))
      # print("ronin list size is {}".format(len(SCHOLAR_LIST_RONIN)))

      print("Scholar info from gsheets loaded")
    except Exception as e:
      print("Something went wrong while retrieving info from google sheets")
      print(str(e))
      await ctx.send("Something went wrong while retrieving info from google sheets")
    await ctx.send("Internal scholar list updated")
    

  async def evaluate_members(self, ctx):
    """ 
    Tries to access data of scholar that is stored and runs 
    algorithm for rank evaluation of members. Outputs data 
    that will be used for changing roles in discord to corresponding
    rank.
    """
    try:
      global DICT_ROLES_CHANGE_SCHOLAR
      DICT_ROLES_CHANGE_SCHOLAR = rank_mod.eval_ranks(SCHOLAR_LIST_NAME, SCHOLAR_LIST_MMR)

      await ctx.send("Successfully evaluated new ranks")
  
      print(DICT_ROLES_CHANGE_SCHOLAR)
    except Exception as eval_error:
      print(eval_error)
      await ctx.send("Error in evaluating ranks")
      

  async def get_rolelist_discord(self, ctx):
    """
    1. Get equivalent discord id of each scholar
    2. use id to get Member object/user object
    3. pass on Member/User object to use remove_roles
    4. get rolename ids from global var  
    """

    global ROLE_LIST
    ROLE_LIST = [] # EMPTY LIST OF ROLES
    for value in DICT_ROLENAME_TO_ID[SERVER.name].values():
      role = SERVER.get_role(value)
      ROLE_LIST.append(role)
    print("Final role list")
    print(ROLE_LIST)

  async def update_roles_discord(self, ctx):
    async with ctx.typing():
      # initialize timer on current time
      start_time = time.time()
      
      print("Rank final list")
      print(DICT_ROLES_CHANGE_SCHOLAR)

      i_scholar = 0 # count scholars
      errors = 0 # get number of role assigning errors
      for key, value in DICT_ROLES_CHANGE_SCHOLAR.items():
        i_scholar += 1
        
        try:
          scholar_id = RECORDS_DISCORD_SCHOLARS.get(key)
          if scholar_id == None:
            errors += 1
            continue
  
          # return member object from id
          scholar = SERVER.get_member(scholar_id)
          print("{}, {}".format(i_scholar, scholar))  # prints scholar info in terminal

          rank = SERVER.get_role(DICT_ROLENAME_TO_ID.get(SERVER.name).get(value)) # guild.get_role to get role object
          await self.set_roles_discord(scholar, rank)  # function for changing roles in discord 
        except Exception as error: 
          ...
          pass
          print(error)
          error +=1
          await ctx.send("Error changing the role of {}".format(error))
          print("Something went wrong while changing roles")

    end_time = time.time() - start_time 
    if i_scholar == 0:
      i_scholar = 0.01

    print("It took {} secs to update {} scholar ranks, averaging {} per scholar ".format(end_time, i_scholar, float(end_time) / i_scholar ))
    print(RECORDS_DISCORD_SCHOLARS)  
    await ctx.send("Done assigning ranks of {} scholars, failed assigning ranks to {}".format(i_scholar, errors))



  @commands.command(name = 'butler_help')
  @commands.has_any_role("Admin", "Facilitator", "Dev", "Mod", "Moderator")  # Checks if user has Admin or Facilitator role
  async def butler_help(self, ctx):
    """
    Usage: !butler_help
    function: prints out the commands of the bot
    """

    await ctx.send(f"prefix: ! ")
    
    for cmd in self.walk_commands():
      if cmd.help:
        await ctx.send(f"Command: !{cmd.qualified_name}, \n {cmd.help}")
    
    
  @commands.command(name = 'give_role')
  @commands.has_any_role("Admin", "Facilitator", "Dev", "Mod", "Moderator")  # Checks if user has Admin or Facilitator role
  async def give_role(self, ctx, name, role, reason = "No reason"):
    
    """
    Format: !give_role [member(don't tag)] [reason (optional)] 
    Assigns role to member
    """
    mem = ctx.guild.get_member_named(name)
    roles_list = ctx.guild.roles
    print(roles_list)
    role_needed = roles_list[[dc_role.name for dc_role in roles_list].index(role)]
    # print(type(role_needed)) - debug
    if role_needed is not None:
      await mem.add_roles(role_needed)
      await ctx.send(f"{name} was given the role of {role}")

    print(role_needed)

  @commands.command(name = 'update_info')
  @commands.has_any_role("Admin", "Facilitator", "Dev", "Mod", "Moderator")  # Checks if user has Admin or Facilitator role
  async def scrapeweb(self,ctx):
    await scrape.get_url_contents()
   

  # command issued by typing !update
  @commands.command(name = 'roleupdate')
  @commands.has_any_role("Admin", "Facilitator", "Dev", "Mod", "Moderator")  # Checks if user has Admin or Facilitator role
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
    global SERVER
    await self.identify_server(ctx)

    await asyncio.sleep(0.1)

    # 2. Fetches the members in the discord server
    await self.fetch_data_discord(ctx)
    
    # 3. Obtains data from gsheets of scholar that comes from the scholarship tracker
    #  try to update from gsheets
    await self.fetch_data_gsheets(ctx)
    
    # 4. Evaluate ranks of scholar based on data from sheets
    # Initiates eval_ranks
    await self.evaluate_members(ctx)

    # 5. get rolename ids from global var  
    await self.get_rolelist_discord(ctx)

    # 6. update roles for each scholar
    # While computing, displays a typing status in Discord
    
    await self.update_roles_discord(ctx)
    

def setup(bot):
    bot.add_cog(GuildData(bot))
    print('I am being loaded!')
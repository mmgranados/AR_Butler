# import discord related library - discord.py
import discord
import asyncio
from discord.ext import tasks, commands
from discord.ext.commands import Bot

# Web server for 24/7 hosting
import keep_alive

# login thru token
import os

# initializes a discord api client
intents = discord.Intents().all()
intents.members = True
bot = commands.Bot(command_prefix='!', intents=intents)



# from cogs.guild_data import guild_data

TIME_DAILY_RESET = 18 # 18TH HR, 6PM
# contains name and user ID 


# # AxieReinassance server/Guild ID
# AR = 864496916317995058

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

# server to keep bot alive (done by pinging every 30 mins)
keep_alive.keep_alive()

bot.load_extension("cogs.guild_data")

my_secret = os.environ['TOKEN']
bot.run(my_secret, reconnect=True)


if __name__ == "__main__":
  main()



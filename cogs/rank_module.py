DIAMOND = 2300
PLATINUM = 2000
GOLD = 1500
SILVER = 1200
BRONZE = 1000
IRON = BRONZE - 1


DICT_ROLES_CHANGE_SCHOLAR = {}

def set_rank(name, rank):
    """
    Assigns rank and appends to dictionary -- name becomes key and value becomes rank
    """
    global DICT_ROLES_CHANGE_SCHOLAR
    DICT_ROLES_CHANGE_SCHOLAR[name] = rank


# Iterate through name list and avgslp list at the same time
# set role for every item - scholar
def eval_ranks(SCHOLAR_LIST_NAME, SCHOLAR_LIST_MMR):
  """
  - Evaluates rank based on slp earnings
  - calls set_rank to assign ranks into dictionary 
  - Return: Dictionary - contains name of scholars as key, rank as value 
  """

  for name, mmr in zip(SCHOLAR_LIST_NAME, SCHOLAR_LIST_MMR):
    if mmr >= DIAMOND:
      set_rank(name, "Diamond Dragon")
    elif mmr >= PLATINUM:
      set_rank(name, "Platinum Wand")
    elif mmr >= GOLD:
      set_rank(name, "Gold Battle Axe")
    elif mmr >= SILVER:
      set_rank(name, "Silver Axe")
    elif mmr >= BRONZE:
      set_rank(name, "Bronze Hammer") 
    elif mmr < IRON:
      set_rank(name, "A Little Chick")
  
  # Return final list of ranks
  print(DICT_ROLES_CHANGE_SCHOLAR)
  return DICT_ROLES_CHANGE_SCHOLAR
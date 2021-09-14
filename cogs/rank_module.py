DIAMOND = 210
PLATINUM = 160
GOLD = 125
SILVER = 100
BRONZE = 75
IRON = BRONZE - 0.000000000001


DICT_ROLES_CHANGE_SCHOLAR = {}

def set_rank(name, rank):
    """
    Assigns rank and appends to dictionary -- name becomes key and value becomes rank
    """
    global DICT_ROLES_CHANGE_SCHOLAR
    DICT_ROLES_CHANGE_SCHOLAR[name] = rank


# Iterate through name list and avgslp list at the same time
# set role for every item - scholar
def eval_ranks(SCHOLAR_LIST_NAME, SCHOLAR_LIST_AVGSLP):
  """
  - Evaluates rank based on slp earnings
  - calls set_rank to assign ranks into dictionary 
  - Return: Dictionary - contains name of scholars as key, rank as value 
  """

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
  
  # Return final list of ranks
  print(DICT_ROLES_CHANGE_SCHOLAR)
  return DICT_ROLES_CHANGE_SCHOLAR
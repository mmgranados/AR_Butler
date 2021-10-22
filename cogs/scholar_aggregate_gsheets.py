#######################
import pandas as pd
import gspread  ## module for spreadsheet manipulation
# Credentials code
gc = gspread.service_account(filename='nifty-expanse-322112-bd87c03b16c7.json')
########################

SCHOLAR_LIST_NAME = []
SCHOLAR_LIST_AVGSLP = []
SCHOLAR_LIST_MMR = []
SCHOLAR_DATA_COMBINED = []

def get_info(): 
    """ Access spreadsheet containing and records them here for later use. """
  
  # get the instance of the Spreadsheet
  # open by means of URL
    sheet_scholars = gc.open_by_url('https://docs.google.com/spreadsheets/d/1BM4ku2HLSXAgxOBg6h0wBHuNtp7m_kHqZjdKpVbpndo/edit#gid=1627501359')
    
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
    
    # split usernames on the # sign. 
    new_name = records_df['Discord Name'].str.split('#', 1, expand=True)
    
    SCHOLAR_LIST_NAME = new_name[0].tolist()
    # print(SCHOLAR_LIST_NAME)
    
    SCHOLAR_LIST_RONIN = records_df["Ronin Address"].tolist()
    
    # for name, slpavg in zip(SCHOLAR_LIST_NAME, SCHOLAR_LIST_AVGSLP):
    #   print("{}, {}".format(name, slpavg)) 

    SCHOLAR_DATA_COMBINED.append(SCHOLAR_LIST_NAME)
    SCHOLAR_DATA_COMBINED.append(SCHOLAR_LIST_RONIN)

    print("name size is {}".format(len((SCHOLAR_LIST_RONIN)))) 
    print("ronin size is {}".format(len((SCHOLAR_LIST_RONIN)))) 

    print("finished get_info test")
    
    return SCHOLAR_DATA_COMBINED

    
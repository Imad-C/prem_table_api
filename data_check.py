from bs4 import BeautifulSoup
import requests
import pandas as pd

data = pd.read_csv("data/df_total.csv")
check = data[data['Team']=='Manchester United']

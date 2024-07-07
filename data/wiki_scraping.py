"""
scraping Wikipedia for premier league results 
"""

'''importing libraries'''
from bs4 import BeautifulSoup
import requests
import pandas as pd


def remove_affix(team_name: str) -> str: 
    '''Removes the (C) and (R) suffix for 'Champions' and 'Relegated'
    '''
    if ('(C)') in team_name or ('(R)') in team_name:
        team_name = team_name.rsplit(' ', 1)[0]
    return team_name


if __name__ == '__main__':
    '''getting wikipedia addresses from 1992 to 2023'''
    wiki_addresses = []
    
    for year in range(1993, 2024):
        wiki_address = (
            f"https://en.wikipedia.org/wiki/{year-1}"
            f"%E2%80%93{str(year)[-2:]}_Premier_League"
            )
        wiki_addresses.append(wiki_address)
    
    '''scraping addresses'''
    # creating main dataframe
    df_total = pd.DataFrame()
    
    # looping through all addresses
    for address in wiki_addresses:
        
        r = requests.get(address)
        soup = BeautifulSoup(r.text, features = 'lxml')
        
        # finding table
        html_table = soup.find(
            'table', class_ = 'wikitable', style = 'text-align:center;'
            )
        df = pd.read_html(str(html_table))[0]
        
        # cleaning table
        df.rename({df.columns[1] : 'Team'}, axis = 1, inplace = True)
        df['Team'] = df['Team'].apply(remove_affix)
        
        # getting season year from string
        season_string = address.split('/')[-1].split('%')[0]
        season_year = f'{season_string}-{str(int(season_string) + 1)[-2:]}'
        df['Season'] = season_year
        
        #joining to main
        df_total = pd.concat([df_total, df], ignore_index = True)
        
        # progress check below
        print(f'season {season_string}/{str(int(season_string) + 1)[-2:]} complete')
    
    '''export to csv'''
    df_total.to_csv('data/df_total.csv', index = False)
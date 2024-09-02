from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np

def scrape_draft_kings_mlb():
  url = "https://sportsbook.draftkings.com/leagues/baseball/mlb"
  req = requests.get(url)
  soup = BeautifulSoup(req.content, "html.parser")
  # print(soup.title)

  df_mlb = pd.DataFrame(columns=['Team', 'Run Line', 'Total', 'Moneyline'])

  teams = soup.find_all(class_='event-cell__name-text')
  blocks = soup.find_all(class_='sportsbook-table__column-row')

  print(len(blocks))
  for i in range(0, len(blocks), 4):
    team = teams[i // 4].text
    run_line = blocks[i + 1].text
    total = blocks[i + 2].text
    moneyline = blocks[i + 3].text

    print(team, run_line, total, moneyline)
    # Add New Row to Dataframe
    df_mlb.loc[len(df_mlb)] = [team, run_line, total, moneyline]
  
  print(df_mlb)




  



  



def main():
    scrape_draft_kings_mlb()

if __name__ == '__main__':
    main()
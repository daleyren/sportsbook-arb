from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np

def clean_up_team_name(team_name):
    '''
    team_name comes into two formats: CHI Cubs & Chicago Cubs.
    This function strips the raw string to just the team name (i.e -> 'Cubs')
    '''
    # List of possible MLB city abbreviations or full names
    mlb_cities = {
        "CHI", "Chicago", "SD", "San Diego", "LA", "Los Angeles", "BOS", "Boston", "NY", "New York",
        "SF", "San Francisco", "HOU", "Houston", "PHI", "Philadelphia", "TOR", "Toronto", "ATL", "Atlanta",
        "CLE", "Cleveland", "CIN", "Cincinnati", "DET", "Detroit", "MIL", "Milwaukee", "MIN", "Minnesota",
        "OAK", "Oakland", "SEA", "Seattle", "TB", "Tampa Bay", "BAL", "Baltimore", "PIT", "Pittsburgh", 
        "KC", "Kansas City", "TEX", "Texas", "COL", "Colorado", "MIA", "Miami", "WAS", "Washington", 
        "STL", "St. Louis", "ARI", "Arizona", "SJ", "San Jose"
    }

    # Split the team name into words
    words = team_name.split()

    # Check if the first word (or first two words) match any city name/abbreviation
    if ' '.join(words[:2]) in mlb_cities:
        # If the city name is two words long (e.g., "San Diego", "Los Angeles")
        return ' '.join(words[2:])
    elif words[0] in mlb_cities:
        # If the city name is one word or an abbreviation (e.g., "LA", "CHI", "MIA")
        return ' '.join(words[1:])
    else:
        return team_name


def scrape_draft_kings_mlb():
    url = "https://sportsbook.draftkings.com/leagues/baseball/mlb"
    req = requests.get(url)
    soup = BeautifulSoup(req.content, "html.parser")
    # print(soup.title)

    df_mlb = pd.DataFrame(columns=['Team', 'Run Line', 'Total', 'Moneyline'])

    teams = soup.find_all(class_='event-cell__name-text')
    blocks = soup.find_all(class_='sportsbook-table__column-row')

    for i in range(0, len(blocks), 4):
        team = clean_up_team_name(teams[i // 4].text)
        run_line = blocks[i + 1].text
        total = blocks[i + 2].text
        moneyline = blocks[i + 3].text

        # print(team, run_line, total, moneyline)
        # Add New Row to Dataframe
        df_mlb.loc[len(df_mlb)] = [team, run_line, total, moneyline]
    
    print(df_mlb)


def main():
    scrape_draft_kings_mlb()

if __name__ == '__main__':
    main()
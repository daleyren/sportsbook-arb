from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome import service
import undetected_chromedriver as uc
from fake_useragent import UserAgent
import requests

import time
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


def scrape_mlb_draft_kings():
    url = 'https://sportsbook.draftkings.com/leagues/baseball/mlb' # Fairly certain, url is hardset
    req = requests.get(url)
    soup = BeautifulSoup(req.content, "html.parser")
    # print(soup.title)

    df_mlb = pd.DataFrame(columns=['Team', 'Spread', 'Total', 'Moneyline'])

    teams = soup.find_all(class_='event-cell__name-text')
    blocks = soup.find_all(class_='sportsbook-table__column-row')

    for i in range(0, len(blocks), 4):
        team = clean_up_team_name(teams[i // 4].text)
        spread = blocks[i + 1].text
        total = blocks[i + 2].text
        moneyline = blocks[i + 3].text

        # print(team, run_line, total, moneyline)
        # Add New Row to Dataframe
        df_mlb.loc[len(df_mlb)] = [team, spread, total, moneyline]
    
    return df_mlb


def scrape_mlb_caesars():
    '''
    CURRENTLY BLOCKS CONTENT ON DEFAULT SELENIUM (MAY NEED LOGIN/COOKIES/ETC)
    When scraping, requires the window focus to be on the WebDriver tab (can probably game later)
    '''
    # options = webdriver.ChromeOptions()
    # options.page_load_strategy = 'normal' # Used by default, waits for all resources to download
    # options.page_load_strategy = 'eager' # DOM access is ready, but other resources like images may still be loading
    # options.page_load_strategy = 'none' # Does not block WebDriver at all    
    # ua = UserAgent()
    # options = webdriver.ChromeOptions()
    # options.add_argument(f'user-agent={ua.random}')
    # driver = webdriver.Chrome(options=options)

    driver = uc.Chrome()
    url = 'https://sportsbook.caesars.com/us/md/bet/baseball?id=04f90892-3afa-4e84-acce-5b89f151063d'
    driver.get(url)
    time.sleep(3)

    # Scroll Down (NECESSARY - website progressively loads the DOM)
    for i in range(20):  # Adjust the range for more or fewer scrolls
        driver.execute_script("window.scrollBy(0, 150);")  # Scroll down by 500 pixels
        time.sleep(0.1)  # Wait a bit before scrolling again
    
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")

    df_mlb = pd.DataFrame(columns=['Team', 'Spread', 'Total', 'Moneyline'])

    # blocks = soup.find_all(class_='eventContainer')
    blocks = soup.select('.eventContainer:not(.eventHasTournament)')

    for i, block in enumerate(blocks):
        teams = block.find_all(class_='truncate2Rows')
        team_one = clean_up_team_name(teams[0].text)
        team_two = clean_up_team_name(teams[1].text)

        buttons = block.find_all('button')
        spread_one = buttons[0].text
        spread_two = buttons[1].text
        moneyline_one = buttons[2].text
        moneyline_two = buttons[3].text
        total_one = buttons[4].text
        total_two = buttons[5].text
        
        df_mlb.loc[len(df_mlb)] = [team_one, spread_one, total_one, moneyline_one]
        df_mlb.loc[len(df_mlb)] = [team_two, spread_two, total_two, moneyline_two]

        # print(team_one, 'vs', team_two)
    driver.quit()
    return df_mlb

def scrape_mlb_bet_mgm():
    # Will probably have to switch to selenium

    # URL might be subject to change depending on location and other factors
    url = 'https://sports.md.betmgm.com/en/sports/baseball-23/betting/usa-9/mlb-75'
    req = requests.get(url)
    soup = BeautifulSoup(req.content, "html.parser")
    print(soup.title)


    df_mlb = pd.DataFrame(columns=['Team', 'Run Line', 'Total', 'Moneyline'])
    blocks = soup.find_all(class_='grid-event-wrapper has-all-markets image ng-star-inserted')
    # STUFF HERE
    for block in blocks:
        team = block.find_all(class_='participant')
        print(team)

    return df_mlb


def main():
    print(scrape_mlb_draft_kings())
    print(scrape_mlb_caesars())
    # print(scrape_mlb_bet_mgm())

if __name__ == '__main__':
    main()
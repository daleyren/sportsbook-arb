from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome import service
import undetected_chromedriver as uc
from fake_useragent import UserAgent
import requests

import time
import pandas as pd
import numpy as np
import uuid

import multiprocessing as mp


def clean_up_team_name(team_name):
    '''
    team_name comes into two formats: CHI Cubs & Chicago Cubs.
    This function strips the raw string to just the team name (i.e -> 'Cubs')
    '''
    # List of possible MLB city abbreviations or full names
    mlb_cities = {
        "CHI", "Chicago", "SD", "San Diego", "LA", "Los Angeles", "BOS", "Boston", "NY", "New York",
        "SF", "San Francisco", "HOU", "Houston", "PHI", "Philadelphia", "TOR", "Toronto", "ATL",
        "Atlanta", "CLE", "Cleveland", "CIN", "Cincinnati", "DET", "Detroit", "MIL", "Milwaukee",
        "MIN", "Minnesota", "OAK", "Oakland", "SEA", "Seattle", "TB", "Tampa Bay", "BAL",
        "Baltimore", "PIT", "Pittsburgh", "KC", "Kansas City", "TEX", "Texas", "COL", "Colorado",
        "MIA", "Miami", "WAS", "Washington", "STL", "St. Louis", "ARI", "Arizona", "SJ", "San Jose"
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
    
def add_event(curr_event, event_ids, events_df):
    '''
    Takes in a tuple of two teams (in any order). If the event was not already processed, then
    creates a new identifier (uuid) for the event; otherwise, returns the existing identifier.
    '''
    if len(curr_event) != 2:
        raise Exception('Did not receive two teams for the event. Check scraping and parsing!')
    
    if curr_event in event_ids:
        return event_ids[curr_event]
    
    team_one, team_two = curr_event[0], curr_event[1]
    new_event_id = uuid.uuid4()

    event_ids[(team_one, team_two)] = new_event_id
    event_ids[(team_two, team_one)] = new_event_id
    events_df.loc[len(events_df)] = [new_event_id, team_one, team_two]

    return new_event_id


def scrape_mlb_draft_kings(event_ids = None, events_df = None):
    driver = uc.Chrome()
    url = 'https://sportsbook.draftkings.com/leagues/baseball/mlb' # Fairly certain, url is hardset
    driver.get(url)
    # time.sleep(10)
    print('SCRAPED DRAFT KINGS')


def scrape_mlb_caesars(event_ids = None, events_df = None):
    '''
    CURRENTLY BLOCKS CONTENT ON DEFAULT SELENIUM (MAY NEED LOGIN/COOKIES/ETC)
    When scraping, requires the window focus to be on the WebDriver tab (can probably game later)
    '''
    driver = uc.Chrome()
    url = 'https://sportsbook.caesars.com/us/md/bet/baseball?id=04f90892-3afa-4e84-acce-5b89f151063d'
    driver.get(url)
    # time.sleep(10)
    print('SCRAPED CAESARS')


    # # Scroll Down (NECESSARY - website progressively loads the DOM)
    # for i in range(25):  # Adjust the range for more or fewer scrolls
    #     driver.execute_script("window.scrollBy(0, 150);")  # Scroll down by 500 pixels
    #     time.sleep(0.1)  # Wait a bit before scrolling again
    
    # html = driver.page_source
    # soup = BeautifulSoup(html, "html.parser")

    # df_mlb = pd.DataFrame(columns=['Team', 'Spread', 'Total', 'Moneyline', 'Event ID'])

    # # blocks = soup.find_all(class_='eventContainer')
    # blocks = soup.select('.eventContainer:not(.eventHasTournament)')

    # for block in blocks:
    #     teams = block.find_all(class_='truncate2Rows')
    #     team_one = clean_up_team_name(teams[0].text)
    #     team_two = clean_up_team_name(teams[1].text)

    #     chunks = block.find_all(class_='selectionContainer')
    #     spread_one = chunks[0].text
    #     spread_two = chunks[1].text
    #     moneyline_one = chunks[2].text
    #     moneyline_two = chunks[3].text
    #     total_one = chunks[4].text
    #     total_two = chunks[5].text
        
    #     event = (team_one, team_two)
    #     event_id = add_event(event, event_ids, events_df)

    #     df_mlb.loc[len(df_mlb)] = [team_one, spread_one, total_one, moneyline_one, event_id]
    #     df_mlb.loc[len(df_mlb)] = [team_two, spread_two, total_two, moneyline_two, event_id]

    # driver.quit()
    # return df_mlb


def scrape_mlb_bet_mgm(event_ids = None, events_df = None):
    # URL might be subject to change depending on location and other factors
    url = 'https://sports.md.betmgm.com/en/sports/baseball-23/betting/usa-9/mlb-75'

    options = webdriver.ChromeOptions()
    options.page_load_strategy = 'normal' # Used by default, waits for all resources to download
    # options.page_load_strategy = 'eager' # DOM access is ready, but other resources like images may still be loading
    # options.page_load_strategy = 'none' # Does not block WebDriver at all    
    ua = UserAgent()
    options = webdriver.ChromeOptions()
    options.add_argument(f'user-agent={ua.random}')
    driver = webdriver.Chrome(options=options)

    driver.get(url)
    # time.sleep(10)
    print('SCRAPED BET MGM')

    # html = driver.page_source
    # soup = BeautifulSoup(html, "html.parser")
    
    # df_mlb = pd.DataFrame(columns=['Team', 'Spread', 'Total', 'Moneyline', 'Event ID'])
    
    # blocks = soup.find_all('ms-six-pack-event')

    # for block in blocks:
    #     teams = block.find_all(class_='participant')
    #     team_one = teams[0].text.strip()
    #     team_two = teams[1].text.strip()

    #     chunks = block.find_all('ms-option')
    #     spread_one = chunks[0].text
    #     spread_two = chunks[1].text
    #     total_one = chunks[2].text
    #     total_two = chunks[3].text
    #     moneyline_one = chunks[4].text
    #     moneyline_two = chunks[5].text

    #     event = (team_one, team_two)
    #     event_id = add_event(event, event_ids, events_df)

    #     df_mlb.loc[len(df_mlb)] = [team_one, spread_one, total_one, moneyline_one, event_id]
    #     df_mlb.loc[len(df_mlb)] = [team_two, spread_two, total_two, moneyline_two, event_id] 

    # driver.quit()
    # return df_mlb


# Function to set up multiprocessing for DraftKings
def open_draft_kings():
    process = mp.Process(target=scrape_mlb_draft_kings)
    process.start()
    # process.join()

def open_caesars():
    process = mp.Process(target=scrape_mlb_caesars)
    process.start()
    # process.join()

def open_bet_mgm():
    process = mp.Process(target=scrape_mlb_bet_mgm)
    process.start()
    # process.join()

# Get live odds from DraftKings
if __name__ == "__main__":
    open_draft_kings()
    open_caesars()
    open_bet_mgm()
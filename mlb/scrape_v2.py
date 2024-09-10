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


def scrape_mlb_draft_kings(event_ids=None, events_df=None):
    driver = uc.Chrome()
    url = 'https://sportsbook.draftkings.com/leagues/baseball/mlb'
    driver.get(url)
    
    try:
        print('SCRAPED DRAFT KINGS')
        while True:  # Infinite loop to keep it running
            time.sleep(1)  # Keeps the program alive until you manually close it

    except KeyboardInterrupt:
        print("DraftKings scraping interrupted. Closing browser...")
    finally:
        driver.quit()  # Ensures the browser closes when the loop is stopped


def scrape_mlb_caesars(event_ids=None, events_df=None):
    driver = uc.Chrome()
    url = 'https://sportsbook.caesars.com/us/md/bet/baseball?id=04f90892-3afa-4e84-acce-5b89f151063d'
    driver.get(url)
    
    try:
        print('SCRAPED CAESARS')
        while True:
            time.sleep(1)  # Keeps the browser session alive

    except KeyboardInterrupt:
        print("Caesars scraping interrupted. Closing browser...")
    finally:
        driver.quit()


def scrape_mlb_bet_mgm(event_ids=None, events_df=None):
    url = 'https://sports.md.betmgm.com/en/sports/baseball-23/betting/usa-9/mlb-75'
    options = webdriver.ChromeOptions()
    ua = UserAgent()
    options.add_argument(f'user-agent={ua.random}')
    driver = webdriver.Chrome(options=options)

    driver.get(url)

    try:
        print('SCRAPED BET MGM')
        while True:
            time.sleep(1)  # Keeps the browser session alive

    except KeyboardInterrupt:
        print("Bet MGM scraping interrupted. Closing browser...")
    finally:
        driver.quit()


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
    try:
        open_draft_kings()
        open_caesars()
        open_bet_mgm()
        
        # Keep the main program running until manually stopped
        while True:
            time.sleep(1)  # Keeps the program alive, allowing subprocesses to run
        
    except KeyboardInterrupt:
        print("Program interrupted. Exiting...")

    finally:
        # If needed, you can add any cleanup logic here
        print("Shutting down.")
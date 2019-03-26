from selenium import webdriver
import time
import random
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

pd.set_option('display.max_columns', 10000)
pd.set_option('display.max_rows', 10000)
pd.set_option('display.max_colwidth', 10000)
pd.set_option('display.width',1000)

# URL
url = "https://hotels.ctrip.com/hotel/391750.html?isFull=F#ctm_ref=hod_sr_lst_dl_i_1_4"
# Kerry https://hotels.ctrip.com/hotel/347422.html?isFull=F#ctm_ref=hod_sr_lst_dl_n_1_8
# Four Season https://hotels.ctrip.com/hotel/391750.html?isFull=F#ctm_ref=hod_sr_lst_dl_i_1_4

# Notice: MAX_PAGE couldn't be too large
MAX_PAGE = 15

# Define Lists
Score = []
Room_Types = []
Travel_Types = []
Comments = []
Travel_Dates = []

filename = "./Comments_Corpus/Beijing_Four_Season_Comments_total.csv"
# filename = "./Comments_Corpus/Beijing_Kerry_Hotel_Comments_total.csv"


def nextPage(page):
    """
    It is a function to execute Next Page function
    """
    retryNum = 5

    while retryNum >= 0:
        try:
            # page is the page you see right now, what you wanna do is to change to the next page.
            page = page + 1
            # Clear
            browser.find_element_by_id("cPageNum").clear()
            # Send keys
            browser.find_element_by_id("cPageNum").send_keys(page)
            # Click goto button
            browser.find_element_by_id("cPageBtn").click()
            # Sleep for random seconds as waiting for loading
            time.sleep(random.randint(15, 25))
            # Check current page
            currentPage = int(browser.find_element_by_css_selector('a.current').text)

            if currentPage != page:
                retryNum -= 1
                print('Retry!')
                continue
            else:
                break
        except Exception as e:
            assert 'Failed to change to next page'
            return False

def scrap_comments():
    """
    It is a function to scrap User comments, Score, Room types, Dates.
    """
    wait.until(EC.presence_of_element_located((By.ID, 'divCtripComment')))

    html = browser.page_source
    soup = BeautifulSoup(html, "lxml")

    scores_total = soup.find_all('span', attrs={"class":"n"})
    # We only want [0], [2], [4], ...
    travel_types = soup.find_all('span', attrs={"class":"type"})
    room_types = soup.find_all('a', attrs={"class":"room J_baseroom_link room_link"})
    travel_dates = soup.find_all('span', attrs={"class":"date"})
    comments = soup.find_all('div', attrs={"class":"J_commentDetail"})

    # Save score in the Score list
    for i in range(2,len(scores_total),2):
        Score.append(scores_total[i].string)
    # for item in comments:
        # print(item.text)
    # Save travel types in the Travel_Types list
    for item in travel_types:
        Travel_Types.append(item.text)
    # Save room types in the Room_Types list
    for item in room_types:
        Room_Types.append(item.text)
    # Save travel dates in the Travel_Dates list
    for item in travel_dates:
        Travel_Dates.append(item.text)
    # Save comments in the Comments list
    for item in comments:
        Comments.append(item.text.replace('\n', ''))

def save():
    """
    It is a function to save scraped data
    :return: a file
    """
    try:
        if len(Score) == len(Travel_Types) == len(Travel_Dates) == len(Room_Types) == len(Comments):
            data_array = np.array((Score, Travel_Types, Travel_Dates, Room_Types, Comments)).T
            columns = ["Score", "Travel Types", "Travel Dates", "Room Types", "Comments"]
            columns_array = np.array((columns))
            comments_array = np.vstack((columns_array, data_array))
            df = pd.DataFrame(data=data_array)
            df.to_csv(filename, sep='\t', encoding='utf-8-sig', mode='a', header=False, index=False)
        else:
            assert "Length of Lists are not the same, Check carefully!"
            print(len(Score),len(Travel_Types),len(Travel_Dates),len(Room_Types),len(Comments))
    except Exception as e:
        assert e


if __name__ == '__main__':

    print("Please input which page you want to start scraping (start page >= 1):")
    start_page = int(input())

    profile = webdriver.FirefoxProfile()
    profile.accept_untrusted_certs = True
    browser = webdriver.Firefox(firefox_profile=profile)
    browser.get(url=url)
    wait = WebDriverWait(browser, 60)
    time.sleep(random.randint(30,45))
    try:
        wait.until(EC.presence_of_element_located((By.ID, 'divCtripComment')))
    except Exception as e:
        print(e)

    if start_page != 1:
        # First, jump to Page start_page-1
        nextPage(start_page-1)
    for pageIndex in range(start_page,start_page+MAX_PAGE):
        print('It is now Page ', pageIndex)
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'comment_detail_list')))
        scrap_comments()
        nextPage(pageIndex)
    browser.close()

    save()
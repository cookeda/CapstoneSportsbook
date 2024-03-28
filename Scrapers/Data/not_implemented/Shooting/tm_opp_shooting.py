from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC

import undetected_chromedriver as uc
import time
import pandas as pd
import json
from threading import Thread


def scrape_league(self):

    #ra, paint(non-ra), mid, ab3, lc3, rc3, c3, 
    x = 1
    if x == 1:
        ra_m = self.driver.find_element(By.XPATH, f'/html/body/div[1]/div[2]/div[2]/div[3]/section[2]/div/div[2]/div[3]/table/tbody/tr[{x}]/td[2]/text()')
        ra_a = self.driver.find_element(By.XPATH, f'/html/body/div[1]/div[2]/div[2]/div[3]/section[2]/div/div[2]/div[3]/table/tbody/tr[{x}]/td[3]')
        ra_per = self.driver.find_element(By.XPATH, f'/html/body/div[1]/div[2]/div[2]/div[3]/section[2]/div/div[2]/div[3]/table/tbody/tr[{x}]/td[4]')
        paint_m = self.driver.find_element(By.XPATH, f'/html/body/div[1]/div[2]/div[2]/div[3]/section[2]/div/div[2]/div[3]/table/tbody/tr[{x}]/td[5]')
        paint_a = self.driver.find_element(By.XPATH, f'/html/body/div[1]/div[2]/div[2]/div[3]/section[2]/div/div[2]/div[3]/table/tbody/tr[{x}]/td[6]')
        paint_per = self.driver.find_element(By.XPATH, f'/html/body/div[1]/div[2]/div[2]/div[3]/section[2]/div/div[2]/div[3]/table/tbody/tr[{x}]/td[7]')
        mid_m = self.driver.find_element(By.XPATH, f'/html/body/div[1]/div[2]/div[2]/div[3]/section[2]/div/div[2]/div[3]/table/tbody/tr[{x}]/td[8]')
        mid_a = self.driver.find_element(By.XPATH, f'/html/body/div[1]/div[2]/div[2]/div[3]/section[2]/div/div[2]/div[3]/table/tbody/tr[{x}]/td[9]')
        mid_per = self.driver.find_element(By.XPATH, f'/html/body/div[1]/div[2]/div[2]/div[3]/section[2]/div/div[2]/div[3]/table/tbody/tr[{x}]/td[10]')
        lc3_m = self.driver.find_element(By.XPATH, f'/html/body/div[1]/div[2]/div[2]/div[3]/section[2]/div/div[2]/div[3]/table/tbody/tr[{x}]/td[11]')
        lc3_a = self.driver.find_element(By.XPATH, f'/html/body/div[1]/div[2]/div[2]/div[3]/section[2]/div/div[2]/div[3]/table/tbody/tr[{x}]/td[12]')
        lc3_per = self.driver.find_element(By.XPATH, f'/html/body/div[1]/div[2]/div[2]/div[3]/section[2]/div/div[2]/div[3]/table/tbody/tr[{x}]/td[13]')
        rc3_m = self.driver.find_element(By.XPATH, f'/html/body/div[1]/div[2]/div[2]/div[3]/section[2]/div/div[2]/div[3]/table/tbody/tr[{x}]/td[14]')
        rc3_a = self.driver.find_element(By.XPATH, f'/html/body/div[1]/div[2]/div[2]/div[3]/section[2]/div/div[2]/div[3]/table/tbody/tr[{x}]/td[15]')
        rc3_per = self.driver.find_element(By.XPATH, f'/html/body/div[1]/div[2]/div[2]/div[3]/section[2]/div/div[2]/div[3]/table/tbody/tr[{x}]/td[16]')
        c3_m = self.driver.find_element(By.XPATH, f'/html/body/div[1]/div[2]/div[2]/div[3]/section[2]/div/div[2]/div[3]/table/tbody/tr[{x}]/td[17]')
        c3_a = self.driver.find_element(By.XPATH, f'/html/body/div[1]/div[2]/div[2]/div[3]/section[2]/div/div[2]/div[3]/table/tbody/tr[{x}]/td[18]')
        c3_per = self.driver.find_element(By.XPATH, f'/html/body/div[1]/div[2]/div[2]/div[3]/section[2]/div/div[2]/div[3]/table/tbody/tr[{x}]/td[19]')
        ab3_m = self.driver.find_element(By.XPATH, f'/html/body/div[1]/div[2]/div[2]/div[3]/section[2]/div/div[2]/div[3]/table/tbody/tr[{x}]/td[20]')
        ab3_a = self.driver.find_element(By.XPATH, f'/html/body/div[1]/div[2]/div[2]/div[3]/section[2]/div/div[2]/div[3]/table/tbody/tr[{x}]/td[21]')
        ab3_per = self.driver.find_element(By.XPATH, f'/html/body/div[1]/div[2]/div[2]/div[3]/section[2]/div/div[2]/div[3]/table/tbody/tr[{x}]/td[22]')
        stats = {
            'RA' :{'RA_M':ra_m, 'RA_A':ra_a, 'RA_%':ra_per},
            'PAINT':{'PAINT_M':paint_m, 'PAINT_A':paint_a, 'PAINT_%':paint_per},
            'MID_M':mid_m, 'MID_A':mid_a, 'MID_%':mid_per,
            'LC3_M':lc3_m, 'LC3_A':lc3_a, 'LC3_%':lc3_per,
            'RC3_M':rc3_m, 'RC3_A':rc3_a, 'RA_%':rc3_per,
            'C3_M':c3_m, 'C3_A':c3_a, 'C3_%':c3_per,
            'AB3_M':ab3_m, 'AB3_A':ab3_a, 'AB3_%':ab3_per                
        }
        print(ra_m)
        #print(stats)
        return stats
    

driver = uc.Chrome()
driver.get("https://www.nba.com/stats/teams/opponent-shooting")
time.sleep(5)
team = []
team.append(scrape_league)
with open('opp.json', 'w') as fp:
    json.dump(team, fp)
#shooting-opponent > tbody:nth-child(4) > tr:nth-child(1) > td:nth-child(3)
#shooting-opponent > tbody:nth-child(4) > tr:nth-child(1) > td:nth-child(3)
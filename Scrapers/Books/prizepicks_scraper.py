from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoAlertPresentException
from selenium.webdriver.support import expected_conditions as EC, wait
from concurrent.futures import ThreadPoolExecutor

import undetected_chromedriver as uc
import time
import pandas as pd

start_time = time.time()
  
driver = uc.Chrome()


driver.get("https://app.prizepicks.com/")
time.sleep(3)


WebDriverWait(driver, 15).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "close")))
time.sleep(3)
driver.find_element(By.XPATH, "/html/body/div[3]/div[3]/div/div/div[1]").click()
time.sleep(2)
ppPlayers = []

league_container = WebDriverWait(driver, 1).until(EC.visibility_of_element_located((By.CLASS_NAME, "pp-container")))
leagues = driver.find_element(By.CSS_SELECTOR, "#scrollable-area").text.split('\n')

def scrape_league(league_number):
    driver.find_element(By.XPATH, "/html/body/div[1]/div/div[3]/div[1]/div/main/div/nav/div/div[" + str(league_number) + "]").click()
    time.sleep(2)

    #element_xpath = driver.find_element(By.XPATH,
     #                                   f"/html/body/div[1]/div/div[3]/div[1]/div/main/div/nav/div[2]/div[1]/div")
    stat_container = WebDriverWait(driver, 1).until(EC.visibility_of_element_located((By.CLASS_NAME, "stat-container")))

    # Finding all the stat elements within the stat-container
    categories = driver.find_element(By.CSS_SELECTOR, ".stat-container").text.split('\n')
    # Collecting categories
    for category in categories:
        driver.find_element(By.XPATH, f"//div[text()='{category}']").click()

        projectionsPP = WebDriverWait(driver, 5).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".projection")))

        for projections in projectionsPP:
            names = projections.find_element(By.CLASS_NAME, "name").text
            value = projections.find_element(By.CLASS_NAME, "presale-score").get_attribute('innerHTML')
            propType = projections.find_element(By.CLASS_NAME, "text").get_attribute('innerHTML')

            # Looped between 2 to print the over and the under of each line
            for z in range(2):
                if z == 0:
                    playersO = {
                        'Platform': 'PrizePicks',
                        'League': leagues[league_number],
                        'Name': names, 
                        'Line': "Over",
                        'PP Value': value,
                        'Prop': propType.replace("<wbr>", "")

                    }
                else:
                    playersU = {
                        'Platform': 'PrizePicks',
                        'League': leagues[league_number],
                        'Name': names,
                        'Line': "Under",
                        'PP Value': value,
                        'Prop': propType.replace("<wbr>", "")
                    }
            ppPlayers.append(playersO)
            ppPlayers.append(playersU)

scrape_league(2)

dfProps = pd.DataFrame(ppPlayers)
    # CHANGE THE NAME OF THE FILE TO YOUR LIKING
dfProps.to_csv('prizepicks_test.csv')

print("These are all of the props offered by PP.", '\n')
print(dfProps)
print('\n')
print(time.time() - start_time)



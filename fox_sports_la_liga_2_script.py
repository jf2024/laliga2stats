import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By

standings_website = 'https://www.foxsports.com/soccer/laliga-2/standings'

driver = webdriver.Chrome()
driver.maximize_window()
driver.get(standings_website)

# standings data (this is grabbing headers)
headers_tag = driver.find_element(By.XPATH, "//thead[@class='data-header fs-11 ls-pt25']")
list_headers = headers_tag.find_elements(By.TAG_NAME, "th")

headers = []
for head in list_headers:
    text = head.text
    headers.append(text)

headers.insert(0, 'POSITION')

## getting the actual data here (after getting the headers)
team_rows = driver.find_elements(By.XPATH, '//tr[starts-with(@id, "tbl-row-")]')

all_team_data = []

for row in team_rows:
    row_cells = row.text.split('\n')
    row_cells = [cell.strip() for cell in row_cells if cell.strip()]
    
    all_team_data.append(row_cells)

standings_df = pd.DataFrame(all_team_data, columns=headers)
standings_df.to_csv("laliga2_standings_2025.csv", index=False)

seasons = [2024, 2025]
base_url = "https://www.foxsports.com"

all_stat_tables = {}

for season in seasons:
    stat_urls = {
        "standard": f"{base_url}/soccer/laliga-2/team-stats?category=standard&season={season}&groupId=129",
        "offensive": f"{base_url}/soccer/laliga-2/team-stats?category=offensive&season={season}&groupId=129",
        "goalkeeping": f"{base_url}/soccer/laliga-2/team-stats?category=goalkeeping&season={season}&groupId=129"
    }

    for cat_name, url in stat_urls.items():
        driver.get(url)
        time.sleep(1.5)
        
        # headers
        headers_tag = driver.find_element(By.XPATH, "//thead[@class='data-header fs-11 ls-pt25 sticky-row-wrapper']")
        list_headers = [head.text.strip() for head in headers_tag.find_elements(By.TAG_NAME, "th") if head.text.strip()]
        
        # team rows
        team_rows = driver.find_elements(By.XPATH, '//tr[starts-with(@id, "tbl-row-")]')
        
        # extract text
        cat_data = []
        for row in team_rows:
            row_cells = [cell.strip() for cell in row.text.split('\n') if cell.strip()]
            if row_cells:
                row_cells = row_cells[1:] 
                cat_data.append(row_cells)
                    
        # create dataframe
        df_cat = pd.DataFrame(cat_data, columns=list_headers)

        all_stat_tables[f"{cat_name}_{season}"] = df_cat


for table_key, df_table in all_stat_tables.items():
    filename = f"laliga2_team_stats_{table_key}.csv"
    
    df_table.to_csv(filename, index=False)

driver.quit()
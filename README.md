# La Liga 2 Analytics Dashboard

## Project Overview
This project is an end-to-end data engineering and analytics pipeline focused on the Spanish Second Division (La Liga 2) for the 2024 and 2025 seasons. It transforms raw, unstructured web data into a fully normalized relational database, culminating in an interactive Streamlit dashboard designed to explore league-wide trends and individual team performance.

[Insert Screenshot of Main Dashboard Here]

## Features
The dashboard is built with a "Macro-to-Micro" analytical approach, featuring four distinct modules:
* **League Trends (Macro View):** Interactive scatter plots exploring the correlation between playstyle (possession, shots) and success (points, goal differential).
* **Team Explorer (Micro View):** Deep dives into specific clubs, highlighting Home vs. Away performance disparities and offensive production profiles.
* **Team Comparison:** A head-to-head evaluation tool comparing multiple clubs across core metrics simultaneously.
* **Raw Data Explorer:** A unified, filterable view of the fully joined dataset.

[Insert Screenshot of Team Comparison Tab Here]

## Technical Architecture
This project implements a standard Extract, Transform, Load (ETL) pipeline:

1.  **Extraction (Web Scraping):** Built with `Selenium` to dynamically scrape structural table data from Fox Sports, cleanly extracting standings, offensive, standard, and goalkeeping metrics.
2.  **Transformation (Data Cleaning):** Utilized `Pandas` to parse complex strings (e.g., splitting "13-7-1" records into dedicated integer columns) and strip redundant metrics at the root level to prevent future merge conflicts.
3.  **Load (Database Normalization):** Engineered a fully normalized SQLite database (`laliga2.db`). The architecture utilizes a master `teams` table to generate primary keys (`team_id`), establishing reliable composite keys (Team ID + Season) for flawless relational joining.
4.  **Presentation (Visualization):** Deployed a highly interactive `Streamlit` web application leveraging `Plotly Express` for dynamic, hover-enabled data visualizations.

## Tech Stack
* **Python 3.11+**
* **Data Collection:** Selenium, Webdriver Manager
* **Data Manipulation:** Pandas
* **Database:** SQLite3
* **Data Visualization:** Streamlit, Plotly Express

## Installation and Setup

You can access the deployed app here: [La Liga 2 Analytics Dashboard](https://laliga2stats-aebpdtnw6tgyuh8rwkczy8.streamlit.app/).  
The same link is also included in `service_urls.txt`.

To run the app locally, follow the steps below.

### Prerequisites

Make sure you have Python installed, then install the required dependencies:

```bash
pip install pandas selenium webdriver-manager streamlit plotly
```

Also make sure `laliga_2_standings_2024.csv` is in your project directory. I created this file manually because I could not access it directly from the website.

### Steps

1. Run `fox_sports_la_liga_2_script.py` to generate the raw CSV files.
2. Run `cleaning_script.py` to clean the CSV files.
3. Run `create_laliga2_db.py` to create the SQLite database.
4. Run the app with:

```bash
streamlit run app.py
```
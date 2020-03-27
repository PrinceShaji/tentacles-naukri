## Deprecated version. No longer works with the new website.

# Tentacles - Naukri
  A scraper for naukri that is capable of multiprocessing the task. The scraper also has a progress bar. So no more guessing the scrape status.

## Requirements
- ~~Create a file ``` tentacles_naukri.py ``` and add the browser heasers and query parameters.~~
- Create a venv using pipenv by ``` pipenv install ```.
- Required libraries.
  - requests
  - BeautifulSoup
  - pandas
  - tqdm

## Usage
- Activate venv by ``` pipenv shell ```.
- Run ``` python tentacle_naukri.py <City Name>```.
- If you didn't enter a city name, you will be prompted to enter one.
- The scraped data will be saved as a csv file in the format ``` city_name_date.csv ```

## Available Cities
- For list available cities, refer ``` complete_city_list.csv ```

### Ignored files
- ~~settings.py is ignored. So create a file settings.py in the roor folder and add the browser headers.~~
- test.py & /test is meant to test out code snippets.


# Tentacles - Naukri
  A scraper for naukri that is capable of multiprocessing the task.


## Requirements
- Create a file ``` tentacles_naukri.py ``` and add the browser heasers and query parameters.
- Create a venv using pipenv.
- Install venv requirements
  - requests
  - Beautiful Soup
  - pandas
  - tqdm
  - termcolor

## Usage
- Rum ``` tentacle_naukri.py ```
- Enter the city name
- The file will be saved as city_name_date.csv
  
### Ignored files
- ~~settings.py is ignored. So create a file settings.py in the roor folder and add the browser headers.~~
- test.py & /test is meant to test out code snippets.


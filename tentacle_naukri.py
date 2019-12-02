#!/usr/bin/env python3

from sys import argv
import requests
from bs4 import BeautifulSoup
import multiprocessing
import tentacles_settings
import re
from time import strftime, gmtime, time, sleep
import pandas as pd
from datetime import date
import tqdm

class multi_scraper:
    """ Scraper class. """

    def __init__(self):
        """ """
        self.city = 'Bangalore' # Default.
        self.headers = self.make_header(self.city)
        self.query = tentacles_settings.query_parameters.format(self.city)
        self.total_jobs = None
        self.total_pages = self.get_total_pages(self.city)

    def make_header(self, city_name):
        """ Create headers with the correct city name. """
        """ Find a better way to do it in fewer lines. """
        tentacles_settings.headers['Referer'] = tentacles_settings.headers['Referer'].format(self.city.lower())
        return tentacles_settings.headers

    def generate_url(self, page_number):
        """ Generates the url. """
        if page_number == 1:
            return f"https://www.naukri.com/jobs-in-{self.city.lower()}"
        return f"https://www.naukri.com/jobs-in-{self.city.lower()}-{page_number}"

    def get_soup(self, url):
        """ Returns soup object. """
        response = requests.post(url, headers=self.headers, data=self.query)
        soup = BeautifulSoup(response.content, 'lxml')  # Use html.parser if lxml is not installed.
        return soup

    def get_total_pages(self, city):
        """ Parses the max number of pages for a city.\n """
        print(f'\nFinding the total number of pages to scrape for {self.city}.\n')
        soup = self.get_soup(self.generate_url(1))
        total_jobs = soup.find_all('span', {'class': 'cnt'})
        self.total_jobs = int(re.findall(r'\d+$', total_jobs[0].text)[0])
        total_pages = ((self.total_jobs - 1) // 50) + 1        
        return total_pages

    def multi_scrape(self, page_number):
        """ The main scraper. """
        # print(f'scraping page {page_number}')   # Comment this line when using progress bar.
        soup = self.get_soup(self.generate_url(page_number))
        data_divs = soup.find_all("div", {"type" : "tuple" })
        data_list = []
        for data_div in data_divs:
            data_dict = {}
            data_dict['Page No.'] = page_number
            try : 
                data_dict['url']=data_div['data-url']
                data_dict['organization']=data_div.find(attrs={"class": "org"}).text
                data_dict['title']=data_div.find(attrs={"class": "desig"}).text
                try:
                    data_dict['experience']=data_div.find(attrs={"class": "exp"}).text
                except:
                    data_dict['experience']=None
                try:          
                    data_dict['skill']=data_div.find(attrs={"class": "skill"}).text
                except:
                    data_dict['skill']=None
                try:
                    data_dict['description']=data_div.find_all(attrs={"class": "more desc"})[1].text
                except:
                    data_dict['description']=None            
                data_dict['salary']=data_div.find(attrs={"class": "salary"}).text
                data_dict['postedby']=data_div.find(attrs={"class": "rec_name"}).text
                data_dict['time']=data_div.find(attrs={"class": "date"}).text
                data_dict['runtime']=strftime("%Y-%m-%d %H:%M:%S", gmtime())
            except:
                data_dict['url']=None
                data_dict['organization']=None
                data_dict['title']=None
                data_dict['experience']=None
                data_dict['skill']=None
                data_dict['description']=None
                data_dict['salary']=None
                data_dict['postedby']=None
                data_dict['time']=None
                data_dict['runtime']=strftime("%Y-%m-%d %H:%M:%S", gmtime())            
            data_list.append(data_dict)
        return data_list

    
if __name__ == "__main__":
    # Creating the scraper object.
    tentacles = multi_scraper()

    # Parsing argv
    if len(argv) > 1:
        tentacles.city = argv[1].title()
    else:
        tentacles.city = input("Enter city name: ").title()

    total_pages = tuple(i for i in range(1, tentacles.total_pages + 1))
    print(f'Total jobs: {tentacles.total_jobs} \nTotal pages to scrape: {tentacles.total_pages}\n')
    
    # # Multiprocessing scraping
    # start = time()
    # pool = multiprocessing.Pool()
    # data = pool.map(tentacles.multi_scrape, total_pages)
    # end = time()
    # print(f'Time taken to scrape {tentacles.total_jobs} jobs from {tentacles.total_pages} pages is: {end-start:2f} seconds.')
    

    # Multiprocessing with progress bar
    start = time()
    with multiprocessing.Pool() as pool:
      data = list(tqdm.tqdm(pool.imap(tentacles.multi_scrape, total_pages), total=len(total_pages)))
    end = time()
    print(f'\nTime taken to scrape {tentacles.total_jobs} jobs from {tentacles.total_pages} pages is: {end-start:2f} seconds.')


    # Formatting the data for creating the dataframe.
    proper_list = []
    for _ in data:
        for jobs in _:
            proper_list.append(jobs)

    # Cleaning for the last 7 days
    df = pd.DataFrame(proper_list)
    pd.set_option('display.max_colwidth', 0)
    time_list = [ 'Just Now', 'Few Hours Ago', 'Today', '1 day ago',
                  '2 days ago', '3 days ago', '4 days ago', '5 days ago', 
                  '6 days ago', '7 days ago']
    df1 = df[df['time'].isin(time_list)]
    df2 = df1.drop(['Page No.', 'runtime','url'], axis=1)
    df3 = df2.drop_duplicates()
    df3.to_csv(f"{tentacles.city}_{date.today()}.csv")

    print('Completed writing to file!\n')

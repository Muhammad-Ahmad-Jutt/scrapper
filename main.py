import requests
import re
from bs4 import BeautifulSoup

def match_url(data):
    # Combined regex patterns
    pattern1 = r'/en/stamps/(years|list)/country/\d+-[A-Za-z_]+'
    pattern2 = r'/en/stamps/list/country/\d+-[A-Za-z_]+/year/(\d{4})'
    
    if re.match(pattern1, data):
        if 'year' in data:
            match = re.match(pattern2, data)
            if match:
                return 1, match.group(1) 
        return 0, None  
    return -1, None  

def extracting_data(data):
    elements = data.find('div', {'id':"plist_items"})
    if elements:
        for element in elements:
            print(element)

def matching_data(data, country=''):
    years = []
    sublink = ''
    link_for_year = ''
    if data:
        for link in data.find_all('a'):
            sublink = link.get('href')
            if sublink:
                match_result, year = match_url(sublink)
                if match_result == 0 and sublink.endswith(country):
                    print('no year')
                    return sublink, None
                elif match_result == 1:
                    print('years')
                    link_for_year = sublink
                    years.append(year)
    return link_for_year, years

def fetch_link(data, country=''):
    sublink, years = matching_data(data, country)
    print(sublink, years)
    if years is not None:
        print('we have some year')
        link = make_sub_link_for_year(sublink)
        data = send_request(link, years[0])
        return data
    else:
        print('going to the sublink')
        data = send_request(sublink)
        return data
         

def send_request(link, year=''):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0'
    }

    try:
        
        link = 'https://colnect.com'+link+year
        print(link, 'we have')
        response = requests.get(link, headers=headers, timeout=10)
        response.raise_for_status() 
        soup = BeautifulSoup(response.text, 'html.parser')
        return soup
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None
def make_sub_link_for_year(sublink):
    link_len = len(sublink)
    return sublink[:link_len-4]
# Test URLs
url = '/en/stamps/countries'
#url = '/en/stamps/years/country/1-Afghanistan'
country = 'Abu_Dhabi'
data = send_request(url)
link = fetch_link(data, country)
data = fetch_link(link)
print(data)        
        
        
        
        
#        sublink, years = matching_data(data)
    #    extracting_data(data)


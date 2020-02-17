import requests
from bs4 import BeautifulSoup as bs
import csv
from fake_useragent import UserAgent


# Взятие html-страницы из url
def get_html(url):
    user_agent = UserAgent()
    user = user_agent.random
    headers = {'User-Agent': str(user)}
    r = requests.get(url, headers=headers)
    return r.text


def get_all_links(html):
    soup = bs(html, "lxml")
    divs = soup.find_all('div', class_ = 'films_left')
    links = []
    for div in divs:
        a = div.find('a', 'films_iconFrame').get('href')
        a = 'https://www.kinoafisha.info' + a
        links.append(a)
    
    return links


def get_page_data(html):
    soup = bs(html, "lxml")
    try:
        name = soup.find('span', class_="breadcrumbs_link").find('span').text.strip()
    except:
        name = ''

    try:
        director = soup.find('div', class_="movieInfoV2_producerColumns").find('span', class_='badgeList_name').text.strip()
    except:
        director = ''

    try:
        description = soup.find('span', class_='movieInfoV2_descText').text.strip()
    except:
        description = ''

    data = {'name': name,
            'director': director,
            'description': description}
    return data


def write(data):
    FILENAME = "kinoafisha_top-1000.csv"
    with open(FILENAME, "a") as file:
        
        writer = csv.writer(file, delimiter = ';')
        
        writer.writerow(( data['name'],
                          data['director'],
                          data['description'] ))
        print(data['name'], 'parsed')


def main():
    
    url = 'https://www.kinoafisha.info/rating/movies/?page=0'
    
    for i in range(11):
        url = 'https://www.kinoafisha.info/rating/movies/?page='
        url = url + str(i)
        all_links = get_all_links(get_html(url))
        for url in all_links:
            html = get_html(url)
            data = get_page_data(html)
            write(data)



if __name__ == '__main__':
    main()



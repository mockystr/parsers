from bs4 import BeautifulSoup
import requests
import json
import re

"""
1. tale amount of pages on query
2. format all urls on site
3. data scraping
"""


def write_json(data):
    with open("data.json", 'ab') as f:
        f.seek(0, 2)  # Go to the end of file
        if f.tell() == 0:  # Check if file is empty
            f.write(json.dumps([data], indent=2, ensure_ascii=False).encode())  # If empty, write an array
        else:
            f.seek(-1, 2)
            f.truncate()  # Remove the last character, open the array
            f.write(' , '.encode())  # Write the separator
            f.write(json.dumps(data, ensure_ascii=False, indent=2).encode())  # Dump the dictionary
            f.write(']'.encode())


def get_html(url):
    return requests.get(url).text


def get_total_pages(html):
    soup = BeautifulSoup(html, 'lxml')
    pages = soup.find('div', class_='pagination-pages').find_all('a', class_="pagination-page")[-1].get('href')
    return int(pages.split('=')[1].split('&')[0])


def get_page_data(html):
    soup = BeautifulSoup(html, 'lxml')
    ads = soup.find('div', class_='catalog-list').find_all('div', class_='item_table')

    for ad in ads:
        try:
            title = ''
            url = ''
            price = ''
            category, company, metro = '', '', ''
            title = ad.find('div', class_='description').find('h3').text.strip()
            url = 'https://www.avito.ru' + ad.find('div', class_='description').find('h3').find('a').get('href')
            price = ad.find('div', class_='description').find('div', class_='about').text.strip().split("₽")[0].strip()
            p_list = ad.find('div', class_='data').find_all('p')

            if len(p_list) == 2:
                category = p_list[0].text.split("|")[0].strip()
                company = p_list[0].text.split("|")[1].strip()
                metro = re.sub(r'\xa0', ' ', p_list[1].text.strip())
            if len(p_list) == 1:
                category = p_list[0].text.split("|")[0].strip()
                company = p_list[0].text.split("|")[1].strip()
        except:
            pass
        data = {'title': title, 'url': url, 'price': price,
                'category': category, 'company': company, 'metro': metro}

        write_json(data)


def main():
    url = 'https://www.avito.ru/moskva?p=1&q=apple'
    total_pages = get_total_pages(get_html(url))

    # for i in range(1, total_pages + 1):
    # if you will write like this
    # i will be banned on site
    # so i parse only first five pages
    for i in range(1, 5):
        url_get = 'https://www.avito.ru/moskva?p={}&q=apple'.format(str(i))
        get_page_data(get_html(url_get))


if __name__ == '__main__':
    main()

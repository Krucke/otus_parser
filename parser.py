import requests
import sys

from bs4 import BeautifulSoup as bs4


SITE = 'https://www.python.org/'


def get_domain(site: str) -> str:
    return '.'.join(site.split('/')[2].split('?')[0].split('.')[-2:])


def get_domain_from_href(href: str) -> str:
    if href.startswith('http'):
        return href
    return ''


def find_relations(site: str, data: list) -> None:
    r = requests.get(site)
    main_domain = get_domain(site)
    soup = bs4(r.content, 'html.parser')
    links = soup.find_all('a')
    for link in links:
        link_domain = get_domain_from_href(link.attrs.get('href'))
        if link_domain and not main_domain == get_domain(link_domain):
            data.append(f'{link_domain} from {site}')


def main():
    
    result = []
    try:
        main_site = sys.argv[1]
    except IndexError:
        main_site = SITE
    
    try:
        type_log = sys.argv[2]
    except IndexError:
        type_log = 'console'
    
    find_relations(main_site, result)
    result = set(result)

    if type_log == 'console':
        for site in result:
            print(site)
        return True
    
    with open('results.txt', 'w') as file:
        for site in result:
            file.write(site+'\n')
    
    return True


if __name__ == '__main__':
    main()
import requests
import json
from bs4 import BeautifulSoup
from fake_headers import Headers

HOST = 'https://spb.hh.ru'
PARAMS = '/search/vacancy?text=python&area=1&area=2'
LINK = f"{HOST}{PARAMS}"

def get_headers():
    return Headers(browser='chrome', os='win').generate()

def get_info(vacancy):
    city = vacancy.find('div', attrs={'data-qa': 'vacancy-serp__vacancy-address'}).text.split(',')[0]
    company = vacancy.find('a', attrs={'data-qa': 'vacancy-serp__vacancy-employer'}).text
    salary_info = vacancy.find('span', attrs={'data-qa': 'vacancy-serp__vacancy-compensation'})
    salary = salary_info.text if salary_info is not None else 'Не указана'
    link = vacancy.find('a', attrs={'data-qa': 'serp-item__title'})['href']
    
    return {
        'city': city,
        'company': company,
        'salary': salary,
        'link': link
    }

def is_match(link):
    vacancy_page = requests.get(link, headers=get_headers())
    description = BeautifulSoup(vacancy_page.text, 'html.parser')\
        .find('div', class_='vacancy-description').text.lower()
    return 'django' in description or 'flask' in description






if __name__ == '__main__':
    page = requests.get( LINK, headers=get_headers())
    soup = BeautifulSoup(page.text, 'html.parser')
    vacancies = soup.find_all('div', class_='vacancy-serp-item-body__main-info')
    vacancies_info = [get_info(vacancy) for vacancy in vacancies]
    filter_vacancies = [vacancy for vacancy in vacancies_info if is_match(vacancy['link'])]

    with open('vacancies.json', 'w') as f:
        json.dump(filter_vacancies, f, indent=2, ensure_ascii=False)




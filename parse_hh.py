import requests
from bs4 import BeautifulSoup

def get_html(url: str):
    try:
        response = requests.get(
            url,
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
            }
        )
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"Request error for URL {url}: {e}")
        return None

def parse_data(soup, selectors):
    data = {}
    for key, (selector, default) in selectors.items():
        element = soup.select_one(selector)
        data[key] = element.get_text(strip=True) if element else default
    return data

def extract_vacancy_data(html):
    soup = BeautifulSoup(html, "html.parser")
    selectors = {
        "title": ("h1[data-qa='vacancy-title']", "Заголовок не найден"),
        "salary": ("span[data-qa='vacancy-salary-compensation-type-net']", "Зарплата не указана"),
        "experience": ("span[data-qa='vacancy-experience']", "Опыт не указан"),
        "employment_mode": ("p[data-qa='vacancy-view-employment-mode']", "Тип занятости не указан"),
        "company": ("a[data-qa='vacancy-company-name']", "Компания не указана"),
        "location": ("p[data-qa='vacancy-view-location']", "Местоположение не указано"),
        "description": ("div[data-qa='vacancy-description']", "Описание не указано"),
    }
    data = parse_data(soup, selectors)
    skills = [skill.get_text(strip=True) for skill in soup.find_all("div", {"class": "magritte-tag__label___YHV-o_3-0-3"})]
    
    markdown = f"""
# {data['title']}

**Компания:** {data['company']}
**Зарплата:** {data['salary']}
**Опыт работы:** {data['experience']}
**Тип занятости и режим работы:** {data['employment_mode']}
**Местоположение:** {data['location']}

## Описание вакансии
{data['description']}

## Ключевые навыки
- {' - '.join(skills) if skills else "Навыки не указаны"}
"""
    return markdown.strip()

def get_job_description(url: str):
    html = get_html(url)
    if html:
        return extract_vacancy_data(html)
    else:
        print("Failed to retrieve job description.")
        return None




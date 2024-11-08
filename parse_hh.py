import requests
from bs4 import BeautifulSoup

def get_html(url: str):
    response = requests.get(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
        },
    )
    if response.status_code != 200:
        print(f"Ошибка запроса: {response.status_code} при URL: {url}")
    return response

def extract_vacancy_data(html):
    soup = BeautifulSoup(html, "html.parser")

    # Извлечение данных вакансии
    title = soup.find("h1", {"data-qa": "vacancy-title"}).get_text(strip=True) if soup.find("h1", {"data-qa": "vacancy-title"}) else "Заголовок не найден"
    salary = soup.find("span", {"data-qa": "vacancy-salary-compensation-type-net"}).get_text(strip=True) if soup.find("span", {"data-qa": "vacancy-salary-compensation-type-net"}) else "Зарплата не указана"
    experience = soup.find("span", {"data-qa": "vacancy-experience"}).get_text(strip=True) if soup.find("span", {"data-qa": "vacancy-experience"}) else "Опыт не указан"
    employment_mode = soup.find("p", {"data-qa": "vacancy-view-employment-mode"}).get_text(strip=True) if soup.find("p", {"data-qa": "vacancy-view-employment-mode"}) else "Тип занятости не указан"
    company = soup.find("a", {"data-qa": "vacancy-company-name"}).get_text(strip=True) if soup.find("a", {"data-qa": "vacancy-company-name"}) else "Компания не указана"
    location = soup.find("p", {"data-qa": "vacancy-view-location"}).get_text(strip=True) if soup.find("p", {"data-qa": "vacancy-view-location"}) else "Местоположение не указано"
    description = soup.find("div", {"data-qa": "vacancy-description"}).get_text(strip=True) if soup.find("div", {"data-qa": "vacancy-description"}) else "Описание не указано"
    skills = [skill.get_text(strip=True) for skill in soup.find_all("div", {"class": "magritte-tag__label___YHV-o_3-0-3"})]

    markdown = f"""
# {title}

**Компания:** {company}
**Зарплата:** {salary}
**Опыт работы:** {experience}
**Тип занятости и режим работы:** {employment_mode}
**Местоположение:** {location}

## Описание вакансии
{description}

## Ключевые навыки
- {' - '.join(skills) if skills else "Навыки не указаны"}
"""
    return markdown.strip()

def extract_candidate_data(html):
    soup = BeautifulSoup(html, 'html.parser')
    try:
        # Извлечение основных данных кандидата
        name = soup.find('h2', {'data-qa': 'bloko-header-1'}).get_text(strip=True)
        gender_age = soup.find('p').get_text(strip=True)
        location = soup.find('span', {'data-qa': 'resume-personal-address'}).get_text(strip=True)
        job_title = soup.find('span', {'data-qa': 'resume-block-title-position'}).get_text(strip=True)
        job_status = soup.find('span', {'data-qa': 'job-search-status'}).get_text(strip=True)

        # Извлечение опыта работы
        experience_section = soup.find('div', {'data-qa': 'resume-block-experience'})
        experiences = []
        if experience_section:
            experience_items = experience_section.find_all('div', class_='resume-block-item-gap')
            for item in experience_items:
                period = item.find('div', class_='bloko-column_s-2').get_text(strip=True)
                duration = item.find('div', class_='bloko-text').get_text(strip=True)
                period = period.replace(duration, f" ({duration})")
                company = item.find('div', class_='bloko-text_strong').get_text(strip=True)
                position = item.find('div', {'data-qa': 'resume-block-experience-position'}).get_text(strip=True)
                description = item.find('div', {'data-qa': 'resume-block-experience-description'}).get_text(strip=True)
                experiences.append(f"**{period}**\n\n*{company}*\n\n**{position}**\n\n{description}\n")
        
        # Извлечение ключевых навыков
        skills_section = soup.find('div', {'data-qa': 'skills-table'})
        skills = [skill.get_text(strip=True) for skill in skills_section.find_all('span', {'data-qa': 'bloko-tag__text'})] if skills_section else []

        markdown = f"# {name}\n\n"
        markdown += f"**{gender_age}**\n\n"
        markdown += f"**Местоположение:** {location}\n\n"
        markdown += f"**Должность:** {job_title}\n\n"
        markdown += f"**Статус:** {job_status}\n\n"
        markdown += "## Опыт работы\n\n" + "\n".join(experiences) if experiences else "Опыт работы не указан.\n\n"
        markdown += "## Ключевые навыки\n\n" + ', '.join(skills) if skills else "Ключевые навыки не указаны\n"

        return markdown
    except Exception as e:
        print(f"Ошибка при извлечении данных кандидата: {e}")
        return None


    # Извлечение типа занятости и режима работы
    employment_mode = soup.find(
        "p", {"data-qa": "vacancy-view-employment-mode"}
    )
    if not employment_mode:
        print("Предупреждение: тип занятости не найден.")
        employment_mode = "Тип занятости не указан"

    # Извлечение компании
    company = soup.find("a", {"data-qa": "vacancy-company-name"})
    if not company:
        print("Предупреждение: компания не найдена.")
        company = "Компания не указана"

    # Извлечение местоположения
    location = soup.find("p", {"data-qa": "vacancy-view-location"})
    if not location:
        print("Предупреждение: местоположение не найдено.")
        location = "Местоположение не указано"

    # Извлечение описания вакансии
    description = soup.find("div", {"data-qa": "vacancy-description"})
    if not description:
        print("Предупреждение: описание вакансии не найдено.")
        description = "Описание не указано"

    # Извлечение ключевых навыков
    skills = [
        skill.text.strip()
        for skill in soup.find_all(
            "div", {"class": "magritte-tag__label___YHV-o_3-0-3"}
        )
    ]

    # Формирование строки в формате Markdown
    markdown = f"""
# {title}

**Компания:** {company}
**Зарплата:** {salary}
**Опыт работы:** {experience}
**Тип занятости и режим работы:** {employment_mode}
**Местоположение:** {location}

## Описание вакансии
{description}

## Ключевые навыки
- {' - '.join(skills)}

"""
    return markdown.strip()



def extract_candidate_data(html):
    soup = BeautifulSoup(html, 'html.parser')

    try:
        # Извлечение основных данных кандидата
        name_tag = soup.find('h2', {'data-qa': 'bloko-header-1'})
        if not name_tag:
            raise ValueError("Не найдено имя кандидата.")
        name = name_tag.text.strip()

        gender_age = soup.find('p').text.strip()
        location = soup.find('span', {'data-qa': 'resume-personal-address'}).text.strip()
        job_title = soup.find('span', {'data-qa': 'resume-block-title-position'}).text.strip()
        job_status = soup.find('span', {'data-qa': 'job-search-status'}).text.strip()

        # Извлечение опыта работы
        experience_section = soup.find('div', {'data-qa': 'resume-block-experience'})
        experience_items = experience_section.find_all('div', class_='resume-block-item-gap')
        experiences = []
        for item in experience_items:
            period = item.find('div', class_='bloko-column_s-2').text.strip()
            duration = item.find('div', class_='bloko-text').text.strip()
            period = period.replace(duration, f" ({duration})")

            company = item.find('div', class_='bloko-text_strong').text.strip()
            position = item.find('div', {'data-qa': 'resume-block-experience-position'}).text.strip()
            description = item.find('div', {'data-qa': 'resume-block-experience-description'}).text.strip()
            experiences.append(f"**{period}**\n\n*{company}*\n\n**{position}**\n\n{description}\n")

        # Извлечение ключевых навыков
        skills_section = soup.find('div', {'data-qa': 'skills-table'})
        skills = [skill.text.strip() for skill in skills_section.find_all('span', {'data-qa': 'bloko-tag__text'})]

        # Формирование строки в формате Markdown
        markdown = f"# {name}\n\n"
        markdown += f"**{gender_age}**\n\n"
        markdown += f"**Местоположение:** {location}\n\n"
        markdown += f"**Должность:** {job_title}\n\n"
        markdown += f"**Статус:** {job_status}\n\n"
        markdown += "## Опыт работы\n\n"
        for exp in experiences:
            markdown += exp + "\n"
        markdown += "## Ключевые навыки\n\n"
        markdown += ', '.join(skills) + "\n"

        return markdown
    except Exception as e:
        print(f"Ошибка при извлечении данных кандидата: {e}")
        return None


def get_candidate_info(url: str):
    response = get_html(url)
    if response.status_code != 200:
        print(f"Ошибка при получении данных кандидата. Статус: {response.status_code}")
        return None
    return extract_candidate_data(response.text)


def get_job_description(url: str):
    response = get_html(url)
    if response.status_code != 200:
        print(f"Ошибка при получении данных о вакансии. Статус: {response.status_code}")
        return None
    return extract_vacancy_data(response.text)



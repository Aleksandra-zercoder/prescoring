import openai
import streamlit as st
from parse_hh import get_job_description

# Получение API-ключа из файла secrets.toml
openai.api_key = st.secrets["OPENAI_API_KEY"]

SYSTEM_PROMPT = """
Напишите краткий анализ, который объясняет, насколько кандидат соответствует требованиям вакансии. Оцените, как его опыт и навыки соотносятся с ключевыми задачами и обязанностями данной должности.

Проведите детальную оценку резюме кандидата. Проанализируйте, с какими задачами он сталкивался на предыдущих местах работы, как именно решал эти задачи, какие методы использовал, и какие результаты были достигнуты. Особое внимание уделите тому, как кандидат презентует свои проекты и достижения. Важно, чтобы кандидат мог четко и понятно рассказать о своей работе, своих проектах и опыте.

С учетом анализа резюме и соответствия кандидатуры требованиям вакансии, поставьте финальную оценку кандидата от 1 до 10. Выделите финальную оценку отдельно.
""".strip()


# Функция для запроса к GPT
def request_gpt(system_prompt, user_prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Используем gpt-3.5-turbo
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            max_tokens=800,
            temperature=0.1,
        )
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        st.error(f"Ошибка при обращении к API: {e}")
        return None

# Инициализация session_state для всех необходимых ключей с дефолтными значениями
if 'job_description' not in st.session_state:
    st.session_state['job_description'] = ''
if 'cv_info' not in st.session_state:
    st.session_state['cv_info'] = ''

# Основная функция для оценки кандидата
def evaluate_candidate(job_description_url, cv_text):
    # Получение описания вакансии
    if job_description_url.startswith("http"):
        job_description = get_job_description(job_description_url)
    else:
        job_description = job_description_url  # Если введен текст, используем его напрямую

    if job_description and cv_text:
        # Отправка данных в GPT для получения результата
        combined_input = f"Оценка кандидата по вакансии:\n\n{job_description}\n\nРезюме кандидата:\n\n{cv_text}"
        evaluation = request_gpt(SYSTEM_PROMPT, combined_input)
        return evaluation
    else:
        return "Ошибка при получении данных."

# Интерфейс Streamlit
st.title("Оценка кандидата")

# Используем .get() для безопасного доступа
job_description_url = st.text_input("Введите ссылку на описание вакансии или текст", value=st.session_state.get('job_description', ''))
cv_text = st.text_area("Введите текст резюме кандидата", value=st.session_state.get('cv_info', ''))

# Обновляем session_state с новыми значениями
st.session_state['job_description'] = job_description_url
st.session_state['cv_info'] = cv_text

if st.button("Оценить"):
    evaluation_result = evaluate_candidate(job_description_url, cv_text)
    st.write("Результат оценки:", evaluation_result)


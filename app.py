import streamlit as st
import json
import os
from tools import extract_text_from_pdf, score_resume
from openai import OpenAI

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.title("📄 AI Анализ резюме (мультиагентная система)")

st.header("⚙️ Настройка агентов")

analyst_role = st.text_input("Агент 1 (Аналитик)", "Анализирует резюме")
matcher_role = st.text_input("Агент 2 (Сопоставитель)", "Сравнивает с вакансией")
generator_role = st.text_input("Агент 3 (Генератор)", "Создает результат")

st.header("📥 Входные данные")

resume_file = st.file_uploader("Загрузите PDF резюме")
job_text = st.text_area("Вставьте текст вакансии")

with open("knowledge.txt", "r", encoding="utf-8") as f:
    knowledge = f.read()
USE_CREWAI = False
st.header("🚀 Запуск")

if st.button("Запустить анализ"):

    if resume_file is None or job_text.strip() == "":
        st.error("Загрузите файл и введите вакансию")
    else:
        resume_text = extract_text_from_pdf(resume_file)

        score, common = score_resume(resume_text, job_text)

        st.write(f"📊 Совпадение: {score:.2f}")

        memory = {}
        if os.path.exists("memory.json"):
            with open("memory.json", "r") as f:
                memory = json.load(f)

        analysis_prompt = f"""
        Ты аналитик резюме.
        Резюме:
        {resume_text}

        Выдели навыки и опыт.
        """

        analysis = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": analysis_prompt}]
        ).choices[0].message.content

        st.subheader("🧠 Анализ резюме")
        st.write(analysis)

        match_prompt = f"""
        Сравни резюме и вакансию.

        Резюме:
        {resume_text}

        Вакансия:
        {job_text}

        Совпадение слов: {common}

        Дай оценку соответствия.
        """

        match = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": match_prompt}]
        ).choices[0].message.content

        st.subheader("🔍 Сопоставление")
        st.write(match)

        if score < 0.5:
            st.warning("⚠️ Недостаточно данных — требуется уточнение")

            question = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{
                    "role": "user",
                    "content": "Задай 1 короткий уточняющий вопрос кандидату"
                }]
            ).choices[0].message.content

            st.write("❓ Вопрос:", question)

            user_answer = st.text_input("Ваш ответ")

        else:
            user_answer = ""

        final_prompt = f"""
        Используй знания:
        {knowledge}

        Резюме:
        {resume_text}

        Вакансия:
        {job_text}

        Ответ пользователя:
        {user_answer}

        Сгенерируй:
        1. Краткое summary
        2. Cover letter
        3. Рекомендации
        """

        result = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": final_prompt}]
        ).choices[0].message.content

        st.subheader("📄 Результат")
        st.write(result)


        st.subheader("✍️ Проверка человеком (HITL)")
        edited = st.text_area("Отредактируйте результат", result)

        if st.button("Подтвердить"):
            st.success("Финальная версия:")
            st.write(edited)

        memory["last_score"] = score
        memory["skills"] = common

        with open("memory.json", "w") as f:
            json.dump(memory, f)
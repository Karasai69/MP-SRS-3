import streamlit as st
from crewai import Crew
from agents import create_agents
from tasks import create_tasks
from tools import extract_text_from_pdf, score_resume
import json
import os

st.title("📄 Анализ резюме и вакансии (Multi-Agent AI)")

# =========================
# 🔹 ЗОНА 1 — КОНФИГ
# =========================

st.header("⚙️ Настройка агентов")

role_input = st.text_input("Роль генератора", "Карьерный консультант")
goal_input = st.text_area("Цель", "Помочь получить работу")

# =========================
# 🔹 ЗОНА 2 — ВХОД
# =========================

st.header("📥 Входные данные")

resume_file = st.file_uploader("Загрузите PDF резюме")
job_text = st.text_area("Вставьте текст вакансии")

# =========================
# 🔹 ЗОНА 3 — ЗАПУСК
# =========================

st.header("🚀 Запуск системы")

if st.button("Запустить"):

    if resume_file is None or job_text == "":
        st.error("Загрузите файл и вставьте вакансию")
    else:
        # 📄 Извлечение текста
        resume_text = extract_text_from_pdf(resume_file)

        # 📊 Скоринг
        score, common = score_resume(resume_text, job_text)

        st.write(f"Совпадение: {score:.2f}")

        # 🤖 Агенты
        extractor, matcher, clarifier, generator = create_agents()

        # 📋 Задачи
        tasks = create_tasks(extractor, matcher, clarifier, generator, score)

        # 🧠 Memory
        memory_data = {}
        if os.path.exists("memory.json"):
            with open("memory.json", "r") as f:
                memory_data = json.load(f)

        # 🚀 Crew
        crew = Crew(
            agents=[extractor, matcher, clarifier, generator],
            tasks=tasks,
            memory=True
        )

        result = crew.kickoff()

        st.subheader("📊 Результат")
        st.write(result)

        # 💾 Сохранение memory
        memory_data["last_score"] = score
        memory_data["skills"] = common

        with open("memory.json", "w") as f:
            json.dump(memory_data, f)

        # =========================
        # 👤 HITL
        # =========================

        st.subheader("✍️ Проверка человеком (HITL)")

        edited = st.text_area("Отредактируйте перед финалом", result)

        if st.button("Подтвердить финал"):
            st.success("Финальная версия:")
            st.write(edited)
from crewai import Agent

extractor = Agent(
    role="Аналитик",
    goal="Извлечь навыки",
    backstory="HR эксперт"
)

matcher = Agent(
    role="Сопоставитель",
    goal="Сравнить резюме",
    backstory="Рекрутер"
)

generator = Agent(
    role="Генератор",
    goal="Создать итог",
    backstory="Карьерный консультант"
)
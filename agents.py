from crewai import Agent

def create_agents():

    extractor = Agent(
        role="Аналитик резюме",
        goal="Извлечь навыки и опыт из резюме",
        backstory="Ты эксперт HR с опытом анализа кандидатов"
    )

    matcher = Agent(
        role="Сопоставитель",
        goal="Сравнить резюме с вакансией",
        backstory="Ты специалист по подбору персонала"
    )

    clarifier = Agent(
        role="Уточняющий агент",
        goal="Запросить недостающую информацию",
        backstory="Ты задаешь точные вопросы кандидату"
    )

    generator = Agent(
        role="Карьерный консультант",
        goal="Создать итоговый результат",
        backstory="Ты помогаешь людям получать работу"
    )

    return extractor, matcher, clarifier, generator
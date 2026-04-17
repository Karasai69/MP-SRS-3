from crewai import Task
from crewai.tasks.conditional_task import ConditionalTask

def create_tasks(extractor, matcher, clarifier, generator, score):

    task1 = Task(
        description="Извлечь ключевые навыки и опыт из резюме",
        expected_output="Список навыков и опыта",
        agent=extractor
    )

    task2 = Task(
        description="Сравнить резюме с вакансией и определить совпадение",
        expected_output="Процент совпадения",
        agent=matcher
    )

    # 🔀 Условие
    def condition_fn(context):
        return score < 0.5

    conditional_task = ConditionalTask(
        description="Если данных недостаточно — задай уточняющий вопрос пользователю",
        expected_output="Уточняющий вопрос",
        agent=clarifier,
        condition=condition_fn
    )

    task3 = Task(
        description="Создать summary, cover letter и рекомендации",
        expected_output="Готовый текст",
        agent=generator
    )

    return [task1, task2, conditional_task, task3]
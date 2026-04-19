from crewai import Task

task1 = Task(
    description="Извлечь навыки",
    expected_output="Список навыков"
)

task2 = Task(
    description="Сравнить с вакансией",
    expected_output="Совпадение"
)

task3 = Task(
    description="Сгенерировать результат",
    expected_output="Финальный текст"
)
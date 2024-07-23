from classes.engine import HH

"""В этом файле вам необходимо реализовать интерфейс взаимодействия с парсером через консоль
А именно
- 1 предложить пользователю выбрать вакансию для поиска;

- 2 спросить сколько вакансий просмотреть от 20 до 200 c шагом 20 вакансий 
(понадобится дополнительный параметр в __init__) который потом надо будет реализовать в теле метода get_request();
- 3 спросить нужна ли сортировка по зарплате;
- 4 спросить сколько отсортированных вакансий вывести;
- 5 добавить докстринги в файле engine.py;
- 6 (дополнительно) добавить возможные исключения.

Для того чтобы это все работало
вам будет необходимо несколько модифицировать код который находится в пакете classes внутри файла engine.py
"""
user_input_vacancy = None
vacancies_quantity_to_proceed = None
vacancies_per_pages_list = [i for i in range(20, 201, 20)]
user_choice_yes_no = ["да", "нет"]

# while not user_input_vacancy:
#     user_input_vacancy = input("Введите название вакансии для поиска: ")

while True:
    for idx, i in enumerate(vacancies_per_pages_list, 1):
        print(f"{idx}. {i}")
    user_choice_vacancies_quantity = input("Выберете количество вакансий для вывода: ")
    if user_choice_vacancies_quantity.isdigit():
        if 1 <= int(user_choice_vacancies_quantity) <= len(vacancies_per_pages_list):
            vacancies_quantity_to_proceed = int(vacancies_per_pages_list[int(user_choice_vacancies_quantity) - 1])
            break
    else:
        print("Неверный выбор. Попробуйте снова.")

while True:
    print('Сортировать по зарплате?')
    for idx, choice_y_n in enumerate(user_choice_yes_no, 1):
        print(f"{idx}. {choice_y_n}")
    user_choice_is_sort = input("Выберите: ")
    if user_choice_is_sort.isdigit():
        if 1 <= int(user_choice_is_sort) <= len(user_choice_yes_no):
            user_choice_is_sort = user_choice_yes_no[int(user_choice_is_sort) - 1]
            if user_choice_is_sort == "нет":
                sort_by_salary = False
                break
            else:
                sort_by_salary = True
                while True:
                    user_choice_is_sort_yes__quantity = input(f"Сколько вакансий вывести?(Max {vacancies_quantity_to_proceed}): ")
                    if user_choice_is_sort_yes__quantity.isdigit():
                        if int(user_choice_is_sort_yes__quantity) <= int(vacancies_quantity_to_proceed):
                            sorted_vacancies_quantity = int(user_choice_is_sort_yes__quantity)
                            print(f"Выбрано количество вакансий для сортировки: {sorted_vacancies_quantity}")
                            break
                        else:
                            print("Неверный выбор. Попробуйте снова.")
                    else:
                        print("Неверный выбор. Попробуйте снова.")
            break
        else:
            print("Неверный выбор. Попробуйте снова.")
    else:
        print("Неверный выбор. Попробуйте снова.")


# vacancy_to_search = user_input_vacancy
vacancy_to_search = "маляр"
hh = HH(vacancy_to_search, vacancies_quantity_to_proceed)
my_vacaincies_list = hh.get_request()
hh.make_json(vacancy_to_search, my_vacaincies_list)
if sort_by_salary:
    sorted_vacancies = hh.sorting(vacancy_to_search, True, my_vacaincies_list, sorted_vacancies_quantity)
    for vacancy in sorted_vacancies:
        print(vacancy)
else:
    vacancies_list = hh.for_console_output(my_vacaincies_list)
    for vacancy in vacancies_list:
        print(vacancy)
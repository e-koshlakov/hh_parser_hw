import math

import requests
import json
from abc import ABC, abstractmethod


class Engine(ABC):
    """ Абстрактный класс для создания движков поиска вакансий """

    @abstractmethod
    def get_request(self):
        pass


class HH(Engine):
    """ Класс для поиска вакансий на сайте hh.ru.
    Принимает название вакансии и количество вакансий на странице.
    Возвращает список вакансий """
    vacancies_all = []
    vacancies_dicts = []

    def __init__(self, vacancy, vacancies_quantity):
        self.vacancy = vacancy
        self.vacancies_quantity = vacancies_quantity

    def get_request(self):
        """Метод для получения вакансий с сайта hh.ru"""
        for num in range(math.ceil(self.vacancies_quantity / 20)):
            url = 'https://api.hh.ru/vacancies'
            params = {
                'text': {self.vacancy},
                'areas': 113,
                'per_page': 20,
                'page': num,
                'only with salary': True
            }
            response = requests.get(url, params=params)
            info = response.json()
            if info is None:
                return "Данны не получены!"
            elif 'errors' in info:
                return info['errors'][0]['value']
            elif info['found'] == 0:
                return "Нет вакансий"
            else:
                for vacancy in range(20):
                    self.vacancies_all.append(vacancy)
                    if info['items'][vacancy]['salary'] is not None \
                            and info['items'][vacancy]['salary']['currency'] == 'RUR':
                        vacancy_dict = {'employer': info['items'][vacancy]['employer']['name'],
                                        'name': info['items'][vacancy]['name'],
                                        'url': info['items'][vacancy]['alternate_url'],
                                        'requirement': info['items'][vacancy]['snippet']['requirement'],
                                        'salary_from': info['items'][vacancy]['salary']['from'],
                                        'salary_to': info['items'][vacancy]['salary']['to']}
                        if vacancy_dict['salary_from'] is None:
                            vacancy_dict['salary_from'] = "не указано"
                        elif vacancy_dict['salary_to'] is None:
                            vacancy_dict['salary_to'] = "не указано"
                        self.vacancies_dicts.append(vacancy_dict)
        return self.vacancies_dicts

    """Метод для создания json файла с вакансиями"""

    @staticmethod
    def make_json(vacancy, vacancies_dicts):
        with open(f"{vacancy}_hh_ru.json", 'w', encoding='utf-8') as file:
            json.dump(vacancies_dicts, file, indent=2, ensure_ascii=False)
        return f"Вакансии добавлены в файл: {vacancy}_hh_ru.json"

    """Метод для сортировки вакансий по зарплате"""

    @staticmethod
    def sorting(filename, type_of_sort, vacancies, num_of_vacancies=None):
        vacancies_list = []
        for vacancy in vacancies:
            if not isinstance(vacancy['salary_from'], int):
                if vacancy['salary_from'].isdigit():
                    vacancy['salary_from'] = int(vacancy['salary_from'])
                else:
                    vacancy['salary_from'] = 0
        vacancies_sort = sorted(vacancies, key=lambda vacancy: vacancy['salary_from'], reverse=type_of_sort)
        for vacancy in vacancies:
            vacancies_list.append(f"""
        Наниматель: {vacancy['employer']}
        Вакансия: {vacancy['name']}
        Описание/Требования: {vacancy['requirement']}
        Заработная плата от {vacancy['salary_from']} до {vacancy['salary_to']}
        Ссылка на вакансию: {vacancy['url']}""")
        with open(f'{filename}_sorted_vacancies.json', 'w', encoding='utf-8') as file:
            json.dump(vacancies_sort, file, indent=2, ensure_ascii=False)
        return vacancies_list[:num_of_vacancies] if num_of_vacancies else vacancies_list

    """Метод для подготови вывода вакансий в консоль, если не выбрана сортировка по зарплате"""

    @staticmethod
    def for_console_output(vacancies):
        vacancies_list = []
        for vacancy in vacancies:
            vacancies_list.append(f"""
        Наниматель: {vacancy['employer']}
        Вакансия: {vacancy['name']}
        Описание/Требования: {vacancy['requirement']}
        Заработная плата от {vacancy['salary_from']} до {vacancy['salary_to']}
        Ссылка на вакансию: {vacancy['url']}""")
        return vacancies_list

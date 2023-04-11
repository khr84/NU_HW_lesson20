from django.core.management.base import BaseCommand
from django.core.exceptions import ObjectDoesNotExist
from hh_search_app.models import Region, Skill, Search_vacancy, Search_salary, Employer, Schedule, Currency, Vacancy
import os
import json

class Command(BaseCommand):

    def handle(self, *args, **options):

        path_str = os.path.join(os.getcwd(), 'hh_search_app', 'fill_db', 'region.json')
        with open(path_str, 'r', encoding='utf-8') as f:
            res = json.load(f)
        region_dict = res['regions']
        region_list = list(map(lambda x: (x[0], int(x[1])), region_dict.items()))
        for region in region_list:
            Region.objects.get_or_create(region_name = region[0], defaults={'region_name':region[0], 'region_id':region[1]})
        print('Region - ok')

        schedule_list = [{'name': 'Полный день', 'code': 'fullDay'},
                         {'name': 'Сменный график', 'code': 'shift'},
                         {'name': 'Гибкий график', 'code': 'flexible'},
                         {'name': 'Удаленная работа', 'code': 'remote'},
                         {'name': 'Вахтовый метод', 'code': 'flyInFlyOut'},
                         {'name': 'Unknown', 'code': 'None'}]
        for schedule in schedule_list:
            Schedule.objects.get_or_create(code=schedule['code'], defaults={'name':schedule['name'], 'code':schedule['code']})
        print('Schedule - ok')

        currency_list = [{'name': 'Манаты', 'code': 'AZN'},
                         {'name': 'Белорусские рубли', 'code': 'BYR'},
                         {'name': 'Евро', 'code': 'EUR'},
                         {'name': 'Грузинский лари', 'code': 'GEL'},
                         {'name': 'Киргизский сом', 'code': 'KGS'},
                         {'name': 'Тенге', 'code': 'KZT'},
                         {'name': 'Рубли', 'code': 'RUR'},
                         {'name': 'Гривны', 'code': 'UAH'},
                         {'name': 'Доллары', 'code': 'USD'},
                         {'name': 'Узбекский сум', 'code': 'UZS'},
                         {'name':'Unknown', 'code':'None'}]
        for cur in currency_list:
            Currency.objects.get_or_create(code=cur['code'], defaults={'name': cur['name'], 'code': cur['code']})
        print('Currency - ok')


        path_str = os.path.join(os.getcwd(), 'hh_search_app', 'fill_db', 'search_result.json')
        n = 0
        with open(path_str, 'r', encoding='UTF-8') as f:
            for line in f:
            # line = f.readline()
                res = json.loads(line)
                skill_list = res['requirements']
                for skill in skill_list:
                    skill_db = Skill.objects.filter(skill_name=skill['name'])
                    if not skill_db:
                        Skill.objects.create(skill_name=skill['name'])
                print('Skill by search - ok')
                search_strict = 1 if res['search_strict'] == 'true' else 0
                search_region = Region.objects.get(region_name=res['area'])
                try:
                    search_db = Search_vacancy.objects.get(search_str=res['keywords'], region_id=search_region, strict_search=search_strict)
                    search_db.delete()
                except ObjectDoesNotExist:
                    pass
                search = Search_vacancy.objects.create(search_str=res['keywords'],
                                              count_vacancy=res['count'],
                                              search_date=res['search_date'],
                                              region_id=search_region,
                                              strict_search=search_strict)
                for skill in skill_list:
                    skill_db = Skill.objects.get(skill_name=skill['name'])
                    search.skill_id.add(skill_db)
                Search_salary.objects.create(search_id=search,
                                             low_value=res['salary']['from'],
                                             high_value=res['salary']['to'],
                                             count_salary=res['salary']['vacancy_with_salary'])
                for vacancy in res['vacancy_list']:
                    # инфа по работодателю
                    employer_db, created = Employer.objects.get_or_create(emp_name=vacancy['empoyer']['name'],
                                                                 defaults={'emp_name': vacancy['empoyer']['name'],
                                                                           'emp_url': vacancy['empoyer']['url'],
                                                                           'emp_id': vacancy['empoyer']['id']})
                    # инфа по графику работы
                    schedule = vacancy.get('schedule', 'None')
                    schedule_db = Schedule.objects.get(code=schedule)
                    # инфа по валюте ЗП
                    salary_dict = vacancy.get('salary', dict())
                    currency = salary_dict.get('currency', 'None')
                    currency_db = Currency.objects.get(code=currency)
                    # обработка вакансии
                    try:
                        vacancy_db = Vacancy.objects.get(vacancy_url=vacancy['url'])
                        vacancy_db.delete()
                    except ObjectDoesNotExist:
                        pass
                    Vacancy.objects.create(search_id=search,
                                           vacancy_name=vacancy['name'],
                                           vacancy_url=vacancy['url'],
                                           salary_from=salary_dict.get('from', 'null'),
                                           salary_to=salary_dict.get('to', 'null'),
                                           salary_cur=currency_db,
                                           salary_grace=salary_dict.get('grace', 'null'),
                                           schedule=schedule_db,
                                           employer=employer_db)
                print('Vacancy by search - ok')
            print('search - ok')

from src.db_manager import DBManager
from src.hh import HeadHunterAPI


class Engine(DBManager, HeadHunterAPI):
    def __init__(self):
        print("ПАРСЕР HH")
        super().__init__()
        self.menu = []
        self.employers = self.get_companies_and_vacancies_count()

    def engine_menu(self):
        """Меню действий в выбранном запросе вакансий"""
        text_menu_first = ["Добавить организацию и вакансии с HH в БД", "Завершить сессию"]
        text_menu_second = ["Добавить организацию и вакансии с HH в БД", "Вывести среднюю зарплату по всем вакансиям",
                            "Вывести список всех вакансий, у которых зарплата выше средней",
                            "Вывести список всех вакансий, в названии которых содержатся ваше ключевое слово",
                            "Вывести список всех вакансий", "Завершить работу с программой"]
        while True:
            position_menu = 1
            if len(self.employers) > 0:
                print('-' * 30)
                for employer in self.employers:
                    print(f'{position_menu}: "{employer[0]}" Кол-во вакансий:{employer[1]}')
                    position_menu += 1
                print('-' * 30)
                for menu_second in text_menu_second:
                    print(f'{position_menu}: {menu_second}')
                    position_menu += 1
            else:
                print('-' * 30)
                for menu_first in text_menu_first:
                    print(f'{position_menu}: {menu_first}')
                    position_menu += 1
                print('-' * 30)
            position_name = int(input("Введите номер из списка:"))
            if position_name in range(1, len(self.employers) + 1):
                self.engine_submenu(self.employers[position_name - 1])
            elif position_name == len(self.employers) + 1:
                if len(self.employers) != 10:
                    employer_name = input("Введите название организации:")
                    self.search_add_bd_employers(employer_name)
                else:
                    print("\n Не может быть больше 10 организаций\n")
            elif position_name == len(self.employers) + 2 and len(self.employers) > 0:
                print(f"\n{'-' * 30} Вывести среднюю зарплату по всем вакансиям \n{'-' * 30}")
                print(f'Средняя заработная плата по  вакансиям: {int(self.get_avg_salary()[0][0])} руб')
                print('-' * 30)
                continue
            elif position_name == len(self.employers) + 3 and len(self.employers) > 0:
                print(f"\n{'-' * 20} Список вакансий, у которых зарплата выше средней {'-' * 50}")
                for vacancy in self.get_vacancies_with_higher_salary():
                    if vacancy[2] == vacancy[3]:
                        salary = f" {vacancy[2]} руб"
                    else:
                        salary = f" от {vacancy[2]}руб до {vacancy[3]}руб"
                    print(f" Организация:{vacancy[0]},\n Должность:{vacancy[1]}\n Зарплата{salary}\n"
                          f"Ссылка на вакансию:{vacancy[4]}")
                    print('-' * 50)
                continue
            elif position_name == len(self.employers) + 4 and len(self.employers) > 0:
                word = input("Ключевое слово для поиска вакансий:")
                print(f"\n{'-' * 30} Список вакансий, в названии которых есть ключевое слово {'-' * 30}")
                for vacancy in self.get_vacancies_with_keyword(word):
                    if vacancy[2] == vacancy[3]:
                        salary = f" {vacancy[2]} руб"
                    else:
                        salary = f" от {vacancy[2]} руб до {vacancy[3]} руб"
                    print(f" Организация:{vacancy[0]}\n Должность:{vacancy[1]}\n Зарплата{salary}\n "
                          f"Ссылка на вакансию:{vacancy[4]}")
                    print('-' * 30)
                continue
            elif position_name == len(self.employers) + 5 and len(self.employers) > 0:
                print(f"\n{'-' * 30} Список вакансий {'-' * 30}")
                for vacancy in self.get_all_vacancies():
                    if vacancy[2] == vacancy[3]:
                        salary = f" {vacancy[2]} руб"
                    else:
                        salary = f" от {vacancy[2]} руб до {vacancy[3]} руб"
                    print(f" Организация:{vacancy[0]}\n Должность:{vacancy[1]}\n Зарплата{salary}\n "
                          f"Ссылка на вакансию:{vacancy[4]}\n")
                    print('-' * 30)
                continue
            elif (position_name == len(self.employers) + 6 and len(self.employers) > 0) or \
                    (position_name == len(self.employers) + 2 and len(self.employers) == 0):
                break
            else:
                print("\nВведите цифру из списка")

    def engine_submenu(self, employer):
        """Подменю действий в выбранном запросе вакансий"""
        text_menu_query = '1: Вывести список  вакансий данной организации\n' \
                          '2: Удалить организацию из списка\n' \
                          '3: Назад\n'
        while True:
            print(f'\n"{employer[0]}" Кол-во вакансий:{employer[1]}')
            print('-' * 30)
            print(text_menu_query)
            position_name = int(input("Введите номер:"))
            if position_name == 1:
                print('-' * 30)
                for vacancy in self.get_one_employer_all_vacancies(employer[2]):
                    if vacancy[2] == vacancy[3]:
                        salary = f" {vacancy[2]} руб"
                    else:
                        salary = f" от {vacancy[2]} руб до {vacancy[3]} руб"
                    print(f" Организация:{vacancy[0]}\n Должность:{vacancy[1]}\n Зарплата{salary}\n "
                          f"Ссылка на вакансию:{vacancy[4]}")
                    print('-' * 30)
                continue
            elif position_name == 2:
                self.del_companies_and_vacancies(employer[2])
                self.employers = self.get_companies_and_vacancies_count()
                break
            elif position_name == 3:
                break
            else:
                print("Вопрос задан некорректно")
            pass

    def search_add_bd_employers(self, name):
        """Меню для выбора организации"""
        data_employers = self.get_search_employers(name)
        i = 0
        end_search = True
        direction_point = True  # False - назад, True - вперёд
        course_point = 0
        while end_search:
            print(f'Найдено  {len(data_employers)} организаций')
            while True:
                if i < 20 and direction_point and 0 <= course_point < len(data_employers):
                    print(f'{course_point + 1}: {data_employers[course_point]["name"]}')
                    i += 1
                    if not course_point == len(data_employers) - 1:
                        course_point += 1
                    else:
                        i = 0
                        break
                elif i < 20 and not direction_point and 0 <= course_point < len(data_employers):
                    print(f'{course_point + 1}: {data_employers[course_point]["name"]}')
                    i += 1
                    if not course_point == 0:
                        course_point -= 1
                    else:
                        i = 0
                        break
                else:
                    i = 0
                    break
            point_employers = input(f'next - посмотреть следующие 20 компаний\nprev - посмотреть предыдущие 20 компаний\n'
                                    f'menu - назад в меню\n'
                                    f'Введите выбранную организацию для отслеживания вакансии: ')
            try:
                if point_employers.strip() == 'next':
                    direction_point = True
                    continue
                elif point_employers.strip() == 'prev':
                    direction_point = False
                    continue
                elif point_employers.strip() == 'menu':
                    break
                else:
                    hh_employer_vacancies = self.get_insert_vacancies(data_employers[int(point_employers) - 1]['id'])
                    self.add_companies_and_vacancies(data_employers[int(point_employers) - 1], hh_employer_vacancies)
                    # end_search = False
                    break
            except:
                print("\nВыберите в меню и введите нужную цифру или букву")
                course_point = 0

        self.employers = self.get_companies_and_vacancies_count()
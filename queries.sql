-- Команда для создания таблицы employers
CREATE TABLE public.employers (
                            id int,
                            name varchar(200) NOT NULL,
                            CONSTRAINT pk_public_employers_id PRIMARY KEY (id));

-- Команда для создания таблицы vacancies
CREATE TABLE public.vacancies (
                            id int,
                            employer_id int,
                            name varchar(100) NOT NULL,
                            salary_from int NOT NULL,
                            salary_to int NOT NULL,
                            url varchar(255) NOT NULL,
                            description text,
                            CONSTRAINT pk_vacancies PRIMARY KEY (id),
                            CONSTRAINT fk_employers_vacancies FOREIGN KEY(employer_id) REFERENCES public.employers(id))

-- Добавление организации и вакансий в базу данных
INSERT INTO public.employers VALUES (%s, %s), (employer_data['id'], employer_data['name']);
INSERT INTO public.vacancies VALUES (%s, %s, %s, %s, %s, %s, %s), vacancies_data);

-- Получает список всех компаний и количество вакансий у каждой компании
SELECT employers.name, COUNT(*), employers.id
FROM public.employers
JOIN public.vacancies ON employers.id = vacancies.employer_id
GROUP BY employers.name, employers.id
ORDER BY COUNT(employers.name) DESC;

-- Удаление из базы данных организацию и вакансии
DELETE FROM public.vacancies WHERE employer_id = %s;
DELETE FROM public.employers WHERE id = %s;

-- Получает список всех вакансий одной организации с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию
SELECT employers.name, vacancies.name, vacancies.salary_from, vacancies.salary_to, vacancies.url, vacancies.description
FROM public.employers
JOIN public.vacancies ON employers.id=vacancies.employer_id
WHERE employers.id = %s

-- Получает список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию
SELECT employers.name, vacancies.name, vacancies.salary_from, vacancies.salary_to, vacancies.url, vacancies.description
FROM public.employers
JOIN public.vacancies ON employers.id=vacancies.employer_id

-- Получает среднюю зарплату по всем вакансиям
SELECT AVG((salary_from + salary_to) / 2) AS salary
FROM public.vacancies

-- Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям
SELECT employers.name, vacancies.name, vacancies.salary_from, vacancies.salary_to, vacancies.url
FROM public.employers
JOIN public.vacancies ON employers.id=vacancies.employer_id
WHERE (vacancies.salary_from + vacancies.salary_to) / 2 > (SELECT AVG((salary_from + salary_to) / 2) FROM vacancies)
ORDER BY salary_from DESC

-- Получает список всех вакансий, в названии которых содержатся переданные в метод слова
SELECT employers.name, vacancies.name, vacancies.salary_from, vacancies.salary_to, vacancies.url
FROM public.employers
JOIN public.vacancies ON employers.id=vacancies.employer_id
WHERE LOWER(description) LIKE '%{word.lower()}%'






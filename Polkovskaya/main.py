import pandas as pd
import numpy as np
import os
import telebot
from telebot import types
from pathlib import Path
import matplotlib.pyplot as plt
from htmlwebshot import WebShot 
from func import do_picture
from token_for_bot import Token
import time



bot = telebot.TeleBot(Token)

def out(text):
    print('\033[1m\033[32m{}'.format(text), end='')
    print('\033[1m\033[31m{}'.format(''))


global not_main_rq, alf, df_examiners, df_students, df_exams, examiners_name
global date_of_exam, date_of_exam1, date_of_exam2, mark_by_exam, dict_date_of_exam


not_main_rq = ['Запрос на выборку']
alf = ['А', 'Б', 'В', 'Г', 'Д', 'Е', 'Ё', 'Ж', 'З', 'И', 'Й', 'К', 'Л', 'М',
 'Н', 'О', 'П', 'Р', 'С', 'Т', 'У', 'Ф', 'Х', 'Ц', 'Ч', 'Ш', 'Щ', 'Э', 'Ю', 'Я']
df_students = pd.read_excel(r'data/Data.xlsx', sheet_name='students')
df_examiners = pd.read_excel(r'data/Data.xlsx', sheet_name='examiners')
df_exams = pd.read_excel(r'data/Data.xlsx', sheet_name='exams')
examiners_name = list(df_examiners.examiner_name)
mark_by_exam = {
    'philosophy': 'philosophy_mark',
    'math': 'math_mark',
    'IKT': 'IKT_mark',
    'PE': 'PE_mark',
    'programming': 'programming_mark',
    'history': 'history_mark',
    'cultural_studies': 'cultural_studies_mark',
    'english': 'english_mark'
    }
dict_date_of_exam = {
    'philosophy': '2022-06-21',
    'math': '2022-06-22',
    'IKT': '2022-06-22',
    'PE': '2022-06-23',
    'programming': '2022-06-27',
    'history': '2022-06-27',
    'cultural_studies': '2022-06-27'
}


# date_of_exam = sorted(list(set(df_examiners.date.values)))
# date_of_exam = list(map(lambda x: x[:10], list(map(str, np.array(df_exams.values)[0]))))
date_of_exam = sorted(map(lambda x: x[:10], map(lambda x: str(x), list(set(df_examiners.date.values)))))
date_of_exam1 = ''
date_of_exam2 = ''
@bot.message_handler(commands=['start', 'restart'])
def welcome(message):
    """
    Функция приветствия
    """

    out(f'Отправлено сообщение:\n {message.text}\t от\t{message.from_user.username}')
    start = types.ReplyKeyboardMarkup(row_width=1)
    btn_start = 'Начать'
    start.add(btn_start)
    bot.send_message(message.from_user.id, 'Этот бот создан для работы с тестовой базой данных',
                     reply_markup=start)
    time.sleep(1)
    bot.send_sticker(message.from_user.id, 'CAACAgIAAxkBAAEFNCZixXvz226_cCpfszkWsxGjNhmaGQAC-BAAAuO_SEpmmeh30LPWwSkE')


@bot.message_handler(func=lambda message: True)
def other_text(message):

    global not_main_rq, alf, df_exams, df_examiners, df_students, examiners_name
    global date_of_exam,date_of_exam1, date_of_exam2, mark_by_exam


    out(f'Отправлено сообщение:\n {message.text}\t от\t{message.from_user.username}')

    rq = types.ReplyKeyboardMarkup(row_width=1)
    button_1 = 'Автоформа в столбец' # Done!
    button_2 = 'Форма с Подчиненной формой' # Done!
    button_3 = 'Запрос на выборку' # Done!
    button_4 = 'Запрос с параметром' # Done!
    button_5 = 'Запрос с вычисляемыми полями' # Done!
    button_6 = 'Итоговый запрос' # Done!
    button_7 = 'Запрос на создание базовой таблицы' # Done!
    button_8 = 'Запрос на удаление' # Done!
    button_9 = 'Запрос на обновление' # Done!
    button_10 = 'Автоотчет в столбец' # Done!
    button_11 = 'Отчет, созданный средствами Мастера отчетов' #

    rq.add(button_1, button_2, button_3, button_4, button_5, button_6, button_7, button_8, button_9,
                   button_10, button_11)
    if message.text not in not_main_rq:
        bot.send_message(message.from_user.id, 'Обновляем запросы', reply_markup=rq)
    
    if message.text == 'Автоформа в столбец':
        df = df_students
        do_picture(df)
        photo = open(r'data/table.jpg', 'rb')
        time.sleep(1)
        bot.send_photo(message.from_user.id, photo)
        time.sleep(2)
        photo.close
    if message.text == 'Запрос на выборку':
        rq = types.ReplyKeyboardMarkup(row_width=1)
        button_1 = 'Сортировка по первой букве Фамилии' # Выводит таблицу со студентами, фамилии которых, начинающимеся на "И"
        button_2 = 'Сортировка по стоимости экзамена' # Выводит таблицу с экзаменаторами, стоимость экзамена у которых от 30 до 50
        button_3 = 'Сортировка по году рождения' # Выводит таблицу со студентами роившимися с 1980 года по 1990 год 
        rq.add(button_1, button_2, button_3)
        bot.send_message(message.from_user.id, 'Выберете тип запроса на выборку:', reply_markup=rq)
    if message.text == 'Сортировка по первой букве Фамилии':
        df = df_students
        df = df[df['Full_Name'].str.find('И')==0]
        if do_picture(df):
            photo = open(r'data/table.jpg', 'rb')
            time.sleep(1)
            bot.send_photo(message.from_user.id, photo)
            time.sleep(2)
            photo.close
    if message.text == 'Сортировка по году рождения':
        df = df_students
        new_df = df[(df.Year_of_birth >= '1980')&(df.Year_of_birth < '1990')]
        if do_picture(new_df):
            photo = open(r'data/table.jpg', 'rb')
            time.sleep(1)
            bot.send_photo(message.from_user.id, photo)
            time.sleep(2)
            photo.close
        else: bot.send_message(message.from_user.id, 'Нет информации по этим данным')
    if message.text == 'Запрос с параметром':
        rq = types. ReplyKeyboardMarkup(row_width=1)
        button_1 = 'Запрос с параметром - 1'
        button_2 = 'Запрос с параметром - 2'
        rq.add(button_1, button_2)
        bot.send_message(message.from_user.id, 
        '''
        Выберете тип запроса с параметром:

        1 - Выбирает из таблицы ЭКЗАМЕНАТОРЫ информацию об экзаменаторе по ФИО

        2 - Выбирает из таблиц информацию обо всех экзаменах в некоторый заданный интервал времени
        ''', reply_markup=rq)        
    if message.text == 'Запрос с параметром - 1': # DONE!
        rq = types. ReplyKeyboardMarkup(row_width=1)
        button_1 = str(examiners_name[0]); button_2 = str(examiners_name[1])
        button_3 = str(examiners_name[2]); button_4 = str(examiners_name[3])
        button_5 = str(examiners_name[4]); button_6 = str(examiners_name[5])
        button_7 = str(examiners_name[6])
        rq.add(button_1, button_2, button_3, button_4, button_5, button_6, button_7)
        bot.send_message(message.from_user.id, 'Выберете ФИО экзаменатора', reply_markup=rq)
    if message.text in examiners_name:
        df = df_examiners[df_examiners.examiner_name == message.text]
        bot.send_message(message.from_user.id,
        f'Имя: {df.examiner_name.values[0]}\nЭкзамен: {df.exam.values[0]}\nСтоимость экзамена: {df.cost.values[0]}')
    
        
    if (message.text == 'Запрос с параметром - 2' or len(message.text)==21):
                    
        if len(message.text)==21:
            date_of_exam1, date_of_exam2 = message.text.split('_')
            
            df = df_examiners[(df_examiners.date >= date_of_exam1) & (df_examiners.date <= date_of_exam2)]
            examiner_name = list(df.examiner_name.values)
            for i in range(5):
                examiner_name.append('')
            dt = list(map(lambda x: [x[:10]], list(map(str, np.array(df_exams.values)[0]))))
            for i in dt:
                for j in range(10):
                    i.append(i[0])
            exam_date ={i: dt[x] for x, i in enumerate(list(df_examiners.exam.values[(df_examiners.date >= date_of_exam1) & (df_examiners.date <= date_of_exam2)]))}
    
            exams = list(df_examiners.exam.values[(df_examiners.date >= date_of_exam1) & (df_examiners.date <= date_of_exam2)])
            out_df = pd.DataFrame(
                df_students.Full_Name
                ).join(df_students.Year_of_birth
                ).join(df_students.Address
                ).join(df_students.number_of_passport                
                ).join(pd.DataFrame({mark_by_exam[i]: df_students[mark_by_exam[i]] for i in exams})
                ).join(
                    df_examiners.examiner_name[
                        (df_examiners.date >= date_of_exam1) & (df_examiners.date <= date_of_exam2)
                        ]
                ).join(
                    pd.DataFrame({i: [dict_date_of_exam[i] for _ in range(11)] for i in exams})
                )
            do_picture(out_df)
            if do_picture(out_df):
                photo = open(r'data/table.jpg', 'rb')
                time.sleep(1)
                bot.send_photo(message.from_user.id, photo)
                time.sleep(2)
                photo.close
                # print(f'date_of_exam1 - {date_of_exam1}\ndate_of_exam2 - {date_of_exam2}')
                date_of_exam1 = ''
                date_of_exam2 = ''
            else: bot.send_message(message.from_user.id, 'Нет информации по этим данным')
        
        else:
            bot.send_message(message.from_user.id, 'Введите дату по образцу ГГГГ-ММ-ДД_ГГГГ-ММ-ДД')
            bot.send_message(message.from_user.id, 'Где первая дата - начало выборки по дате экзаменов, а вторая - конец')
            bot.send_message(message.from_user.id, f'Даты проведения экзаменов: {str(date_of_exam)[1:-1]}')

    if message.text == 'Форма с Подчиненной формой':
        df = df_students.join(pd.DataFrame(
            {i: [dict_date_of_exam[i] for _ in range(11)] for i in list(df_examiners.exam.values)}
            ))
        do_picture(df)
        if do_picture(df):
            photo = open(r'data/table.jpg', 'rb')
            time.sleep(1)
            bot.send_photo(message.from_user.id, photo)
            time.sleep(2)
            photo.close
            date_of_exam1 = ''
            date_of_exam2 = ''
        else: bot.send_message(message.from_user.id, 'Нет информации по этим данным')
    
    if message.text == 'Сортировка по стоимости экзамена':
        df = df_examiners[(df_examiners.cost >=30) & (df_examiners.cost <=50)]
        do_picture(df)
        if do_picture(df):
            photo = open(r'data/table.jpg', 'rb')
            time.sleep(1)
            bot.send_photo(message.from_user.id, photo)
            time.sleep(2)
            photo.close
            date_of_exam1 = ''
            date_of_exam2 = ''
        else: bot.send_message(message.from_user.id, 'Нет информации по этим данным')
    if message.text == 'Запрос с вычисляемыми полями':
        df = pd.DataFrame({
            'examiner_name': list(df_examiners.examiner_name.values),
            'cost_for_1_exam': list(df_examiners.cost.values),
            'date_of_exam': list(df_examiners.date.values),
            'exam': list(df_examiners.exam.values),
            'tax': list(map(lambda x: x*0.13, list(df_examiners.cost.values))),
            'salary': list(map(lambda x: (x - x*0.13)*len(list(df_students.Full_Name.values)), list(df_examiners.cost.values)))
        })
        do_picture(df)
        if do_picture(df):
            photo = open(r'data/table.jpg', 'rb')
            time.sleep(1)
            bot.send_photo(message.from_user.id, photo)
            time.sleep(2)
            photo.close
            date_of_exam1 = ''
            date_of_exam2 = ''
        else: bot.send_message(message.from_user.id, 'Нет информации по этим данным')
    if message.text == 'Итоговый запрос':
        rq = types. ReplyKeyboardMarkup(row_width=1)
        button_1 = 'Итоговый запрос - 1'
        button_2 = 'Итоговый запрос - 2'
        rq.add(button_1, button_2)
        bot.send_message(message.from_user.id, 
        '''
        Выберете тип запроса с параметром:

        1 - Выполняет группировку по полю Год рождения. Для каждой группы определяет количество абитуриентов

        2 - Выполняет группировку по полю Наименование дисциплины. Для каждой группы вычисляет среднее значение оценки
        ''', reply_markup=rq)
    if message.text == 'Итоговый запрос - 1':
        df = pd.DataFrame({
                '1981': ['Самсонов Роман Богдановч', '', '', '', '', '', '1 абитуриет'],
                '1983': ['Иванов Степан Фёдорович', '', '', '', '', '','1 абитуриет'],
                '1988': ['Носков Мариан Игнатович', '', '', '', '', '', '1 абитуриет'],
                '2000': ['Александров Харлампий Вячеславович', 'Аверкий Чеславович Волков', 
                        'Шашкова Елизавета Андреевна', 'Логинов Павел Юльевич',
                        'Богданов Федосий Устинович','Орехова Валерия Михайловна', '6 абитуриентов'],
                '2001': ['Зыкоа Емельян Тарасович', 'Рубен Антипович Вишняков', '', '', '', '', '2 абитуриента']
            })
        do_picture(df)
        if do_picture(df):
            photo = open(r'data/table.jpg', 'rb')
            time.sleep(1)
            bot.send_photo(message.from_user.id, photo)
            time.sleep(2)
            photo.close
            date_of_exam1 = ''
            date_of_exam2 = ''
        else: bot.send_message(message.from_user.id, 'Нет информации по этим данным')
    if message.text == 'Итоговый запрос - 2':
        df = pd.DataFrame({i: [str(round(np.mean((df_students[mark_by_exam[i]].values)), 2))] for i in list(df_examiners.exam.values)})
        do_picture(df)
        if do_picture(df):
            photo = open(r'data/table.jpg', 'rb')
            time.sleep(1)
            bot.send_photo(message.from_user.id, photo)
            time.sleep(2)
            photo.close
            date_of_exam1 = ''
            date_of_exam2 = ''
        else: bot.send_message(message.from_user.id, 'Нет информации по этим данным')
    
    if message.text == 'Запрос на создание базовой таблицы':
        rq = types. ReplyKeyboardMarkup(row_width=1)
        button_1 = 'Запрос на создание базовой таблицы - 1'
        button_2 = 'Запрос на создание базовой таблицы - 2'
        rq.add(button_1, button_2)
        bot.send_message(message.from_user.id, 
        '''
        Выберете тип запроса с параметром:

        1 - Создаёт таблицу "Encrollee_1988", содержащую информацию о абитуриентах 1988 года рождения

        2 - Создает копию таблицы Экзаменаторы с имененм "КОПИЯ_ЭКЗАМЕНАТОРЫ"
        ''', reply_markup=rq)



    if message.text == 'Запрос на создание базовой таблицы - 1':
        t_df = df_students.join(pd.DataFrame({'only_year': list(map(lambda x: str(x)[0:4], list(df_students.Year_of_birth.values)))}))
        df = (t_df[t_df.only_year=='1988']).drop(['only_year'], axis=1)
        do_picture(df)
        if do_picture(df):
            photo = open(r'data/table.jpg', 'rb')
            time.sleep(1)
            bot.send_photo(message.from_user.id, photo)
            bot.send_message(message.from_user.id, 'Таблица сохранена под названием "Encrollee_1988"')
            new_data = pd.ExcelWriter(r'data/Encrollee_1988.xlsx')
            df.to_excel(new_data, index=False)
            new_data.save()
            time.sleep(2)
            photo.close
            
        else: bot.send_message(message.from_user.id, 'Нет информации по этим данным')
    if message.text == 'Запрос на создание базовой таблицы - 2':
        new_data = pd.ExcelWriter(r'data/COPY_examiners.xlsx')
        df_examiners.to_excel(new_data, index=False)
        new_data.save()
        bot.send_message(message.from_user.id, 'Таблица сохранена под названием "COPY_examiners"')
        if do_picture(df_examiners):
            photo = open(r'data/table.jpg', 'rb')
            time.sleep(1)
            bot.send_photo(message.from_user.id, photo)
            time.sleep(2)
            photo.close
            
        else: bot.send_message(message.from_user.id, 'Нет информации по этим данным')
    if message.text == 'Запрос на удаление':
        df = pd.read_excel(r'data/COPY_examiners.xlsx')
        df = df.drop(labels=list((df[df.cost>100]).index), axis=0)
        new_data = pd.ExcelWriter(r'data/COPY_examiners.xlsx')
        df.to_excel(new_data, index=False)
        new_data.save()
        if do_picture(df):
            photo = open(r'data/table.jpg', 'rb')
            time.sleep(1)
            bot.send_photo(message.from_user.id, photo)
            time.sleep(2)
            photo.close
            
        else: bot.send_message(message.from_user.id, 'Нет информации по этим данным')

    if message.text == 'Запрос на обновление':
        df = pd.read_excel('data/COPY_examiners.xlsx')
        df.loc[df.cost <= 50, 'cost'] =  55
        new_data = pd.ExcelWriter(r'data/COPY_examiners.xlsx')
        df.to_excel(new_data, index=False)
        new_data.save()
        bot.send_message(message.from_user.id, 'Таблица обновлена')
        if do_picture(df):
            photo = open(r'data/table.jpg', 'rb')
            time.sleep(1)
            bot.send_photo(message.from_user.id, photo)
            time.sleep(2)
            photo.close
            
        else: bot.send_message(message.from_user.id, 'Нет информации по этим данным')
    if message.text == 'Автоотчет в столбец':
        df = df_examiners      
        if do_picture(df):
            photo = open(r'data/table.jpg', 'rb')
            time.sleep(1)
            bot.send_photo(message.from_user.id, photo)
            time.sleep(2)
            photo.close
            
        else: bot.send_message(message.from_user.id, 'Нет информации по этим данным')
    if message.text == 'Отчет, созданный средствами Мастера отчетов':
        df = pd.DataFrame({
            'date': ['21/06/22','22/06/22','22/06/22','24/06/22','27/06/22','27/06/22','27/06/22'],
            'examiner_name': ['Гришина Марина Дмитриевна','Михайлов Парфен Устинович',
                'Полковская Марина Николаевна','Сидорова Оксана Николаевна','Салина Вера Игоревна',
                'Дорофеева Элеонора Натановна','Селезнев Иван Феодосиевич'],
            'exam': ['philosophy','math','IKT','programming','history','cultural_studies','PE'],
            'cost': ['50','60','60','50','50','60','60']
        })  
        if do_picture(df):
            photo = open(r'data/table.jpg', 'rb')
            time.sleep(1)
            bot.send_photo(message.from_user.id, photo)
            time.sleep(2)
            photo.close
            
        else: bot.send_message(message.from_user.id, 'Нет информации по этим данным')

bot.infinity_polling()


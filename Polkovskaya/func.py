from operator import index
from htmlwebshot import WebShot
import pandas as pd
import os
from path import path, pic
def do_picture(df):
    """
    Функция принимает на вход датафрейм
    \nДалее Соxраняет картинку, и возвращает булевое значение
    \nTrue - таблица на картинке не пустая
    \nFalse - таблица на картинке пустая
    """
    try: 
        os.remove(pic+'.html')
        os.remove(pic+'.jpg')
    except FileNotFoundError: pass

    if not df.empty:
        df.to_html(pic+'.html', encoding='UTF-16', index=False)
        shot = WebShot()
        shot.create_pic(html=pic+'.html', output=pic+'.jpg', quality=100)
        return True
    else: 
        print('///EMPTY_DATAFRAME\\\\\\')
        return False



# df = pd.read_excel(r'data/Data.xlsx')
# do_picture(df)


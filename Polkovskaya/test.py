from hashlib import new
import pandas as pd
import numpy as np
import os
import telebot
from telebot import types
from pathlib import Path
import matplotlib.pyplot as plt
from htmlwebshot import WebShot # Тот ещё камшот
from func import do_picture
from token_for_bot import Token
import time
# from path import path, pic

df = pd.read_excel(r'data/Data.xlsx')
new_df = pd.DataFrame([])
# print(df := df[df.Full_Name.values[::][::][0] == 'C'])
#print(df)


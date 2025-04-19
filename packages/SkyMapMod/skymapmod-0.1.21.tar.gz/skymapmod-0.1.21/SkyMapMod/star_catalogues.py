import numpy as np

from .data.load_data import load_star_temperatures, load_star_brightness

from.zodiac import black_body_phot

#на вход подаем галактические координаты (l -- долгота, b -- широта) и массив длин волн, по которым строим спектр
#РАЗОБРАТЬСЯ С КОЭФФИЦИЕНТАМИ А -- НАДО ЛИ НОРМИРОВАТЬ НА C (КАЖЕТСЯ НАДО) А ЕЩЕ ВРОДЕ Я ЕГО ОТНОРМИРОВАЛА И ПОДГРУЗИЛА -- ПРОВЕРИТЬ
def star_spectrum(l, b, lmbd):
    j = int((1800 - round(l*10)) + 3600) #пересчет из галактических к позиции в массиве
    i = int(900 + round(b*10))
    star_brightness = load_star_brightness()
    star_temperatures = load_star_temperatures()    
    A = star_brightness[i][j]
    T = star_temperatures[i][j]
    print('Информация по звезде в этом пикселе: T = ', T, ', A = ', A, sep='')
    print('Техническая строчка: i = ', i, ', j = ', j, sep='')
    spectrum = A * black_body_phot(lmbd, T)
    return spectrum
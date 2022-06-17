import requests
import json
from aiohttp import request
from config import url_clinic
from datetime import datetime, timedelta

from aiogram import types
from aiogram.types import InlineKeyboardButton



"""парсинг направлений"""
def parse_speki():
    speki = requests.get(f'{url_clinic}/api/reservation/departments')
    json_data = json.loads(speki.text)
    specializacii = json_data['data']
    return specializacii

"""парсинг докторов в выбранном направлении"""
def parse_doctors(id_doctor):
    parse_docs = requests.get(f'{url_clinic}/api/reservation/doctors?f=1&d={id_doctor}')
    json_data = json.loads(parse_docs.text)
    docs = json_data['data']
    speki = docs[0]
    spek = speki['departmentName']
    return docs, spek

"""парсинг даты приемы выбранного доктора"""
def parse_doc_date(id_doctor):
    days = timedelta(days=30)
    date_start = datetime.today().strftime("%Y%m%d")
    date_end = (datetime.today() + days).strftime("%Y%m%d")
    parse = requests.get(f'{url_clinic}/api/reservation/schedule?st={str(date_start)}&en={str(date_end)}&doctor={str(id_doctor)}')
    result_parse = json.loads(parse.text)
    cache_perem = result_parse['data']
    docdata = cache_perem[0]
    dname = docdata['dname']
    free_date = docdata['intervals']
    dcode = docdata['dcode']
    return dname, free_date, dcode

"""парсинг время приемов выбранного доктора"""
def parse_doc_daytime(date, dcode):
    parse = requests.get(f'{url_clinic}/api/reservation/intervals?st={str(date)}&en={str(date)}&dcode={str(dcode)}')
    result_parse = json.loads(parse.text)
    """упростить"""
    docdata = result_parse['data']
    dates = docdata[0]
    free_date = dates['workdates']
    cache_perem = free_date[0]
    cache_perem = cache_perem[date]
    cache_perem = cache_perem[0]
    time = cache_perem['intervals']
    return time

"""меню для лечения, восстановления и диагностики"""
def menu_special(special):
    menu = types.InlineKeyboardMarkup(row_width=2)
    data = []
    speki = parse_speki()
    if special == 'heal':
        for spek in speki:
            if spek['groupName'] == 'Лечение':
                name = spek['name']
                id = f'special_{str(spek["id"])}'
                new_btn = (name, id)
                data.append(new_btn)
    elif special == 'repair':
        for spek in speki:
            if spek['groupName'] == 'Восстановление':
                name = spek['name']
                id = f'special_{str(spek["id"])}'
                new_btn = (name, id)
                data.append(new_btn)
    elif special == 'diagnostics':
        for spek in speki:
            if spek['groupName'] == 'Диагностика':
                name = spek['name']
                id = f'diagspecial_{str(spek["id"])}'
                new_btn = (name, id)
                data.append(new_btn)
    menu.add(*[InlineKeyboardButton(button[0], callback_data=button[1]) for button in data])
    menu.add(InlineKeyboardButton(text="Главное меню", callback_data="main"))
    return menu

"""меню выбора доктора диагностики"""
def menu_diag_doc(id):
    menu = types.InlineKeyboardMarkup(row_width=1)
    data = []
    date_max = datetime.today() + timedelta(29)
    doctors, spek = parse_doctors(id)
    for doctor in doctors:
        near_date = doctor["nearestDate"]
        date = datetime.strptime(near_date, '%d.%m.%Y')
        if date_max >= date:
            id = f'diagdoctorsID_{str(doctor["dcode"])}'
            name = doctor['name']
            sep = (name, id)
            data.append(sep)
    menu.add(*[InlineKeyboardButton(button[0], callback_data=button[1]) for button in data])
    menu.add(InlineKeyboardButton(text="Главное меню", callback_data="main"))
    return menu, spek

"""меню выбора доктора"""
def menu_doc(id):
    menu = types.InlineKeyboardMarkup(row_width=1)
    data = []
    date_max = (datetime.today() + timedelta(29))
    doctors, spek = parse_doctors(id)
    for doctor in doctors:
        near_date = doctor["nearestDate"]
        date = datetime.strptime(near_date, '%d.%m.%Y')
        if (date_max >= date):
            id = f'doctorsID_{str(doctor["dcode"])}'
            name = doctor['name']
            sep = (name, id)
            data.append(sep)
    menu.add(*[InlineKeyboardButton(button[0], callback_data=button[1]) for button in data])
    menu.add(InlineKeyboardButton(text="Главное меню", callback_data="main"))
    return menu, spek

"""меню даты приема доктора диагностики"""
def menu_diag_doc_date(id):
    menu = types.InlineKeyboardMarkup(row_width=3)
    data = []
    docname, dates, dcode = parse_doc_date(id)
    for doctor in dates:
        if doctor["isAvailable"] == True:
            date = datetime.strptime(doctor['workDate'], '%Y%m%d')
            name = date.strftime('%d.%m')
            id = f'diagdocdate_{str(dcode)}_{str(doctor["workDate"])}'
            sep = (name, id)
            data.append(sep)
    menu.add(*[InlineKeyboardButton(button[0], callback_data=button[1]) for button in data])
    menu.add(InlineKeyboardButton(text="Главное меню", callback_data="main"))
    return menu, docname

"""меню даты приема доктора"""
def menu_doc_date(id):
    menu = types.InlineKeyboardMarkup(row_width=4)
    data = []
    docname, dates, dcode = parse_doc_date(id)
    for doctor in dates:
        if doctor["isAvailable"] == True:
            date = datetime.strptime(doctor['workDate'], '%Y%m%d')
            name = date.strftime('%d.%m')
            id = f'docdate_{str(dcode)}_{str(doctor["workDate"])}'
            sep = (name, id)
            data.append(sep)
    menu.add(*[InlineKeyboardButton(button[0], callback_data=button[1]) for button in data])
    menu.add(InlineKeyboardButton(text="Главное меню", callback_data="main"))
    return menu, docname

"""меню время на дату доктора"""
def menu_doc_daytime(dcode, wdate):
    menu = types.InlineKeyboardMarkup(row_width=3)
    data = []
    for time in parse_doc_daytime(wdate, dcode):
        if time["isFree"] == True:
            id = f'timeID_{str(dcode)}_{str(time["time"])}'
            tiime = time['time']
            sep = (tiime, id)
            data.append(sep)
    menu.add(*[InlineKeyboardButton(button[0], callback_data=button[1]) for button in data])
    menu.add(InlineKeyboardButton(text="Главное меню", callback_data="main"))
    return menu, wdate
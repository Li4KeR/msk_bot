import logging
from datetime import datetime
#from sys import call_tracing
#from turtle import back

from aiogram import Bot, Dispatcher, executor, types
import asyncio
from aiogram.dispatcher.filters import Text

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import InlineKeyboardButton
from aiogram.utils import executor

from aiogram.contrib.middlewares.logging import LoggingMiddleware
from contextlib import suppress

from aiogram.utils.exceptions import (MessageToEditNotFound, MessageCantBeEdited, MessageCantBeDeleted, MessageToDeleteNotFound)

from config import TOKEN, operator, log_path
import keyboards
import logic
import parse

#############################################################


logging.basicConfig(level=logging.INFO, format = "%(asctime)s - %(levelname)s - %(funcName)s: %(lineno)d - %(message)s", filename=log_path, )

bot = Bot(token=TOKEN, parse_mode=types.ParseMode.HTML)

storage = MemoryStorage()

dp = Dispatcher(bot, storage=storage)
dp.middleware.setup(LoggingMiddleware())

"""создаём форму и указываем поля"""
class anketa(StatesGroup):
    id = State()                #tele_id
    name = State()              #ФИО
    phones = State()            #телефон
    spek = State()              #специализация
    doctor = State()            #какой врач
    time = State()              #время приема
    date_tr = State()           #дата приема
    comment = State()           #комент
    naprav = State()            #направление

"""Стартовое меню"""
@dp.message_handler(commands="start")
async def start(message: types.Message):
    await message.answer(text="Вас приветствует Московская клиника!\nВыберите тему обращения:", reply_markup=keyboards.main)

@dp.callback_query_handler(lambda call: "main" in call.data)
async def next_keyboard(call: types.CallbackQuery):
    await call.message.edit_text(text="Вас приветствует Московская клиника!\nВыберите тему обращения:")
    await call.message.edit_reply_markup(reply_markup=keyboards.main)
    await call.answer()

"""Информация"""
@dp.message_handler(commands="about")
async def start(message: types.Message):
    menu = types.InlineKeyboardMarkup(row_width=1)
    menu.add(   InlineKeyboardButton(text="Вызвать такси", url="https://3.redirect.appmetrica.yandex.com/route?start-lat=&start-lon=&end-lat=55.797301&end-lon=37.600127&ref=moscowclinic.ru&appmetrica_tracking_id=1178268795219780156&tariffClass=econom&lang=ru"),
                #InlineKeyboardButton(text="Такси Павелецкая", url="https://3.redirect.appmetrica.yandex.com/route?start-lat=&start-lon=&end-lat=55.730649&end-lon=37.642393&ref=moscowclinic.ru&appmetrica_tracking_id=1178268795219780156&tariffClass=econom&lang=ru"),
                InlineKeyboardButton(text="Главное меню", callback_data="main"))
    await message.answer(text=u"Многопрофильные медицинский центр в Москве. МРТ, УЗИ, рентген, гастроскопия, общеклинические анализы, массаж, мануальная терапия, физиотерапия, 25 лечебных направлений. Прием ведут более 60 опытных специалистов, доктора, кандидаты медицинских наук, врачи высшей категории.", reply_markup=menu)

    """Мой ID"""
@dp.message_handler(commands="myid")
async def start(message: types.Message):
    menu = types.InlineKeyboardMarkup(row_width=1)
    menu.add(InlineKeyboardButton(text="Главное меню", callback_data="main"))
    await message.answer(text="Ваш id: " + str(message.from_user.id), reply_markup=menu)

"""переход в главное меню через n сек"""
async def back_to_main(call: types.CallbackQuery, sleep_time: int = 0):
    await asyncio.sleep(sleep_time)
    await call.message.edit_text(text="Вас приветствует Московская клиника!\nВыберите тему обращения:")
    await call.message.edit_reply_markup(reply_markup=keyboards.main)

"""сброс fsm state call"""
async def reset_fsm_call(call: types.CallbackQuery, state: FSMContext):
    await asyncio.sleep(600)
    await call.message.edit_text(text="Вас приветствует Московская клиника!\nВыберите тему обращения:")
    await call.message.edit_reply_markup(reply_markup=keyboards.main)
    await state.finish()

"""сброс fsm state msg"""
async def reset_fsm_msg(message: types.Message, state: FSMContext):
    await asyncio.sleep(600)
    await message.delete()
    await message.edit_text(text="Вас приветствует Московская клиника!\nВыберите тему обращения:")
    await message.edit_reply_markup(reply_markup=keyboards.main)
    await state.finish()

"""меню оператор"""
@dp.callback_query_handler(lambda call: "operator" in call.data)
async def next_keyboard(call: types.CallbackQuery):
    await call.message.edit_text(text="Связь с оператором")
    await call.message.edit_reply_markup(reply_markup=keyboards.operator)
    await call.answer()

"""меню мои записи"""
@dp.callback_query_handler(lambda call: "menu_mythreat" in call.data)
async def next_keyboard(call: types.CallbackQuery):
    id_user = call.from_user.id
    data = logic.all_treat_pac(id_user)
    menu = types.InlineKeyboardMarkup(row_width=2)
    if len(data) == 0:
        await call.message.edit_text(text="У Вас нет активных записей")
        menu.add(InlineKeyboardButton(text="Главное меню", callback_data="main"))
        await call.message.edit_reply_markup(reply_markup=menu)
    else:
        await call.message.edit_text(text="Ваши активные записи:")
        menu.add(*[InlineKeyboardButton(button[1], callback_data=f"custom_threat_{button[0]}") for button in data])
        menu.add(InlineKeyboardButton(text="Главное меню", callback_data="main"))
        await call.message.edit_reply_markup(reply_markup=menu)
    await call.answer()

"""показ информации пациенту о своей записи"""
@dp.callback_query_handler(Text(startswith="custom_threat_"))
async def callbacks_num(call: types.CallbackQuery):
    id_treat = call.data.split("_")[2]
    doc, tr_date, spek = logic.custom_treat(id_treat)
    menu = types.InlineKeyboardMarkup(row_width=2)
    menu.add(InlineKeyboardButton(text="Главное меню", callback_data="main"))
    await call.message.edit_text(text=f"Вы записаны к доктору\n{doc}\n{spek}\nПрием: {tr_date}")
    await call.message.edit_reply_markup(reply_markup=menu)
    await call.answer()

"""меню лечение"""
@dp.callback_query_handler(lambda call: "menu_heal" in call.data)
async def next_keyboard(call: types.CallbackQuery, state: FSMContext):
    asyncio.create_task(reset_fsm_call(call, state))
    menu = parse.menu_special('heal')
    await state.update_data(naprav="Лечение")
    await state.update_data(comment='Нет')
    await call.message.edit_text(text="Лечение:")
    await call.message.edit_reply_markup(reply_markup=menu)
    await call.answer()

"""меню восстановление"""
@dp.callback_query_handler(lambda call: "menu_repair" in call.data)
async def next_keyboard(call: types.CallbackQuery, state: FSMContext):
    asyncio.create_task(reset_fsm_call(call, state))
    menu = parse.menu_special('repair')
    await state.update_data(naprav="Восстановление")
    await state.update_data(comment=' ')
    await call.message.edit_text(text="Восстановление:")
    await call.message.edit_reply_markup(reply_markup=menu)
    await call.answer()

"""меню диагностики"""
@dp.callback_query_handler(lambda call: "menu_diagnostics" in call.data)
async def next_keyboard(call: types.CallbackQuery, state: FSMContext):
    menu = parse.menu_special('diagnostics')
    asyncio.create_task(reset_fsm_call(call, state))
    await state.update_data(naprav="Диагностика")
    await state.update_data(comment='Нет')
    await call.message.edit_text(text="Диагностика:")
    await state.update_data(time='111111')
    await call.message.edit_reply_markup(reply_markup=menu)
    await call.answer()

"""*************Если диагностика, то*************
    ловим выбор специализации диагностики и показываем докторов"""
@dp.callback_query_handler(Text(startswith="diagspecial_"))
async def callbacks_num(call: types.CallbackQuery, state: FSMContext):
    id_spec = call.data.split("_")[1]
    menu, special = parse.menu_diag_doc(id_spec)
    asyncio.create_task(reset_fsm_call(call, state))
    await state.update_data(spek=special)
    await call.message.edit_text(text="Выберете доктора:")
    await call.message.edit_reply_markup(reply_markup=menu)
    await call.answer()

"""ловим выбор доктора диагностики и показываем даты приема"""
@dp.callback_query_handler(Text(startswith="diagdoctorsID_"))
async def callbacks_num(call: types.CallbackQuery, state: FSMContext):
    id_spec = call.data.split("_")[1]
    menu, docname = parse.menu_diag_doc_date(id_spec)
    asyncio.create_task(reset_fsm_call(call, state))
    await state.update_data(doctor=docname)
    await call.message.edit_text(text="Доктор: " + str(docname) + "\n" +  "Выберете дату:")
    await call.message.edit_reply_markup(reply_markup=menu)
    await call.answer()

"""*************Если НЕ диагностика, то******************
    ловим выбор специализации и показываем докторов"""
@dp.callback_query_handler(Text(startswith="special_"))
async def callbacks_num(call: types.CallbackQuery, state: FSMContext):
    id_spec = call.data.split("_")[1]
    menu, special = parse.menu_doc(id_spec)
    asyncio.create_task(reset_fsm_call(call, state))
    await state.update_data(spek=special)
    await call.message.edit_text(text="Выберете доктора:")
    await call.message.edit_reply_markup(reply_markup=menu)
    await call.answer()

"""ловим выбор доктора и показываем даты приема"""
@dp.callback_query_handler(Text(startswith="doctorsID_"))
async def callbacks_num(call: types.CallbackQuery, state: FSMContext):
    id_spec = call.data.split("_")[1]
    menu, docname = parse.menu_doc_date(id_spec)
    asyncio.create_task(reset_fsm_call(call, state))
    await state.update_data(doctor=docname)
    await call.message.edit_text(text=f"Доктор: {str(docname)}\nВыберете дату:")
    await call.message.edit_reply_markup(reply_markup=menu)
    await call.answer()

"""ловим выбор даты и показываем время"""
@dp.callback_query_handler(Text(startswith="docdate_"))
async def callbacks_num(call: types.CallbackQuery, state: FSMContext):
    id_doc = call.data.split("_")[1]
    id_wdate = call.data.split("_")[2]
    docname = await state.get_data()
    menu, wdate = parse.menu_doc_daytime(id_doc, id_wdate)
    asyncio.create_task(reset_fsm_call(call, state))
    await state.update_data(date_tr=wdate)
    await call.message.edit_text(text=f"Доктор: {str(docname['doctor'])}\nВыберете время:") #str(id_doc)
    await call.message.edit_reply_markup(reply_markup=menu)
    await call.answer()

"""меню акций"""
#where i use it?
@dp.callback_query_handler(lambda call: "sale" in call.data)
async def next_keyboard(call: types.CallbackQuery):
    asyncio.create_task(back_to_main(call, 300))
    await call.message.edit_text(text="Акции")
    await call.message.edit_reply_markup(reply_markup=keyboards.sale)
    await call.answer()

"""Форма обратной связи"""
@dp.callback_query_handler(Text(startswith="timeID_"))
async def enter_name(call: types.CallbackQuery, state: FSMContext):
    id_wdate = call.data.split("_")[2]
    asyncio.create_task(reset_fsm_call(call, state))
    await call.answer()
    await state.update_data(time=id_wdate)
    await call.message.edit_text('Введите Ваши ФИО')
    await anketa.name.set()

"""Форма для диагностики"""
"""***************************************************"""
"""ловим начало формы диагностики и запускаем FSM"""
@dp.callback_query_handler(Text(startswith="diagdocdate_"))
async def callbacks_num(call: types.CallbackQuery, state: FSMContext):
    id_doc = call.data.split("_")[1]
    id_wdate = call.data.split("_")[2]
    menu, wdate = parse.menu_doc_daytime(id_doc, id_wdate) # для выбора времени добавить меню и обработку как в лечении\вос
    asyncio.create_task(reset_fsm_call(call, state))
    await call.answer()
    await state.update_data(date_tr=wdate)
    await call.message.answer('Введите Ваши ФИО')
    await anketa.name.set()

"""ловим стейт anketa.name"""
@dp.message_handler(state=anketa.name)
async def enter_phones(message: types.Message, state: FSMContext):
    answer = message.text
    asyncio.create_task(reset_fsm_msg(message, state))
    await state.update_data(id=message.from_user.id)
    await state.update_data(name=answer)
    await message.answer('Телефон')
    await anketa.phones.set()

"""ловим стейт anketa.phones"""
@dp.message_handler(state=anketa.phones)
async def enter_comm(message: types.Message, state: FSMContext):
    answer = message.text
    await state.update_data(phone=answer)
    data = await state.get_data()                       
    if str(data['naprav']) == 'Диагностика':                # если диагностика, то запрашиваем комент и передаем дальше.
        asyncio.create_task(reset_fsm_msg(message, state))        
        await message.answer('Комментарии')
        await anketa.comment.set()
    else:
        user_data = await state.get_data()
        await state.finish()
        
        user_info = [
            user_data['name'],
            user_data['phone'],
            user_data['comment'],
            user_data['id']
        ]

        tr_info = [
            user_data['doctor'],
            user_data['time'],
            user_data['date_tr'],
            user_data['spek']
        ]

        #Форматируем полученные данные
        date_pri = datetime.strptime(user_data['date_tr'], '%Y%m%d')
        date_pr = date_pri.strftime('%d.%m')
        date_time = f"{str(date_pr)} {str(user_data['time'])}"

        #для бд
        pacid = str(user_info[3])
        fio = str(user_info[0])
        doc = str(tr_info[0])
        dtime = str(date_time)
        comm = str(user_info[2])
        phone = str(user_info[1])
        spek = str(tr_info[3])
        date_cr = datetime.today()#.strftime('%d.%m.%Y-%H:%M'))
        acc = False

        data_pac = f'ФИО: {fio}\nТелефон: {phone}\nКоментарии: {comm}'
        tr_data= f'Врач: {doc}\nДата и время: {dtime}'
        data = data_pac + '\n' + tr_data

        #Пишем в бд отформатированные данные
        logic.ins_sql(pacid, fio, phone, doc, dtime, comm, spek, date_cr, acc)
        #Передаем информацию о записи оператору кц
        urll = f"tg://user?id={str(user_info[3])}"
        cb = types.InlineKeyboardMarkup(row_width=1)
        cb.add(InlineKeyboardButton(text='Написать пациенту', url=urll))
        cb.add(InlineKeyboardButton(text='Подтвердить', callback_data=f"accepted_{pacid}_{dtime}"))
        await bot.send_message(operator, f"Запись пользователя:\n{str(data)}", reply_markup=cb)
        #Оповещаем пациента о записи
        menu = types.InlineKeyboardMarkup(row_width=1)
        menu.add(InlineKeyboardButton(text="Главное меню", callback_data="main"))
        await message.answer(text=f"Вы записались к врачу: {doc}\nНаправление: {spek}\nДата и время: {dtime}\nДля подтверждения записи оператор свяжется с Вами в ближайшее время, спасибо за обращение!", reply_markup=menu)
        logic.send_mail(fio, phone, doc, comm, dtime)

"""ФСМ лечение и восстановление"""
"""ловим стейт коментов, пишем дату, передаем в кц и возвращаем юзеру"""
@dp.message_handler(state=anketa.comment)
async def print_anketa(message: types.Message, state: FSMContext):
    ans = message.text
    await state.update_data(comment=ans)
    await state.update_data(id=message.from_user.id)
    user_data = await state.get_data()
    await state.finish()

    user_info = [
        user_data['name'],
        user_data['phone'],
        user_data['comment'],
        user_data['id']
    ]

    tr_info = [
        user_data['doctor'],
        user_data['time'],
        user_data['date_tr'],
        user_data['spek']
    ]

    date_pri = datetime.strptime(user_data['date_tr'], '%Y%m%d')
    date_pr = date_pri.strftime('%d.%m')

    pacid = str(user_info[3])
    fio = str(user_info[0])
    doc = str(tr_info[0])
    dtime = str(date_pr)
    comm = str(user_info[2])
    phone = str(user_info[1])
    spek = str(tr_info[3])
    date_cr = datetime.today()
    acc = False

    logic.ins_sql(pacid, fio, phone, doc, dtime, comm, spek, date_cr, acc)
    data_pac = f'ФИО: {fio}\nТелефон: {phone}\nКоментарии: {comm}'
    tr_data= f'Врач: {doc}\nДата: {dtime}'

    data = f"{data_pac}\n{tr_data}"
    urll = f"tg://user?id={pacid}"
    cb = types.InlineKeyboardMarkup(row_width=1)
    cb.add(InlineKeyboardButton(text='Написать пациенту', url=urll))
    cb.add(InlineKeyboardButton(text='Подтвердить', callback_data=f"accepted_{pacid}_{dtime}"))
    await bot.send_message(operator, f"Запись пользователя: {str(data)}", reply_markup=cb)
    
    menu = types.InlineKeyboardMarkup(row_width=1)
    menu.add(InlineKeyboardButton(text="Главное меню", callback_data="main"))
    await message.answer(text=f"Вы записались к врачу: {doc}\nНаправление: {spek}\nДата: {dtime}\nДля подтверждения записи оператор свяжется с Вами в ближайшее время, спасибо за обращение!", reply_markup=menu)
    logic.send_mail(fio, phone, doc, comm, dtime)

"""Подтверждение пациента для БД КЦ"""
@dp.callback_query_handler(Text(startswith="accepted_"))
async def callbacks_num(call: types.CallbackQuery):
    pacid = call.data.split("_")[1]
    dtime = call.data.split("_")[2]
    acc_time = datetime.today()
    logic.update_acc_sql(pacid, dtime, acc_time)
    fio, phone, doc, date_pr = logic.info_acc_sql(pacid, dtime)
    menu = types.InlineKeyboardMarkup(row_width=1)
    urll = f"tg://user?id={pacid}"
    menu.add(InlineKeyboardButton(text='Написать пациенту', url=urll))
    await call.message.edit_text(text=f"Пациент подтвержден\nФИО: {str(fio)}\nТелефон: {str(phone)}\nДоктор: {str(doc)}\nДата приема: {str(date_pr)}")
    await call.message.edit_reply_markup(reply_markup=menu)
    await call.answer()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
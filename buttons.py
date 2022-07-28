from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

btn_uz_1 = KeyboardButton('Python dasturlash')
btn_uz_2 = KeyboardButton('Arhitektura va dizayn')
btn_uz_3 = KeyboardButton('Grafik dizayn')
btn_uz_4 = KeyboardButton('Kompyuter savodxonligi')
btn_uz_5 = KeyboardButton('Android dasturlash')
btn_uz_6 = KeyboardButton('Veb dasturlash')
btn_uz_7 = KeyboardButton('Mobil Robototexnika')

btn_ru_1 = KeyboardButton('Программирование на Python')
btn_ru_2 = KeyboardButton('Архитектура и дизайн')
btn_ru_3 = KeyboardButton('Графический дизайн')
btn_ru_4 = KeyboardButton('Компьютерная грамотность')
btn_ru_5 = KeyboardButton('Android-программирование')
btn_ru_6 = KeyboardButton('Веб-программирование')
btn_ru_7 = KeyboardButton('Мобильная робототехника')

can = KeyboardButton('/cancel')

kurs_btn_Uz = ReplyKeyboardMarkup(resize_keyboard=True).add(btn_uz_1, btn_uz_2, btn_uz_3).add(btn_uz_4, btn_uz_5, btn_uz_6).add(btn_uz_7, can)
kurs_btn_Ru = ReplyKeyboardMarkup(resize_keyboard=True).add(btn_ru_1, btn_ru_2, btn_ru_3).add(btn_ru_4, btn_ru_5, btn_ru_6).add(btn_ru_7, can)



ertalab = KeyboardButton('Ertalab')
abetdan = KeyboardButton('Abetdan keyin')

courseTime = ReplyKeyboardMarkup(resize_keyboard=True).add(ertalab, abetdan).add(can)


ru = KeyboardButton('RUS')
uz = KeyboardButton('UZ')
lang_btn = ReplyKeyboardMarkup(resize_keyboard=True).add(ru, uz).add(can)




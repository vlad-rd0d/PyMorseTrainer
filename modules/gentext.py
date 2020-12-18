#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        gentext.py
# Purpose:
#
# Author:      Vladimir Shchekunov RD0D
#
# Created:     14.12.2020
# Copyright:   (c) Vladimir Shchekunov RD0D 2020
# Licence:     GPL
#-------------------------------------------------------------------------------

import random
import string
import re

letters_rus = 'АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'
letters_eng = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
digits = '1234567890'
chars = '.,?`!/()&:;=+-_&@'
user_chars = ""

# шаблон регулярного выражения для генерирования позывных
regex = "(((1A|1M|1S|3A|3B6|3C|3DA|3V|3W|3X|3Y|3Y|4J|4L|4O|4S|4U|4U|4W|4W|4X|5A|5B|5H|5N|5R|5T|5U|5V|5W|5X|5Z|6W|6Y|7O|7O|7P|7Q|7X|8P|8Q|8R|9A|9G|\
        9H|9J|9K|9L|9N|9Q|9U|9V|9X|9Y|A[ABD]|AP|BV|BY|CE|CN|CO|CP|CT|CT3|CU|CX|DL|DU|EA|EI|EK|EL|EP|ER|ES|ET|E[UVW]|EX|EY|EZ|F|FF|FG|FH|FJ|FK|FM|FO|FP|FR|FS|\
        FW|FY|G|GD|GI|GJ|GM|GU|GW|HA|HB|HC|HH|HI|HK|HL|HP|HR|HS|HV|HZ|I|IS|JA|JD|JD|JT|JW|JX|JY|K|K[A-Z]|LA|LU|LX|LY|LZ|N|N[A-Z]|OA|OD|OE|OH|OK|OM|ON|OX|OY|OZ|\
        PA|PY|PZ|R|R[ACDEFGHIJKLMNOPQTUVWXYZ]|SM|SP|ST|SU|SV|TA|TF|TG|TI|TJ|TK|TL|TN|TR|TT|TU|TY|TZ|U[A-I]|UK|UN|U[RSTUVWXYZ]|VE|VK|VO|VU|W|W[A-Z]|XE|XT|XU|\
        XW|XZ|YB|YI|YJ|YK|YL|YN|YO|YS|YU|YV|ZA|ZB|ZC|ZF|ZL|ZP|ZS)\d[A-Z]{1,3})|((3B8|3B9|3C0|3D2|8Z4|8Z5|9M2|9M6|9S4|9U5|A1|A2|A3|A4|A40|A5|A6|A7|A9|AC3|\
        AC4|BS7|BV9|C2|C3|C5|C6|C9|C9|CE9|CN2|CR8|CY0|CY9|D2|D4|D6|E3|E4|E5|E6|E7|EA6|EA8|EA9|EA9|FI8|FN8|FO0|FQ8|H4|H40|H44|HB0|HC8|HK0|J2|J28|J3|J5|\
        J6|J7|J8|JZ0|KG4|KH0|KH1|KH2|KH3|KH4|KH5|KH6|KH8|KH9|KP1|KP2|KP4|KP5|KR6|KS4|KZ5|OH0|OJ0|P2|P29|P4|P40|P5|PJ2|PJ4|PJ5|PJ7|PK1|PK4|PK5|PK6|S0|\
        S2|S5|S7|S9|ST0|SV5|SV9|T2|T30|T31|T32|T33|T5|T6|T7|T8|TI9|UN1|V2|V3|V4|V5|V6|V7|V8|VK0|VK9|VP5|VP6|VP8|VP9|VQ1|VQ6|VQ9|VR2|VS2|VS4|VU4|VU7|XF4|\
        XX9|YV0|Z2|Z3|Z6|Z8|ZC5|ZC6|ZD4|ZD7|ZD8|ZD9|ZK3|ZL7|ZL8|ZL9|ZS0|ZS8|ZS9)[A-Z]{1,3})|((CE0X|CE0Y|CE0Z|KH5K|KH7K|KH8S|RI1F|RI1M|PY0F|PY0P|PY0T|\
        VP2E|VP2M|VP2V|VS9H|VS9K)[A-Z]{0,2})|((FT)\d[GJTWXZ][A-Z]{0,2}))"


CHAR_SET = [letters_eng, digits, letters_rus, letters_eng + digits, user_chars]


def gen_text(min_symbols, max_symbols, k, char_set):
    """
    Функция генерирует тренировочный текст
    min_symbols - минимальное кол-во символов в группе (слове)
    max_symbols - максимальное кол-во символов в группе (слове)
    k - кол-во групп (слов)
    char_set - набор символов для генерирования текста
    """
    result = ''
    for i in range(k):
        if min_symbols == max_symbols:
            l = max_symbols
        else:
            l = random.randint(min_symbols, max_symbols)
        if len(char_set) < 15:
            result += "".join(random.choice(char_set) for x in range(l)) + " "
        else:
            result += "".join(random.sample(char_set, l)) + " "
    return result


def gen_hamcall(n, groups):
    """
    Функция генерирует тренировочный текст из позывных
    n - длина сгенерированной строки
    groups - кол-во групп (слов)
    """
    result = ''
    count = 0
    char_set = CHAR_SET[3]
    while count < groups:
        #stroka = "".join(random.choice(char_set) for _ in range(n))
        stroka = "".join(random.sample(char_set, n))
        hamcall = re.findall(regex, stroka)
        for temp in hamcall:
            w = temp[0]
            call = re.search(regex, w)
            call = call.group(0)
            if len(call) > 3:
                result += call + " "
                count += 1
                if count == groups: break
    return result

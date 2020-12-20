# -*- coding: utf-8 -*-
from PyQt5 import QtCore
from pysine import sine


morse_code = {'A': '.-', 'a': '.-',
            'B': '-...', 'b': '-...',
            'C': '-.-.', 'c': '-.-.',
            'D': '-..', 'd': '-..',
            'E': '.', 'e': '.',
            'F': '..-.', 'f': '..-.',
            'G': '--.', 'g': '--.',
            'H': '....', 'h': '....',
            'I': '..', 'i': '..',
            'J': '.---', 'j': '.---',
            'K': '-.-', 'k': '-.-',
            'L': '.-..', 'l': '.-..',
            'M': '--', 'm': '--',
            'N': '-.', 'n': '-.',
            'O': '---', 'o': '---',
            'P': '.--.', 'p': '.--.',
            'Q': '--.-', 'q': '--.-',
            'R': '.-.', 'r': '.-.',
            'S': '...', 's': '...',
            'T': '-', 't': '-',
            'U': '..-', 'u': '..-',
            'V': '...-', 'v': '...-',
            'W': '.--', 'w': '.--',
            'X': '-..-', 'x': '-..-',
            'Y': '-.--', 'y': '-.--',
            'Z': '--..', 'z': '--..',
            'А': '.-', 'а': '.-',
            'Б': '-...', 'б': '-...',
            'В': '.--', 'в': '.--',
            'Г': '--.', 'г': '--.',
            'Д': '-..', 'д': '-..',
            'Е': '.', 'е': '.',
            'Ё': '.', 'ё': '.',
            'Ж': '...-', 'ж': '...-',
            'З': '--..', 'з': '--..',
            'И': '..', 'и': '..',
            'Й': '.---', 'й': '.---',
            'К': '-.-', 'к': '-.-',
            'Л': '.-..', 'л': '.-..',
            'М': '--', 'м': '--',
            'Н': '-.', 'н': '-.',
            'О': '---', 'о': '---',
            'П': '.--.', 'п': '.--.',
            'Р': '.-.', 'р': '.-.',
            'С': '...', 'с': '...',
            'Т': '-', 'т': '-',
            'У': '..-', 'у': '..-',
            'Ф': '..-.', 'ф': '..-.',
            'Х': '....', 'х': '....',
            'Ц': '-.-.', 'ц': '-.-.',
            'Ч': '---.', 'ч': '---.',
            'Ш': '----', 'ш': '----',
            'Щ': '--.-', 'щ': '--.-',
            'Ъ': '--.--', 'ъ': '--.--',
            'Ы': '-.--', 'ы': '-.--',
            'Ь': '-..-', 'ь': '-..-',
            'Э': '..-..', 'э': '..-..',
            'Ю': '..--', 'ю': '..--',
            'Я': '.-.-', 'я': '.-.-',
            '1': '.----',
            '2': '..---',
            '3': '...--',
            '4': '....-',
            '5': '.....',
            '6': '-....',
            '7': '--...',
            '8': '---..',
            '9': '----.',
            '0': '-----',
            '.': '.-.-.-',
            ',': '--..--',
            '?': '..--..',
            '`': '.----.',
            '!': '-.-.--',
            '/': '-..-.',
            '(': '-.--.',
            ')': '-.--.-',
            '&': '.-...',
            ':': '---...',
            ';': '-.-.-.',
            '=': '-...-',
            '+': '.-.-.',
            '-': '-....-',
            '_': '..--.-',
            # '«':'',
            # '»':'',
            # '"':'',
            '$': '...-..-',
            '@': '.--.-.',
            '>': '...-.-',
            '#': '...-',
            '<': '.',
            '%': '',
            '\u00b4': '.-..-.'}



class PlayThread(QtCore.QThread):
    playsignal = QtCore.pyqtSignal(str)
    #freq = 0
    #words_per_minute = 0
    #text = ""
    def  __init__(self, parent=None):
        QtCore.QThread.__init__(self, parent)
        self.freq = 0
        self.speed = 0
        self.text = ""

    def run(self):
        set_wpm = self.words(self.speed)
        self.sleep(2) # задержка в 2 сек.
        self.play_text(set_wpm, self.freq, self.text, morse_code)
        pass

    def set_params(self, freq, wpm, text):
        self.freq = freq
        self.speed = wpm
        self.text = text
        pass

    def words(self, words_per_minute):
        """ Вычисление продолжительности сигнала и интервалов для выбранной скорости WPM """
        # Для скорости 18 WPM  и выше:
        if words_per_minute >= 18:
            unit = 1.2 / words_per_minute
            dit = round(unit, 2)
            dah = round(unit * 3, 2)
            elem_space = round(unit, 2)
            char_space = round(unit * 3, 2)
            word_space = round(unit * 7, 2)
            wpm_settings = (dit, dah, elem_space, char_space, word_space)
        # Для скорости ниже 18 WPM:
        else:
            unit = 1.2 / 18
            dit = round(unit, 2)
            dah = round(unit * 3, 2)
            elem_space = round(unit, 2)
            char_speed = 18
            char_space = round(unit * 3, 2)
            word_space = round(unit * 7, 2)
            delay = ((60 * char_speed) - (37.2 * words_per_minute)) / (char_speed * words_per_minute)
            char_delay = 3 * delay / 19
            word_delay = 7 * delay / 19
            char_space += char_delay
            word_space += word_delay
            wpm_settings = (dit, dah, elem_space, round(char_space, 2), round(word_space, 2))
        return wpm_settings

    def play_text(self, set_wpm, freq, text, morse_code):
        """ Озвучиваем текст """
        dit = set_wpm[0]
        dah = set_wpm[1]
        elem_space = set_wpm[2]
        char_space = set_wpm[3]
        word_space = set_wpm[4]
        for word in text.split():
            PRINT_ON = True
            if word == '###':
                PRINT_ON = False
            elif word == '=':
                PRINT_ON = False
            elif word == '>':
                PRINT_ON = False
            elif word == '<<':
                PRINT_ON = False
            for character in word:
                letter = morse_code[character]
                for element in letter:
                    if element == '.':
                        sine(freq, dit)
                        sine(0, elem_space)
                    elif element == '-':
                        sine(freq, dah)
                        sine(0, elem_space)
                sine(0, char_space)
            if PRINT_ON:
                self.playsignal.emit(word + " ")
            sine(0, word_space)

# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
from modules.ui_formsetting import Ui_settingDialog


class fSetting(QtWidgets.QDialog):
    def __init__(self):
        super(fSetting, self).__init__()
        self.form = Ui_settingDialog()
        self.form.setupUi(self)

        self.buttons = {}

        self.min_chars = 0      # min кол-во символов в группе
        self.max_chars = 0      # max кол-во символов в группе
        self.groups = 0         # кол-во групп
        self.speed = 0          # скорость (wpm)
        self.tone = 0           # тон (Hz)
        self.char_set = 0       # набор символов (Lat, Rus, Number, Callsigns, User, File)
        self.prev_char_set = 0
        self.user_chars = 0     # символы пользователя


        self.accepted.connect(self.setNewParams)
        self.rejected.connect(self.changeCharSet)
        self.form.latcharsButton.toggled.connect(self.charSetsChange)
        self.form.ruscharsButton.toggled.connect(self.charSetsChange)
        self.form.numberButton.toggled.connect(self.charSetsChange)
        self.form.callsignsButton.toggled.connect(self.charSetsChange)
        self.form.usercharsButton.toggled.connect(self.charSetsChange)
        self.form.fileButton.toggled.connect(self.charSetsChange)

        #self.load_settings

    def setParams(self, params):
        self.min_chars = params[0]      # min кол-во символов в группе      
        self.max_chars = params[1]      # max кол-во символов в группе      
        self.groups = params[2]         # кол-во групп        
        self.speed = params[3]          # скорость (wpm)        
        self.tone = params[4]           # тон (Hz)           
        self.char_set = params[5]       # набор символов (Lat, Rus, Number, Callsigns, User, File)
        self.prev_char_set = self.char_set       
        self.user_chars = params[6]     # символы пользователя     
        self.form.minCharsBox.setValue(self.min_chars)
        self.form.maxCharsBox.setValue(self.max_chars)
        self.form.groupsBox.setValue(self.groups)
        self.form.speedBox.setValue(self.speed)
        self.form.toneBox.setValue(self.tone)
        self.form.userText.appendPlainText(self.user_chars)
        for button in self.form.charSetsBox.findChildren(QtWidgets.QRadioButton):
            tag = button.property("Tag")
            if tag == self.char_set:
                button.setChecked(True)
                break
        pass
   

    def closeEvent(self, event): 
        super().closeEvent(event)
        pass

    def changeCharSet(self):
        self.char_set = self.prev_char_set
        pass

    def setNewParams(self):
        self.min_chars = self.form.minCharsBox.value()
        self.max_chars = self.form.maxCharsBox.value()
        if self.min_chars > self.max_chars:
            self.min_chars, self.max_chars = self.max_chars, self.min_chars
        self.groups = self.form.groupsBox.value()
        self.speed = self.form.speedBox.value()
        self.tone = self.form.toneBox.value()
        self.user_chars = self.form.userText.toPlainText()
        pass

    def getParams(self):
        min_chars = self.min_chars
        max_chars = self.max_chars
        groups = self.groups
        speed = self.speed
        tone = self.tone
        char_set = self.char_set
        user_chars = self.user_chars
        return [min_chars, max_chars, groups, speed, tone, char_set, user_chars]
        pass

    def charSetsChange(self):
        sender = self.sender()
        if sender.isChecked():
            self.char_set = sender.property("Tag")
        pass

    # def setCheckedBtn(self):
    #     self.buttons[int(self.char_set)].setChecked(True)
    #     print(self.buttons[self.char_set].objectName(),self.buttons[self.char_set].property("Tag"), self.buttons[self.char_set].isChecked())
    #     print(self.spisok[self.char_set].objectName(), self.spisok[self.char_set].property("Tag"), self.spisok[self.char_set].isChecked())

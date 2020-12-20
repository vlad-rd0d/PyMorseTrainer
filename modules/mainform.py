# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtGui, QtWidgets
from modules.formsetting import fSetting
from modules.ui_mainform import Ui_MainForm
import modules.gentext as gen
import modules.morse as morse

CONFIG_FILE_NAME = 'pymorsetrainer.conf'

class fMain(QtWidgets.QMainWindow):
    def __init__(self):
        super(fMain, self).__init__()
        self.ui = Ui_MainForm()
        self.ui.setupUi(self)

        self.ui.outputText.insertPlainText("*** Hello Friend! Let's start the lesson? ***\n")

        self.ui.actionAbout.triggered.connect(self.on_about_click)
        self.ui.actionSetting.triggered.connect(self.on_setting_click)
        self.ui.actionExitApp.triggered.connect(self.on_exit_click)
        self.ui.actionNewText.triggered.connect(self.new_text)
        self.ui.actionStart.triggered.connect(self.on_play)

        self.min_chars = 0      # min кол-во символов в группе
        self.max_chars = 0      # max кол-во символов в группе
        self.groups = 0         # кол-во групп
        self.speed = 0          # скорость (wpm)
        self.tone = 0           # тон (Hz)
        self.char_set = 0       # набор символов (Lat, Rus, Number, Callsigns, User, File)
        self.user_chars = ''    # символы пользователя
        self.char_set_name = ['Lat', 'Number', 'Rus', 'Callsigns', 'User', 'File']
        self.text = ""
        self.load_settings()

    def new_text(self):
        fname = ""
        if self.char_set == 3:
            text = gen.gen_hamcall(20, self.groups)
        elif self.char_set == 4:
            charset = self.user_chars
            text = gen.gen_text(self.min_chars, self.max_chars, self.groups, charset)
        elif self.char_set != 5:
            charset = gen.CHAR_SET[self.char_set]
            text = gen.gen_text(self.min_chars, self.max_chars, self.groups, charset)
        else:
            fname = QtWidgets.QFileDialog.getOpenFileName(self, caption="Open File", directory="~", 
                    filter="All (*);;Txt (*.txt)", initialFilter="Txt (*.txt)")[0]
            print(fname)
            with open(fname, 'r') as f:
                text = str(f.readlines())
            pass
        if self.char_set != 5:
            #self.ui.statusbar.showMessage("Text generated done! Char set: %s, groups: %d" % (self.char_set_name[self.char_set], self.groups))
            self.statusBarMsg("Text generated done! Char set: %s, groups: %d" % 
                              (self.char_set_name[self.char_set], self.groups))
        else:
            #self.ui.statusbar.showMessage("Open file: %s" % fname)
            self.statusBarMsg("Open file: %s" % fname)
        self.text = "### = " + text + "> <<"
        pass


    def play_thread_started(self):
        self.ui.actionStart.setDisabled(True)
        self.statusBarMsg("Test started!")
        pass

    def play_thread_finished(self):
        self.ui.actionStart.setDisabled(False)
        self.statusBarMsg("Test finished!")
        pass
    
    def play_thread_running(self, s):
        self.ui.outputText.insertPlainText(s)
        self.ui.outputText.moveCursor(self.ui.textcursor.End)
        
    def on_play(self):
        if self.text == "":
            self.ui.outputText.setPlainText("* No text created! Click the \"New text\" button or Alt + N *")
        else:
            self.ui.outputText.clear()
            self.play_thread = morse.PlayThread()
            self.play_thread.set_params(self.tone, self.speed, self.text)
            self.play_thread.started.connect(self.play_thread_started)
            self.play_thread.finished.connect(self.play_thread_finished)
            self.play_thread.playsignal.connect(self.play_thread_running, QtCore.Qt.QueuedConnection)
            self.play_thread.start()
        pass

    def on_exit_click(self):
        self.close()

    def closeEvent(self, event):
        reply = QtWidgets.QMessageBox.question(self, "Exit", "Application exit?",
                QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel, QtWidgets.QMessageBox.Cancel)
        if reply == QtWidgets.QMessageBox.Ok:
            event.accept()
            self.save_settins()
        else:
            event.ignore()

    def on_setting_click(self):
        self.modal = fSetting()
        self.modal.setParams([self.min_chars, self.max_chars, self.groups, self.speed,
                    self.tone, self.char_set, self.user_chars])
        self.modal.exec_()
        [self.min_chars, self.max_chars, self.groups, self.speed, self.tone, self.char_set, self.user_chars] = self.modal.getParams()
        if self.char_set != 5:
            msg = "Char set: %s, groups: %d, speed: %d WPM" % (self.char_set_name[self.char_set], self.groups, self.speed)
        else:
            msg = "Char set: %s, speed: %d WPM" % (self.char_set_name[self.char_set], self.speed)                                                        
        self.statusBarMsg(msg)
        self.text = ""
        pass

    def load_settings(self):
        settings = QtCore.QSettings(CONFIG_FILE_NAME, QtCore.QSettings.IniFormat)
        self.min_chars = int(settings.value("Min_chars", 5))
        self.max_chars = int(settings.value("Max_chars", 5))
        self.groups = int(settings.value("Groups", 60))
        self.speed = int(settings.value("Speed", 12))
        self.tone = int(settings.value("Tone", 700))
        self.char_set = int(settings.value("Char_set", 0))
        self.user_chars = settings.value("User_chars", "")
        if self.char_set != 5:
            msg = "Char set: %s, groups: %d, speed: %d WPM" % (self.char_set_name[self.char_set], self.groups, self.speed)
        else:
            msg = "Char set: %s, speed: %d WPM" % (self.char_set_name[self.char_set], self.speed)                                                        
        self.statusBarMsg(msg)        
        pass

    def save_settins(self):
        settings = QtCore.QSettings(CONFIG_FILE_NAME, QtCore.QSettings.IniFormat)
        settings.setValue("Min_chars", self.min_chars)
        settings.setValue("Max_chars", self.max_chars)
        settings.setValue("Groups", self.groups)
        settings.setValue("Speed", self.speed)
        settings.setValue("Tone", self.tone)
        settings.setValue("Char_set", self.char_set)
        settings.setValue("User_chars", self.user_chars)
        settings.sync()

    def on_about_click(self):
        QtWidgets.QMessageBox.about(self, "About", "Morse Trainer Version 0.1\n\nMorse Trainer - program for studying and training in the reception of Morse code\n\nAuthor: Vlad Shchekunov, RD0D, 2020")
        pass
    
    def statusBarMsg(self, msg):
        self.ui.statusbar.showMessage(msg)
        pass

    def window_on_center(self):
        desktop = QtWidgets.QApplication.desktop()
        x = (desktop.width() - self.width()) // 2
        y = (desktop.height() - self.height()) // 2
        self.move(x,y)






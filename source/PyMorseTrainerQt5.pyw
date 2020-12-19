#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        Py Morse Trainer Qt5
# Purpose:
#
# Author:      Vladimir Shchekunov RD0D
#
# Created:     21.01.2020
# Copyright:   (c) Vladimir Shchekunov RD0D 2020
# Licence:     GPL
#-------------------------------------------------------------------------------
import sys
from PyQt5 import QtWidgets
from modules.mainform import fMain

def main():
    app = QtWidgets.QApplication([])
    application = fMain()
    application.window_on_center()
    application.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()

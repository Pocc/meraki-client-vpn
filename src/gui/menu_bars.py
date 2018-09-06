# -*- coding: utf-8 -*-
# Copyright 2018 Ross Jacobs All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""This class contains the menubars of the program."""
import sys

from PyQt5.QtWidgets import QAction
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QTextEdit

import src.modules.os_utils as os_utils
from src.gui.modal_dialogs import show_error_dialog


class MenuBars:
    """Menubars of the GUI

    This class contains mostly boilerplate Qt UI.

    Attributes:
        bar (QMenuBar): The Main Window's built-in menu bar object
        file_menu (QAction): File menu
        edit_menu (QAction): Edit menu
        help_menu (QAction): Help menu
    """

    # Telling PyCharm linter not to (incorrectly) inspect PyQt function args
    # noinspection PyArgumentList
    def __init__(self, bar):
        super(MenuBars, self).__init__()
        self.bar = bar
        self.file_menu = bar.addMenu('&File')
        self.edit_menu = bar.addMenu('&Edit')
        self.help_menu = bar.addMenu('&Help')

    def generate_menu_bars(self):
        """Create each of the menu bars.

        NOTE: Some of the menu additions here are planned features
        """

        # File options
        file_sysprefs = QAction('&Open VPN System Prefs', self.bar)
        file_sysprefs.setShortcut('Ctrl+O')
        file_quit = QAction('&Quit', self.bar)
        file_quit.setShortcut('Ctrl+Q')

        # Edit options
        edit_preferences = QAction('&Prefrences', self.bar)
        edit_preferences.setShortcut('Ctrl+P')

        # Help options
        help_support = QAction('Get S&upport', self.bar)
        help_support.setShortcut('Ctrl+U')
        help_about = QAction('A&bout', self.bar)
        help_about.setShortcut('Ctrl+B')

        self.file_menu.addAction(file_sysprefs)
        self.file_menu.addAction(file_quit)
        self.edit_menu.addAction(edit_preferences)
        self.help_menu.addAction(help_about)

        file_sysprefs.triggered.connect(self.file_sysprefs)
        file_quit.triggered.connect(sys.exit)
        edit_preferences.triggered.connect(self.edit_prefs_action)
        help_about.triggered.connect(self.help_about_action)

    @staticmethod
    def file_sysprefs():
        """Open system VPN settings

        Raises:
            FileNotFoundError: If vpn settings are not found
        """
        try:
            os_utils.open_vpnsettings()
        except FileNotFoundError as e:
            if sys.platform.startswith('linux'):
                show_error_dialog(
                    str(e) + '\n\nThis happens when gnome-network-manager is '
                    'not installed and systems vpn prefs are opened in linux.')
            else:
                show_error_dialog(str(e) + '\n\nUnknown error: VPN settings '
                                           'not found')

    @staticmethod
    def edit_prefs_action():
        """Shows the preferences

        Currently, it merely shows an HTML heading, but the hope is be able
        to control more settings from this pane.

        > It may be worthwhile to use a QSettings object here instead
        (http://doc.qt.io/qt-5/qsettings.html).
        """

        # Preferences should go here.
        # How many settings are here will depend on the feature set
        prefs = QDialog()
        layout = QVBoxLayout()
        prefs_heading = QLabel('<h1>Preferences</h1>')
        layout.addWidget(prefs_heading)
        prefs.setLayout(layout)
        prefs.show()

    @staticmethod
    def help_about_action():
        """Shows an about dialog containing the license."""
        about_popup = QDialog()
        about_popup.setWindowTitle("Meraki Client VPN: About")
        about_program = QLabel()
        about_program.setText("<h1>Meraki VPN Client 0.8.5</h1>\n"
                              "Developed by Ross Jacobs<br><br><br>"
                              "This project is licensed with the "
                              "Apache License, which can be viewed below:")
        license_text = open("LICENSE.txt").read()
        licenses = QTextEdit()
        licenses.setText(license_text)
        # People shouldn't be able to edit licenses!
        licenses.setReadOnly(True)
        popup_layout = QVBoxLayout()
        popup_layout.addWidget(about_program)
        popup_layout.addWidget(licenses)
        about_popup.setLayout(popup_layout)
        about_popup.setMinimumSize(600, 200)
        about_popup.exec_()
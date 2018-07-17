#!/usr/bin/python3

# ~ https://ux.stackexchange.com/questions/12045/what-is-a-modal-dialog-window
# "A modal dialog is a window that forces the user to interact with it
# before they can go back to using the parent application."

# Python modules
from PyQt5.QtWidgets import (QMessageBox, QLineEdit, QWidget, QPushButton,
                             QLabel, QVBoxLayout, QHBoxLayout, QDialog)
from PyQt5.QtGui import QPixmap

# Local modules
from src.modules.pyinstaller_path_helper import resource_path


def show_error_dialog(message):
    error_dialog = QMessageBox()
    error_dialog.setIcon(QMessageBox.Critical)
    error_dialog.setWindowTitle("Error!")
    error_dialog.setText(message)
    error_dialog.exec_()


def show_question_dialog(message):
    question_dialog = QMessageBox()
    question_dialog.setIcon(QMessageBox.Question)
    question_dialog.setWindowTitle("Error!")
    question_dialog.setText(message)
    question_dialog.setStandardButtons(QMessageBox.No | QMessageBox.Yes)
    question_dialog.setDefaultButton(QMessageBox.Yes)
    return show_question_dialog.exec_()


def show_feature_in_development_dialog():
    fid_message = QMessageBox()
    fid_message.setIcon(QMessageBox.Information)
    fid_message.setWindowTitle("Meraki Client VPN: Features in Progress")
    fid_message.setText('This feature is currently in progress.')
    fid_message.exec_()


def get_tfa_dialog():
    # QDialog that gets 6 digit two-factor code
    tfa_dialog = QDialog()
    tfa_dialog.setWindowTitle("Two-Factor Authentication")
    tfa_dialog_layout = QVBoxLayout()
    tfa_code_layout = QHBoxLayout()
    tfa_code_label = QLabel("Enter verification code")
    get_tfa_code = QLineEdit()

    # 'Remember choice' checkbox doesn't quite work yet
    # get_remember_choice = QCheckBox("Remember verification "
    #                                "for this computer for 30 days.")

    tfa_dialog_yesno = QHBoxLayout()
    yesbutton = QPushButton("Verify")
    yesbutton.setToolTip("Attempt connection with this two-factor code")
    nobutton = QPushButton("Cancel")
    yesbutton.setToolTip("Quit")
    tfa_dialog_yesno.addWidget(yesbutton)
    tfa_dialog_yesno.addWidget(nobutton)

    # Layout code
    tfa_code_layout.addWidget(tfa_code_label)
    tfa_code_layout.addWidget(get_tfa_code)
    tfa_dialog_layout.addLayout(tfa_code_layout)
    # dialog_layout.addWidget(self.get_remember_choice)
    tfa_dialog_layout.addLayout(tfa_dialog_yesno)
    tfa_dialog.setLayout(tfa_dialog_layout)

    # Forces you to interact with the dialog (desired behavior)
    # `self.twofactor_dialog.setModal(True)`
    # Wait on user to submit information to go here
    yesbutton.clicked.connect(tfa_submit_info)
    # wait on user to submit information to go here
    nobutton.clicked.connect(tfa_dialog.close())
    tfa_dialog.exec_()


def show_login_dialog():
    meraki_img = QLabel('<a href=https://meraki.cisco.com/products/wireless#mr-new>MR advertisement</a>')
    meraki_img.setOpenExternalLinks(True)
    # meraki_img.l label.connect(open_new("https://meraki.cisco.com/products/wireless#mr-new")
    # mx-new: https://meraki.cisco.com/products/appliance#mx-new
    # sm-new: https://meraki.cisco.com/products/systems-manager#sm-new

    # Copying style from Dashboard Login (https://account.meraki.com/login/dashboard_login)
    heading_style = "font-family: verdana, sans-serif; font-style: normal; " \
                    "font-size: 28px; font-weight: 300; color:  #606060;"
    label_style = "font-family: verdana, sans-serif; font-style: normal; " \
                  "font-size: 13px; color: #606060;"
    # Get back to login button style when you can change the color when it's clicked
    # login_btn_style = "border-radius: 2px; color: #fff; background: #7ac043"
    link_style = "font-family: verdana, sans-serif; font-style: normal; font-size: 13px; color: #1795E6;"

    heading = QLabel("Dashboard Login")
    heading.setStyleSheet(heading_style)
    username_lbl = QLabel("Email")
    username_lbl.setStyleSheet(label_style)
    password_lbl = QLabel("Password")
    password_lbl.setStyleSheet(label_style)
    username_field = QLineEdit()
    password_field = QLineEdit()
    # Set up username and password so these vars have values
    username = ''
    password = ''

    # Masks password as a series of dots instead of characters
    password_field.setEchoMode(QLineEdit.Password)
    login_btn = QPushButton("Log in")

    # login_btn.setStyleSheet(login_btn_style)
    forgot_password_lbl = QLabel("<a href=\"https://account.meraki.com/login/reset_password\" "
                                 "style=\"color:#1795E6;text-decoration:none\">I forgot my password</a>")
    forgot_password_lbl.setStyleSheet(link_style)
    forgot_password_lbl.setOpenExternalLinks(True)
    create_account_lbl = QLabel("<a href=\"https://account.meraki.com/login/signup\" "
                                "style=\"color:#1795E6;text-decoration:none\">Create an account</a>")
    create_account_lbl.setStyleSheet(link_style)
    create_account_lbl.setOpenExternalLinks(True)
    about_lbl = QLabel("<a href=\"https://github.com/pocc/meraki-client-vpn\" "
                       "style=\"color:#1795E6;text-decoration:none\">About</a>")
    about_lbl.setStyleSheet(link_style)
    about_lbl.setOpenExternalLinks(True)

    # --- former init_ui boundary

    layout_login_options = QHBoxLayout()
    layout_login_options.addWidget(forgot_password_lbl)
    layout_login_options.addStretch()
    layout_login_options.addWidget(create_account_lbl)

    # Create a widget to contain the login layout. This allows us to paint the background of the widget
    login_widget = QWidget()
    login_widget.setStyleSheet("background-color:white")
    # Create labels and textboxes to form a login layout
    layout_login = QVBoxLayout(login_widget)
    layout_login.addWidget(heading)
    layout_login.addWidget(username_lbl)
    layout_login.addWidget(username_field)
    layout_login.addWidget(password_lbl)
    layout_login.addWidget(password_field)
    layout_login.addWidget(login_btn)
    layout_login.addLayout(layout_login_options)
    layout_login.addStretch()
    layout_login.addWidget(about_lbl)

    meraki_img.setPixmap(QPixmap(resource_path('src/media/new-mr.jpg')))

    # Background for program will be #Meraki green = #78be20
    login_widget.setStyleSheet("background-color:#eee")
    layout_main = QHBoxLayout()
    layout_main.addWidget(login_widget)
    layout_main.addWidget(meraki_img)
    login_widget.setLayout(layout_main)
    login_widget.setWindowTitle('Meraki Client VPN')

    # Test connection with a virtual browser
    login_btn.clicked.connect(init_browser)

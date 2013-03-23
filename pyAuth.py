# -*- coding: utf-8 -*-
import sys

__author__ = 'Alex Ivanenko'

from user import User
from core import Core
from PySide.QtGui import QMainWindow, QApplication, QMessageBox, QDialog, QGridLayout, QLabel, QLineEdit, QDialogButtonBox
from PySide.QtCore import Qt


class PyAuth(QMainWindow):
    """Main window class."""
    def __init__(self):
        super(PyAuth, self).__init__()
        self.setGeometry(500, 300, 200, 100)
        self.setFixedSize(500, 300)

        # self._setup_menu()

        self.app = Core()
        self.requestCredentials()

    def requestCredentials(self):
        """Form for credentials input"""
        dialog = None

        def ok_handler(username, password):
            status = self.app.logIn(username, password)
            {
                Core.ERROR_INCORRECT_CREDENTIALS: lambda:
                QMessageBox.critical(dialog, "Error", "Incorrect username or password", modal=True),
                Core.ERROR_USER_IS_BLOCKED: lambda:
                QMessageBox.critical(dialog, "Error", "Your account is blocked", modal=True),
                Core.SUCCESS: lambda: (
                    self.show_admin_widget() if self.app.current_user.admin else self.show_customer_widget(),
                    dialog.close()
                )
            }[status]()

        def cancel_handler():
            sys.exit()

        dialog = SignInDialog(self, ok_handler, cancel_handler)
        dialog.show()


class SignInDialog(QDialog):
    def __init__(self, window, ok_handler, cancel_handler):
        super(SignInDialog, self).__init__(window)

        self.setWindowTitle("Sign in")
        self.setFixedSize(300, 130)
        self.setModal(True)

        self.layout = QGridLayout(self)

        self.username_label = QLabel(self)
        self.username_label.setText("Username")
        self.edit_username = QLineEdit(self)

        self.password_label = QLabel(self)
        self.password_label.setText("Password")
        self.edit_password = QLineEdit(self)
        self.edit_password.setEchoMode(QLineEdit.Password)

        self.buttons = QDialogButtonBox(self)
        self.buttons.addButton(QDialogButtonBox.Ok)
        self.buttons.addButton(QDialogButtonBox.Cancel)
        self.buttons.button(QDialogButtonBox.Ok).setText("Sign in")
        self.buttons.button(QDialogButtonBox.Cancel).setText("Cancel")
        self.buttons.button(QDialogButtonBox.Cancel).clicked.connect(cancel_handler)

        self.buttons.button(QDialogButtonBox.Ok).clicked.connect(
            lambda: ok_handler(self.edit_username.text(), self.edit_password.text()))

        self.layout.addWidget(self.username_label, 0, 0)
        self.layout.addWidget(self.edit_username, 0, 1)
        self.layout.addWidget(self.password_label, 1, 0)
        self.layout.addWidget(self.edit_password, 1, 1)
        self.layout.addWidget(self.buttons, 3, 0, 1, 2, Qt.AlignCenter)

        self.setLayout(self.layout)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    pyAuth = PyAuth()
    sys.exit(app.exec_())
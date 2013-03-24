# -*- coding: utf-8 -*-

__author__ = 'Alex Ivanenko'

import sys
from user import User
from core import Core
from PySide.QtGui import QMainWindow, QApplication, QMessageBox, QDialog, QGridLayout, QLabel, QLineEdit, \
    QDialogButtonBox, QAction, QWidget, QTableWidget, QAbstractItemView, QTableWidgetItem, QCheckBox, QPushButton
from PySide.QtCore import Qt


class PyAuth(QMainWindow):
    """Main window class."""

    def __init__(self):
        super(PyAuth, self).__init__()
        self.setGeometry(500, 300, 200, 100)
        self.setFixedSize(500, 300)

        self.__setupMenu()

        self.app = Core()
        self.requestCredentials()

    def __setupMenu(self):
        """Defines basic top menu"""
        quit_action = QAction("&Exit", self)
        quit_action.setShortcut('Ctrl+Q')
        quit_action.triggered.connect(self.close)

        sign_out_action = QAction("Sign out", self)
        sign_out_action.setShortcut('Ctrl+L')
        sign_out_action.triggered.connect(lambda: (self.app.logOut(), self.hide(), self.requestCredentials()))

        change_password_action = QAction("Change password", self)
        change_password_action.triggered.connect(self.requestPasswordChange)

        about_action = QAction("About", self)
        about_action.triggered.connect(lambda: QMessageBox.about(self, "About", u'© ' + __author__ + ' 2013'))

        self.file_menu = self.menuBar().addMenu("&File")
        self.file_menu.addAction(quit_action)

        self.account_menu = self.menuBar().addMenu("&Account")
        self.account_menu.addAction(sign_out_action)
        self.account_menu.addAction(change_password_action)

        self.help_menu = self.menuBar().addMenu("&Help")
        self.help_menu.addAction(about_action)

    def requestPasswordChange(self):
        """Requests dialog for password change."""
        dialog = None

        def ok_handler(oldPassword, password, confirm):
            if 5 > len(password) > 30:
                QMessageBox.critical(dialog, "Error", "Password must be between 6 and 30 char length")
                return
            if password != confirm:
                QMessageBox.critical(dialog, "Error", "Passwords don't match")
                return
            status = self.app.changePassword(oldPassword, password)
            {
                Core.ERROR_OLD_PASSWORD: lambda:
                QMessageBox.critical(dialog, "Error", "Wrong old password.", modal=True),
                Core.ERROR_PASSWORD_RESTRICTION: lambda:
                QMessageBox.critical(dialog, "Error", "Password is too weak.", modal=True),
                Core.SUCCESS: lambda: dialog.close()
            }[status]()

        def cancel_handler():
            dialog.close()

        dialog = ChangePasswordDialog(self, ok_handler, cancel_handler)
        dialog.show()

    def requestCredentials(self):
        """Requests form for credentials input"""
        dialog = None

        def ok_handler(username, password):
            status = self.app.logIn(username, password)
            {
                Core.ERROR_INCORRECT_CREDENTIALS: lambda:
                QMessageBox.critical(dialog, "Error", "Incorrect username or password", modal=True),
                Core.ERROR_USER_IS_BLOCKED: lambda:
                QMessageBox.critical(dialog, "Error", "Your account is blocked", modal=True),
                Core.ERROR_ATTEMPTS: self.close,
                Core.SUCCESS: lambda: (
                    self.showAdminWidget() if self.app.currentUser.admin else self.showCustomerWidget(),
                    dialog.close()
                )
            }[status]()

        def cancel_handler():
            sys.exit()

        dialog = SignInDialog(self, ok_handler, cancel_handler)
        dialog.show()

    def showAdminWidget(self):
        """Requests admin panel."""
        self.setCentralWidget(AdminWidget(self))
        self.show()

    def showCustomerWidget(self):
        """Requests customers panel."""
        self.setCentralWidget(CustomerWidget(self))
        self.show()


class SignInDialog(QDialog):
    """Represents sign in dialog window"""
    def __init__(self, window, ok_handler, cancel_handler):
        super(SignInDialog, self).__init__(window)

        self.setWindowTitle("Login")
        self.setFixedSize(300, 130)
        self.setModal(True)

        self.layout = QGridLayout(self)

        self.username_label = QLabel(self)
        self.username_label.setText("Username:")
        self.edit_username = QLineEdit(self)

        self.password_label = QLabel(self)
        self.password_label.setText("Password:")
        self.edit_password = QLineEdit(self)
        self.edit_password.setEchoMode(QLineEdit.Password)

        self.buttons = QDialogButtonBox(self)
        self.buttons.addButton(QDialogButtonBox.Ok)
        self.buttons.addButton(QDialogButtonBox.Cancel)
        self.buttons.button(QDialogButtonBox.Ok).setText("Login")
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


class ChangePasswordDialog(QDialog):
    """Represents change password dialog window"""
    def __init__(self, window, ok_handler, cancel_handler):
        super(ChangePasswordDialog, self).__init__(window)
        self.setWindowTitle("Change password")
        self.setFixedSize(300, 160)
        self.setModal(True)

        self.layout = QGridLayout(self)

        self.old_password_label = QLabel(self)
        self.old_password_label.setText("Old password")
        self.edit_old_password = QLineEdit(self)
        self.edit_old_password.setEchoMode(QLineEdit.Password)

        self.password_label = QLabel(self)
        self.password_label.setText("New password")
        self.edit_password = QLineEdit(self)
        self.edit_password.setEchoMode(QLineEdit.Password)

        self.confirm_label = QLabel(self)
        self.confirm_label.setText("Confirm password")
        self.edit_confirm = QLineEdit(self)
        self.edit_confirm.setEchoMode(QLineEdit.Password)

        self.buttons = QDialogButtonBox(self)
        self.buttons.addButton(QDialogButtonBox.Ok)
        self.buttons.addButton(QDialogButtonBox.Cancel)
        self.buttons.button(QDialogButtonBox.Ok).setText("Change")
        self.buttons.button(QDialogButtonBox.Cancel).setText("Cancel")
        self.buttons.button(QDialogButtonBox.Cancel).clicked.connect(cancel_handler)

        self.buttons.button(QDialogButtonBox.Ok).clicked.connect(
            lambda: ok_handler(self.edit_old_password.text(), self.edit_password.text(), self.edit_confirm.text()))

        self.layout.addWidget(self.old_password_label, 0, 0)
        self.layout.addWidget(self.edit_old_password, 0, 1)
        self.layout.addWidget(self.password_label, 1, 0)
        self.layout.addWidget(self.edit_password, 1, 1)
        self.layout.addWidget(self.confirm_label, 2, 0)
        self.layout.addWidget(self.edit_confirm, 2, 1)
        self.layout.addWidget(self.buttons, 3, 0, 1, 2, Qt.AlignCenter)

        self.setLayout(self.layout)


class AdminWidget(QWidget):
    """Represents admin panel"""
    def __init__(self, window):
        super(AdminWidget, self).__init__(window)

        self.parentWidget().setWindowTitle("Administartor panel")
        self.__setupMenu()

        self.layout = QGridLayout(self)

        self.user_table = QTableWidget(self)
        self.user_table.setColumnCount(3)
        self.user_table.setHorizontalHeaderLabels(["Username", "Blocked", "Password restriction"])
        self.user_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.user_table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.user_table.setColumnWidth(0, 210)
        self.user_table.setColumnWidth(2, 170)
        self.user_table.verticalHeader().hide()

        changePasswordBtn = QPushButton("Change Password")
        changePasswordBtn.clicked.connect(window.requestPasswordChange)
        createUserBtn = QPushButton("Add User")
        createUserBtn.clicked.connect(self._request_new_account)
        logOutBtn = QPushButton("Logout")
        logOutBtn.clicked.connect(lambda: (window.app.logOut(), window.hide(), window.requestCredentials()))

        self.layout.addWidget(self.user_table, 0, 0, 1, 0)
        self.layout.addWidget(changePasswordBtn, 1, 0)
        self.layout.addWidget(createUserBtn, 1, 1)
        self.layout.addWidget(logOutBtn, 1, 2)
        self.setLayout(self.layout)

        self.__loadUsers()

    def __loadUsers(self):
        """Loads user's data from DB"""
        users = self.parentWidget().app.getUsers()
        self.user_table.clearContents()
        self.user_table.setRowCount(len(users))
        for i in range(len(users)):
            username_item = QTableWidgetItem(users[i].username)
            username_item.setFlags(username_item.flags() ^ Qt.ItemIsEditable)

            blocked_checkbox = QCheckBox()
            if users[i].blocked:
                blocked_checkbox.setChecked(True)

            def create_blocked_toggle(checkbox, user):
                def blocked_toggle():
                    user.blocked = (1 if checkbox.isChecked() else 0)
                    self.parentWidget().app.updateUser(user)
                    self.__loadUsers()
                return blocked_toggle
            blocked_checkbox.toggled.connect(create_blocked_toggle(blocked_checkbox, users[i]))

            password_restrict_checkbox = QCheckBox()
            if users[i].restrictions:
                password_restrict_checkbox.setChecked(True)

            def create_password_restrict_toggle(checkbox, user):
                def password_restrict_toggle():
                    user.restrictions = (1 if checkbox.isChecked() else 0)
                    self.parentWidget().app.updateUser(user)
                    self.__loadUsers()
                return password_restrict_toggle
            password_restrict_checkbox.toggled.connect(
                create_password_restrict_toggle(password_restrict_checkbox, users[i]))

            self.user_table.setItem(i, 0, username_item)
            self.user_table.setCellWidget(i, 1, blocked_checkbox)
            self.user_table.setCellWidget(i, 2, password_restrict_checkbox)

    def __setupMenu(self):
        add_account_action = QAction("Add account", self)
        add_account_action.triggered.connect(self._request_new_account)
        self.parentWidget().account_menu.addAction(add_account_action)

    def _request_new_account(self):
        dialog = None

        def ok_handler(username):
            if not 3 <= len(username) <= 20:
                QMessageBox.critical(dialog, "Error", "Username's length must be between 3 and 20", modal=True)
                return
            user = User(username=username)
            status = self.parentWidget().app.addUser(user)
            {
                Core.ERROR_USER_EXISTS: lambda:
                QMessageBox.critical(dialog, "Error", "Username already exists", modal=True),
                Core.SUCCESS: lambda: (
                    self.__loadUsers(),
                    dialog.close()
                )
            }[status]()

        def cancel_handler():
            dialog.close()

        dialog = AdminWidget.AddAccountDialog(self, ok_handler, cancel_handler)
        dialog.show()

    class AddAccountDialog(QDialog):
        def __init__(self, parent, ok_handler, cancel_handler):
            super(AdminWidget.AddAccountDialog, self).__init__(parent)

            self.setWindowTitle("Add account")
            self.setFixedSize(300, 100)
            self.setModal(True)

            self.layout = QGridLayout(self)

            self.username_label = QLabel(self)
            self.username_label.setText("Username")
            self.edit_username = QLineEdit(self)

            self.buttons = QDialogButtonBox(self)
            self.buttons.addButton(QDialogButtonBox.Ok)
            self.buttons.addButton(QDialogButtonBox.Cancel)
            self.buttons.button(QDialogButtonBox.Ok).setText("Add")
            self.buttons.button(QDialogButtonBox.Cancel).setText("Cancel")
            self.buttons.button(QDialogButtonBox.Cancel).clicked.connect(cancel_handler)
            self.buttons.button(QDialogButtonBox.Ok).clicked.connect(lambda: ok_handler(self.edit_username.text()))

            self.layout.addWidget(self.username_label, 0, 0)
            self.layout.addWidget(self.edit_username, 0, 1)
            self.layout.addWidget(self.buttons, 1, 0, 1, 2, Qt.AlignCenter)

            self.setLayout(self.layout)


class CustomerWidget(QWidget):
    def __init__(self, window):
        super(CustomerWidget, self).__init__(window)
        self.parentWidget().setWindowTitle("Customer panel")

        self.layout = QGridLayout(self)

        helloString = "Hello " + window.app.currentUser.username + "!\n"
        helloString += "Now you can change your password or log out"
        label = QLabel(helloString)
        changePasswordBtn = QPushButton("Change Password")
        changePasswordBtn.clicked.connect(window.requestPasswordChange)
        logOutBtn = QPushButton("Logout")
        logOutBtn.clicked.connect(lambda: (window.app.logOut(), window.hide(), window.requestCredentials()))
        self.layout.addWidget(label, 0, 0, 1, 0, Qt.AlignCenter)
        self.layout.addWidget(changePasswordBtn, 1, 0)
        self.layout.addWidget(logOutBtn, 1, 1)

        self.setLayout(self.layout)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    pyAuth = PyAuth()
    sys.exit(app.exec_())
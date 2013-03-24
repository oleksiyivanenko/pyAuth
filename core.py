# -*- coding: utf-8 -*-
__author__ = 'Alex Ivanenko'

import string
import random
import re
import os
import sqlite3
from hashlib import sha1
from PySide.QtCore import QObject
from user import User


class Core(QObject):
    """Default class for GUI app creation"""
    SUCCESS = 0
    ERROR_INCORRECT_CREDENTIALS = 1
    ERROR_USER_IS_BLOCKED = 2
    ERROR_PASSWORD_RESTRICTION = 3
    ERROR_USER_EXISTS = 4
    ERROR_OLD_PASSWORD = 5
    ERROR_ATTEMPTS = 6

    __attempts = 0

    __dbName = "passApp.db"

    def __init__(self):
        super(Core, self).__init__()
        db_exists = os.path.exists(self.__dbName)
        self.connection = sqlite3.connect(self.__dbName)
        if not db_exists:
            self.__createDb()

    def __del__(self):
        self.connection.close()

    def __createDb(self):
        """Create table in db"""
        cursor = self.connection.cursor()
        cursor.execute("""CREATE TABLE Users(user_id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT UNIQUE NOT NULL,
        password TEXT, salt TEXT, blocked INTEGER NOT NULL, restrictions INTEGER NOT NULL, admin INTEGER NOT NULL)""")
        cursor.close()
        self.connection.commit()
        user = User(username="admin", admin=1)
        self.addUser(user)

    def getUser(self, user_id=None, username=None):
        """Get one user from db by user_id or username."""
        cursor = self.connection.cursor()
        if user_id:
            row = cursor.execute("""SELECT * FROM Users WHERE user_id = ?""", [user_id]).fetchone()
        elif username:
            row = cursor.execute("""SELECT * FROM Users WHERE username = ?""", [username]).fetchone()
        else:
            return
        if not row:
            return None
        user = User(row[0], row[1], row[2], row[3], row[4], row[5], row[6])
        cursor.close()
        return user

    def updateUser(self, user):
        """Update user."""
        cursor = self.connection.cursor()
        cursor.execute("""UPDATE Users SET username = ?, password = ?, salt = ?, blocked = ?,
        restrictions = ?, admin = ? WHERE user_id = ?""",
                       [user.username, user.password, user.salt, user.blocked, user.restrictions,
                        user.admin, user.user_id])
        cursor.close()
        self.connection.commit()

    def addUser(self, user):
        """Add user to db."""
        if self.getUser(username=user.username):
            return self.ERROR_USER_EXISTS
        if user.restrictions and not self.verifyPassword(user.password):
            return self.ERROR_PASSWORD_RESTRICTION

        cursor = self.connection.cursor()
        salt = self.__generateSalt()
        cursor.execute("""INSERT INTO Users(user_id, username, password, salt, blocked, restrictions, admin)
        VALUES(?,?,?,?,?,?,?)""", [user.user_id, user.username, user.password, salt, user.blocked,
                                   user.restrictions, user.admin])
        user = self.getUser(username=user.username)
        user.password = self.__hashPassword(user.user_id, user.password, user.salt)
        self.updateUser(user)
        cursor.close()
        self.connection.commit()

        return self.SUCCESS

    def getUsers(self):
        users = []
        cursor = self.connection.cursor()
        rows = cursor.execute("SELECT * FROM Users ORDER BY username")
        for row in rows:
            users.append(User(row[0], row[1], row[2], row[3], row[4], row[5], row[6]))
        cursor.close()
        return users

    def __generateSalt(self):
        """Generate salt for password hashing"""
        saltAlphabet = string.ascii_letters + string.digits + string.punctuation
        salt = ""
        for i in range(0, 10):
            salt += saltAlphabet[random.randint(0, len(saltAlphabet) - 1)]
        return salt

    def logIn(self, username, password):
        """Log in into system."""
        user = self.getUser(username=username)
        if self.__attempts > 2:
            return self.ERROR_ATTEMPTS
        if (not user) or (self.__hashPassword(user.user_id, password, user.salt) != user.password):
            self.__attempts += 1
            return self.ERROR_INCORRECT_CREDENTIALS
        if user.blocked:
            return self.ERROR_USER_IS_BLOCKED

        self.currentUser = user
        return self.SUCCESS

    def logOut(self):
        """Log out from system."""
        self.currentUser = None

    def changePassword(self, oldPassword, newPassword):
        """Change users password"""
        user = self.currentUser
        if not user or user.password != self.__hashPassword(user.user_id, oldPassword, user.salt):
            return self.ERROR_OLD_PASSWORD
        if user.restrictions and not self.verifyPassword(newPassword):
            return self.ERROR_PASSWORD_RESTRICTION
        user.password = self.__hashPassword(user.user_id, newPassword, user.salt)
        self.updateUser(user)
        return self.SUCCESS

    def __hashPassword(self, userId, password, salt):
        """Returns hashed password"""
        return sha1(str(userId) + sha1(password + salt).hexdigest()).hexdigest()

    def verifyPassword(self, password):
        """Verify password strength.
        In password must be upper letters, lower letters and digits.
        Password length must be at least 6 characters
        """
        if (re.match(r'[A-Za-z0-9@#$%^&+=_]{6,}', password)
            and re.search(r'[A-Z]', password)
            and re.search(r'[a-z]', password)
            and re.search(r'\d', password)):
            return True
        return False

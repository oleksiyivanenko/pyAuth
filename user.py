# -*- coding: utf-8 -*-


class User():
    """
    User model
    """
    def __init__(self, user_id=None, username=None, password=u'', salt=None, blocked=0, restrictions=0, admin=0):
        self.user_id = user_id
        self.username = username
        self.password = password
        self.blocked = blocked
        self.restrictions = restrictions
        self.admin = admin
        self.salt = salt

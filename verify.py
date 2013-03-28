# -*- coding: utf-8 -*-
__author__ = 'Alex Ivanenko'

import os
import ctypes
from win32api import GetSystemMetrics
from hashlib import md5
from _winreg import *


params = []

currentFolder = os.getcwd()
diskSpace = ctypes.c_ulonglong(0)
ctypes.windll.kernel32.GetDiskFreeSpaceExW(ctypes.c_wchar_p(currentFolder), None, ctypes.pointer(diskSpace), None)
params.append(os.environ.get("USERNAME"))
params.append(os.environ['COMPUTERNAME'])
params.append(os.environ['WINDIR'])
params.append(os.environ['WINDIR'] + "\\system32")
params.append(str(GetSystemMetrics(1)))
params.append(str(diskSpace.value))
params.append(str(GetSystemMetrics(43)))


def __getHash():
    hashedString = "".join(params)
    return md5(hashedString.encode("utf-8")).hexdigest().upper()


def __readRegistred():
    aReg = ConnectRegistry(None, HKEY_CURRENT_USER)
    aKey = OpenKey(aReg, r"Software\o_ivanenko")
    try:
        val = QueryValueEx(aKey, "Signature")
        return val[0]
    except EnvironmentError:
        return


def verify():
    if __getHash() == __readRegistred():
        return True
    return False

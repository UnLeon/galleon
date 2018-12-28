# -*- cording:utf-8 -*-
import os
import time
import shutil
copyFileCounts = 0


def whatype(value):        # 判断输入类型
    if not str:
        print("Type is Null")
        return "Null"
    else:
        if isinstance(value, int):
            print("Type is int")
            return "int"
        if isinstance(value, list):
            print("Type is list")
            return "list"
        if isinstance(value, tuple):
            print("Type is tuple")
            return "tuple"
        if isinstance(value, dict):
            print("Type is dict")
            return "dict"
        if isinstance(value, str):
            if value.strip() == "":
                print("Type is Null")
                return "Null"
            else:
                print("Type is str")
                return "str"


def test1():
    pass


class AutoBackup(object):

    def __init__(self, path, target):
        self.sourceDir = path
        self.targetDir = target
        self.copyFile()

    def copyFile(self):
        global copyFileCounts
        for f in os.listdir(self.sourceDir):
            sourceF = os.path.join(self.sourceDir, f)
            targetF = os.path.join(self.targetDir, f)
            if os.path.isfile(sourceF):
                if not os.path.exists(self.targetDir):  # 创建目标文件夹
                    os.makedirs(self.targetDir)
                if os.path.exists(targetF) and (os.path.getmtime(targetF) >= os.path.getmtime(sourceF)):
                    # print("%s %s 已为最新" % (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), targetF))
                    pass
                else:
                    # open(targetF, "wb").write(open(sourceF, "rb").read())   # 写入2进制文件
                    shutil.copy(sourceF, targetF)
                    print("%s %s 已备份 *" % (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), sourceF))
                    copyFileCounts += 1
            elif os.path.isdir(sourceF):
                AutoBackup(sourceF, targetF)
        # print("%s 当前处理文件夹%s已备份%s 个文件" % (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), self.sourceDir, copyFileCounts))


if __name__ == "__main__":
    print(__name__)
    a = dict()
    print("a is", whatype(a))
    # AutoBackup("H:\Learn\Project\py_project\Toel", "H:\Learn\Project\py_project\Toel_backup")
    try:
        AutoBackup("H:\Learn\Project", "G:\Projects")
    except Exception:
        try:
            AutoBackup("I:\Learn\Project", "D:\Projects")
        except Exception:
            pass

# -*- coding: utf-8 -*-
#
# 字符串工具类

def isNull(str):
    print(str)
    if str==None or len(str)==0 or str=='':
        return True;
    return False;


def isNotNull(str):
    if str==None or str=='' or len(str)==0 :
        return False;
    return True;
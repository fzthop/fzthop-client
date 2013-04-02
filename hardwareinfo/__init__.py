# coding=utf-8
"""

"""
__author__  = 'Shine tong<linuxtong@gmail.com>'
__version__ = '0.1.0'
__date__    = '2013-03-29'
__all__     = [ 'totalInfo','blosInfo','systemInfo','cacheInfo',
                'cpuInfo','memoryInfo','netCardinfo','newInfo']

from hardwareinfo import dmidecode,kudzu
import os

def blosInfo():
    return  dmidecode.blosInfo()

def systemInfo():
    return dmidecode.systemInfo()

def cacheInfo():
    return dmidecode.cacheInfo()

def cpuInfo():
    return dmidecode.cpuInfo()

def memoryInfo():
    return dmidecode.memoryInfo()

def netCardinfo():
    return kudzu.networkCard()

def totalInfo():
    project = ['blos','system','cache','cpu','mem','net']
    info = [blosInfo(),systemInfo(),cacheInfo(),cpuInfo(),memoryInfo(),netCardinfo()]
    totalInfo = dict(zip(project,info))
    return totalInfo

def newInfo(path='/tmp',cachename='hardware.info'):
    if not os.path.exists(path):
        os.makedirs(path,0755)
    info = totalInfo()
    filename  = path + os.sep + cachename
    try:
        cache = open(filename, 'r' ).read()
    except IOError:
        cache = ""
    if str(info) != str(cache):
        try:
            fileHandle = open(filename,'w+')
            fileHandle.write(str(info))
        finally:
            fileHandle.close()
        return info
    else:
        return None
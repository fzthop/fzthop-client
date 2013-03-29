# coding=utf-8
"""

"""
__author__  = 'Shine tong<linuxtong@gmail.com>'
__version__ = '0.1.0'
__date__    = '2013-03-29'
__all__     = [ 'blosInfo','systemInfo','cacheInfo','cpuInfo','memoryInfo','netCardinfo']

from hardwareinfo import dmidecode,kudzu

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
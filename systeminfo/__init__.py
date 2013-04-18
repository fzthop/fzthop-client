# coding=utf-8
"""

"""

__author__  = 'Shine tong<linuxtong@gmail.com>'
__version__  = "0.1.0"
__date__     = "2013-04-08"
__all__      = ['cpu','physicalMem','buffersMem','swapMem','partition','uptime',
                'process','netCard','iostat','total']

from systeminfo import top,free,net,df,io
from ipaddress import ipaddress
import sys

def init():
    """
    重新初始化类，获取新信息
    如未初始化，获取的信息是上一次初始化的信息
    """
    top.__init__()
    free.__init__()
    net.__init__()
    df.__init__()
    io.__init__()

def cpu():
    cpu = top.cpuLoad()
    if cpu is None:
        sys.stderr.writelines("Cpu info is None\n")
    return cpu

def physicalMem():
    mem = free.physicalMem()
    if mem is None:
        sys.stderr.writelines("Physical mem info is None\n")
    return mem

def buffersMem():
    mem = free.bufferslMem()
    if mem is None:
        sys.stderr.writelines("Buffers mem info is None\n")
    return mem

def swapMem():
    mem = free.swapMem()
    if mem is None:
        sys.stderr.writelines("Swap mem info is None\n")
    return mem

def partition():
    partition =  df.detail()
    if partition is None:
        sys.stderr.writelines("Partition info is None\n")
    return partition

def uptime():
    load =  top.uptime()
    if load is None:
        sys.stderr.writelines("Uptime info is None\n")
    return load

def process():
    process =  top.processStatus()
    if process is None:
        sys.stderr.writelines("Process info is None\n")
    return process

def netCard():
    netCard = net.detail()
    if netCard is None:
        sys.stderr.writelines("NetCard info is None\n")
    return netCard

def iostat():
    iostat = io.detail()
    if iostat is None:
        sys.stderr.writelines("Io info is None\n")
    return iostat

def maxInetipadd():
    result = []
    try:
        cardInfo = net.detail()
        for card in cardInfo.keys():
            netInfo = cardInfo[card]
            ip = netInfo['ipadd']
            if ip is not None:
                result.append(ip)
    except Exception,error:
        sys.stderr.writelines("To obtain net card ip address error,code:%s\n" %error)
    if result:
        return  ipaddress.maxInetip(result)
    else:
        return None

def total():
    """
    """
    project = ['cpu','physicalMem','buffersMem','swapMem','partition','uptime',
               'process','netCard','io']
    info = [cpu(),physicalMem(),buffersMem(),swapMem(),partition(),uptime(),process(),netCard(),iostat()]
    totalInfo = dict(zip(project,info))
    return totalInfo
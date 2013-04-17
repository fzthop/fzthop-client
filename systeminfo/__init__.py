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
    return top.cpuLoad()

def physicalMem():
    return free.physicalMem()

def buffersMem():
    return free.bufferslMem()

def swapMem():
    return free.swapMem()

def partition():
    return df.detail()

def uptime():
    return top.uptime()

def process():
    return top.processStatus()

def netCard():
    return net.detail()

def iostat():
    return io.detail()

def maxInetipadd():
    result = []
    cardInfo = net.detail()
    for card in cardInfo.keys():
        netInfo = cardInfo[card]
        ip = netInfo['ipadd']
        if ip is not None:
            result.append(ip)
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
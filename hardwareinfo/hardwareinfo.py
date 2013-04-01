# coding=utf-8
"""
获取服务器硬件信息

"""

import subprocess
import re

class Dmidecode():
    """
    获取板载信息
    """
    def __init__(self):
        dmidecodeCmd = "/usr/sbin/dmidecode"
        #if os.path.isfile(dmidecodeCmd):
        subp   = subprocess.Popen(dmidecodeCmd, shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        dmidecodeInfo= subp.stdout.read()
        if subp.poll() == 0:
            dmidecodeInfo = dmidecodeInfo.split("\n\n")
        else:
            dmidecodeInfo = []
#        #test--code
#        dmidecodeInfo = open(r"dmidecode.info").read()
#        dmidecodeInfo = dmidecodeInfo.split("\n\n")
#        #test--code
        self.dmidecodeInfo = dmidecodeInfo

    def blosInfo(self):
        dmidecodeInfo = self.dmidecodeInfo
        findAll = re.compile(r"""vendor:([^\n]+)\n            #制造商信息
                                 .*version:([^\n]+)\n          #BLOS版本
                                 .*release\s+date:([^\n]+)\n   #生产日期
                                 #.*address:([^\n]+)\n         #blos地址
                                 """,re.I|re.X|re.S)
        result = {}
        project = ['vendor','version','releaseDate']
        for ls in dmidecodeInfo:
            #print ls
            if ls.find("BIOS Information") > 0:
                try:
                    blosInfo = findAll.findall(ls)[0]
                    blosInfo = [x.strip() for x in blosInfo]
                    result =  dict(zip(project,blosInfo))
                except (ValueError,IndexError),error:
                    pass
        if result:
            return  result
        else:
            return None
    def systemInfo(self):
        dmidecodeInfo = self.dmidecodeInfo
        findAll = re.compile(r"""manufacturer:([^\n]+)\n     #制造商信息
                                 .*product\s+name:([^\n]+)\n  #产品信息（服务器版本，比如dell R710 R10等）
                                 .*version:([^\n]+)\n         #版本
                                 .*serial\s+number:([^\n]+)\n #序列号，保修用
                                 .*uuid:([^\n]+)\n            #主板ID
                                 """,re.I|re.X|re.S)
        result = {}
        project = ['manufacturer','name','version','serialNumber','uuid']
        for ls in dmidecodeInfo:
            #print ls
            if ls.find("System Information") > 0:
                try:
                    systemInfo = findAll.findall(ls)[0]
                    systemInfo = [x.strip() for x in systemInfo]
                    result =  dict(zip(project,systemInfo))
                except (ValueError,IndexError),error:
                    pass
        if result:
            return  result
        else:
            return None
    def cacheInfo(self):
        dmidecodeInfo = self.dmidecodeInfo
        findAll = re.compile(r"""type:([^\n]+)\n        #内存类型
                                 .*capacity:([^\n]+)\n   #最大支持内存
                                 .*devices:([^\n]+)      #内存插槽数
                                 """,re.I|re.X|re.S)
        result = {}
        project = ['type','capacity','devices']
        for ls in dmidecodeInfo:
            #print ls
            if ls.find("Physical Memory Array") > 0:
                try:
                    cache = findAll.findall(ls)[0]
                    cache =  [x.strip() for x in cache]
                    result= dict(zip(project,cache))
                except (ValueError,IndexError),error:
                    pass
        if result:
            return  result
        else:
            return None
    def cpuInfo(self):
        dmidecodeInfo = self.dmidecodeInfo
        findAll = re.compile(r"""designation:([^\n]+)\n             #CPU插槽位置
                                  .*id:([^\n]+)\n                    #CPU ID
                                  .*version:([^\n]+)\n               #CPU型号
                                  .*voltage:([^\n]+)\n               #CPU电压
                                  .*clock:([^\n]+)\n                 #CPU外频
                                  .*max\s+speed:([^\n]+)\n           #CPU最大主频
                                  .*current\s+speed:([^\n]+)\n       #CPU当前主频
                                  .*upgrade:([^\n]+)\n               #CPU接口类型
                                  (?=.*core\s+count:([^\n]+)\n)?     #CPU核心个数
                                  (?=.*core\s+enabled:([^\n]+)\n)?   #CPU核心启用个数
                                  (?=.*thread\s+count:([^\n]+)\n)?   #CPU线程数
                                 """,re.I|re.X|re.S)
        result = {}
        project = ['designation','id','version','voltage','clock','maxSpeed',
                 'currentSpeed','upgrade','coreCount','coreEnabled','threadCount']
        for ls in dmidecodeInfo:
            if ls.find("Processor Information") > 0:
                try:
                    cpuInfo = findAll.findall(ls)[0]
                    cpuInfo = [ x.strip() for x in cpuInfo]
                    cpuInfo = dict(zip(project,cpuInfo))
                    cpuNum = cpuInfo['designation']
                    try:
                        if result[cpuNum]:
                            pass
                    except KeyError:
                        result[cpuNum] = cpuInfo
                except (ValueError,IndexError),error:
                    pass
        if result:
            return  result
        else:
            return None
    def memoryInfo(self):
        dmidecodeInfo = self.dmidecodeInfo
        findAll = re.compile(r"""size:([^\n]+)\n                #内存大小
                                  .*\tlocator:([^\n]+)\n         #内存插槽位置
                                  .*type:([^\n]+)\n              #内存类型
                                  .*speed:([^\n]+)\n             #内存时钟频率
                                  .*manufacturer:([^\n]+)\n      #制造商编码
                                  .*serial\s+number:([^\n]+)\n   #序列号
                                  .*asset\s+tag:([^\n]+)\n       #资产标签
                                  .*part\s+number:([^\n]+)\n?    #物料编码
                                  (?:.*rank:([^\n]+)\n?)?        #内存芯片镶嵌类型
                                 """,re.I|re.X|re.S)
        result = {}
        project = ['size','locator','type','speed','manufacturer','serialNumber',
                     'assetTag','partNumber','rank']
        for ls in dmidecodeInfo:
            if ls.find("Memory Device") > 0:
                try:
                    memoryInfo = findAll.findall(ls)[0]
                    #print memoryInfo
                    memoryInfo = [ x.strip() for x in memoryInfo]
                    memoryInfo = dict(zip(project,memoryInfo))
                    memoryNum  = memoryInfo['locator']
                    try:
                        if result[memoryNum]:
                            pass
                    except KeyError:
                        result[memoryNum] = memoryInfo
                except (ValueError,IndexError),error:
                    pass
        if result:
            return  result
        else:
            return None
class Kudzu():
    """
    获取网卡信息
    """
    def __init__(self):
        kudzuCmd  = "/sbin/kudzu --probe --class=network"
        subp      = subprocess.Popen(kudzuCmd, shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        kudzuInfo = subp.stdout.read()
        if subp.poll() == 0:
            kudzuInfo = kudzuInfo.split("-")
        else:
            kudzuInfo = []
#        #test--code
#        kudzuInfo = open(r"netwok.info").read()
#        kudzuInfo = kudzuInfo.split("-")
#        #test--code
        self.kudzuInfo = kudzuInfo

    def networkCard(self):
        kuzuInfo = self.kudzuInfo
        findAll = re.compile(r"""device:([^\n]+)\n      #设备编号
                                  .*driver:([^\n]+)\n    #驱动版本
                                  .*desc:([^\n]+)\n      #详情
                                  .*hwaddr:([^\n]+)\n    #MAC 地址
                              """,re.I|re.X|re.S)
        result = {}
        project = ['device','driver','desc','hwaddr']
        #print kuzuInfo
        for ls in kuzuInfo:
            if ls.find("NETWORK") > 0:
                try:
                    nCinfo = findAll.findall(ls)[0]
                    nCinfo = [ x.strip() for x in nCinfo]
                    nCinfo = dict(zip(project,nCinfo))
                    cardName = nCinfo['device']
                    try:
                        if result[cardName]:
                            pass
                    except KeyError:
                        result[cardName] = nCinfo
                except (ValueError,IndexError),error:
                    pass
        if result:
            return  result
        else:
            return None

dmidecode = Dmidecode()
kudzu     = Kudzu()
if __name__ == "__main__":
    print dmidecode.blosInfo()
    print dmidecode.systemInfo()
    print dmidecode.cacheInfo()
    print dmidecode.cpuInfo()
    print dmidecode.memoryInfo()
    print kudzu.networkCard()
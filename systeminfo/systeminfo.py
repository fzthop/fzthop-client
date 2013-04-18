# coding=utf-8
"""
获取服务器运行状态
"""

import subprocess
import re


class Top():
    """
    """
    def __init__(self):
        topCmd = "/usr/bin/top -bi -n 3 -d 2"
        subp   = subprocess.Popen(topCmd, shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        topInfo= subp.stdout.read()
        if subp.poll() == 0:
            topInfo = topInfo.split("\n\n\n")[2]
            topInfo = topInfo.split("\n")
        else:
            topInfo = []
        self.topInfo = topInfo

    def uptime(self):
        topInfo = self.topInfo
        try:
            uptimeInfo = topInfo[0]
        except IndexError:
            uptimeInfo = ""
        findAll = re.compile(r"""(\d+\s+)user             #登录用户数
                               .*average:(.*),(.*),(.*)$  #load 1分钟，5分钟，15分钟负载
                             """,re.X)
        result = {}
        project = ['user','load1','load5','load15']
        try:
            uptimeInfo = findAll.findall(uptimeInfo)[0]
            uptimeInfo = [x.strip() for x in uptimeInfo]
            result =  dict(zip(project,uptimeInfo))
        except (ValueError,IndexError):
            pass
        if result:
            return  result
        else:
            return None

    def processStatus(self):
        topInfo = self.topInfo
        try:
            processInfo = topInfo[1]
        except IndexError:
            processInfo = ""
        findAll = re.compile(r"""(\d+\s+)total       #总运行的进程
                               .*(\d+\s+)running     #正在运行的进程
                               .*(\d+\s+)sleeping    #休眠的进程
                               .*(\d+\s+)stopped     #停止的进程
                               .*(\d+\s+)zombie      #僵尸进程
                             """,re.X)
        result = {}
        project = ['total','running','sleeping','stopped','zombie']
        try:
            processInfo = findAll.findall(processInfo)[0]
            processInfo = [x.strip() for x in processInfo]
            result =  dict(zip(project,processInfo))
        except (ValueError,IndexError):
            pass
        if result:
            return  result
        else:
            return None
    def cpuLoad(self):
        topInfo = self.topInfo
        try:
            cpuInfo = topInfo[2]
        except IndexError:
            cpuInfo = ""
        findAll = re.compile(r"""\s(\d.*)%us    #用户空间占用CPU
                               .*\s(\d.*)%sy    #内核空间占用CPU
                               .*\s(\d.*)%ni    #用户空间内改变过优先级的进程占用CPU百分比
                               .*\s(\d.*)%id    #空闲CPU百分比
                               .*\s(\d.*)%wa    #等待输入输出的CPU时间百分比
                               .*\s(\d.*)%hi    #硬件中断
                               .*\s(\d.*)%si    #软件中断
                               .*\s(\d.*)%st    #实时
                             """,re.X)
        result = {}
        project = ['us','sy','ni','idle','wa','hi','si','st']
        try:
            cpuInfo = findAll.findall(cpuInfo)[0]
            cpuInfo = [x.strip() for x in cpuInfo]
            result =  dict(zip(project,cpuInfo))
        except (ValueError,IndexError):
            pass
        if result:
            return  result
        else:
            return None
class Free():
    """

    """
    def __init__(self):
        freeCmd = "/usr/bin/free"
        subp   = subprocess.Popen(freeCmd, shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        freeInfo = subp.stdout.read()
        if subp.poll() == 0:
            freeInfo = freeInfo.split("\n")
        else:
            freeInfo = []
        self.freeInfo = freeInfo

    def  physicalMem(self):
        freeInfo = self.freeInfo
        try:
            phInfo = freeInfo[1]
        except IndexError:
            phInfo = ""
        findAll = re.compile(r"""\s+(\d+)    #总物理内存
                                  \s+(\d+)   #分配的内存
                                  \s+(\d+)   #未分配的内存
                                  \s+(\d+)   #多个进程共享的内存
                                  \s+(\d+)   #磁盘缓存
                                  \s+(\d+)   #系统已分配但未被使用的cache数量
                             """,re.X)
        result = {}
        project = ['total','used','free','shard','buffers','cached']
        try:
            phInfo = findAll.findall(phInfo)[0]
            phInfo = [x.strip() for x in phInfo]
            result =  dict(zip(project,phInfo))
        except (ValueError,IndexError):
            pass
        if result:
            return  result
        else:
            return None
    def  bufferslMem(self):
            freeInfo = self.freeInfo
            try:
                buInfo = freeInfo[2]
            except IndexError:
                buInfo = ""
            findAll = re.compile(r"""\s+(\d+)    #buffers 使用的内存
                                  \s+(\d+)       #cache的内存
                             """,re.X)
            result = {}
            project = ['buffers','cache']
            try:
                buInfo = findAll.findall(buInfo)[0]
                buInfo = [x.strip() for x in buInfo]
                result =  dict(zip(project,buInfo))
            except (ValueError,IndexError):
                pass
            if result:
                return  result
            else:
                return None
    def  swapMem(self):
        freeInfo = self.freeInfo
        try:
            swapInfo = freeInfo[3]
        except IndexError:
            swapInfo = ""
        findAll = re.compile(r"""\s+(\d+)    #swap内存
                                  \s+(\d+)   #swap使用内存
                                  \s+(\d+)   #swap剩余内存
                             """,re.X)
        result = {}
        project = ['total','used','free']
        try:
            swapInfo = findAll.findall(swapInfo)[0]
            swapInfo = [x.strip() for x in swapInfo]
            result =  dict(zip(project,swapInfo))
        except (ValueError,IndexError):
            pass
        if result:
            return  result
        else:
            return None

class Netcard():
    """

    """
    def __init__(self):
        netFile = "/proc/net/dev"
        ifconfigCmd = "/sbin/ifconfig"
        try:
            netInfo = open(netFile,'r').read()
            netInfo = netInfo.replace(':',' ')
            netInfo = netInfo.split('\n')
        except IOError:
            netInfo = []
        subp   = subprocess.Popen(ifconfigCmd, shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        ifconfigInfo = subp.stdout.read()
        if subp.poll() == 0:
            ifconfigInfo = ifconfigInfo.split("\n\n")
        else:
             ifconfigInfo = []
        self.netInfo = netInfo
        self.ifconfigInfo = ifconfigInfo
    def detail(self):
        netInfo = self.netInfo
        ifconfigInfo = self.ifconfigInfo
        findAll = re.compile(r"""(\w+\d+)
                                 .*addr:(\d+.\d+.\d+.\d+)
                              """,re.I|re.X|re.S)
        try:
            netInfo = netInfo[2::]
        except IndexError:
            netInfo = ""
        result = {}
        ipadd = {}
        project = ['input','output','name','ipadd']
        for ip in ifconfigInfo:
            try:
                ipname,ip =  findAll.findall(ip)[0]
                ipadd.setdefault(ipname,[]).append(ip)
            except (ValueError,IndexError):
                pass
        for net in netInfo:
            net =  re.split('\s+',net.strip())
            if len(net) == 17:
                cardName,receiveBytes = net[0],net[1]
                transmitBytes = net[9]
                try:
                    ip = ipadd[cardName]
                    if len(str(ip)) > 15:
                        ip = ','.join(ip)
                except KeyError:
                    ip = None
                traffic = dict(zip(project,
                                (receiveBytes,transmitBytes,cardName,ip)
                                )
                             )
                try:
                    if result[cardName]:
                        pass
                except KeyError:
                    result[cardName] = traffic
        if result:
            return  result
        else:
            return None

class Df():
    """

    """
    def __init__(self):
        dfCmdsize = "/bin/df"
        dfCmdnode = "/bin/df -i"
        subpSize   = subprocess.Popen(dfCmdsize, shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        subpNode   = subprocess.Popen(dfCmdnode, shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        dfSizeinfo = subpSize.stdout.read()
        dfNodeinfo = subpNode.stdout.read()
        if subpSize.poll() == 0:
            dfSizeinfo = dfSizeinfo.replace('\n ','')
            dfSizeinfo = dfSizeinfo.replace('%','')
            dfSizeinfo = dfSizeinfo.split('\n')
        else:
            dfSizeinfo = []
        if subpNode.poll() == 0:
            dfNodeinfo = dfNodeinfo.replace('\n ','')
            dfNodeinfo = dfNodeinfo.replace('%','')
            dfNodeinfo = dfNodeinfo.split('\n')
        else:
            dfNodeinfo = []
        self.dfSizeinfo = dfSizeinfo
        self.dfNodeinfo = dfNodeinfo

    def detail(self):
        dfSizeinfo = self.dfSizeinfo
        dfNodeinfo = self.dfNodeinfo
        try:
            dfSizeinfo = dfSizeinfo[1::]
            dfNodeinfo = dfNodeinfo[1::]
        except IndexError:
            dfSizeinfo = ""
            dfNodeinfo = ""
        project = ['filesystem','size','used','availused',
                       'sizeuse','mountedon','nodeuse']
        result = {}
        for size in dfSizeinfo:
            size = re.split("\s+",size)
            key  = size[-1]
            nodeUse = None
            for node in dfNodeinfo:
                if node.find(key) > 0:
                    node =  re.split("\s+",node)
                    nodeUse = node[-2]
            size.append(nodeUse)
            info = dict(zip(project,size))
            try:
                if result[key]:
                    pass
            except KeyError:
                if key:
                    result[key] = info
        if result:
            return result
        else:
            return None

class Iostat():
    """

    """
    def __init__(self):
        iostatCmd = "/usr/bin/iostat -x"
        subp = subprocess.Popen(iostatCmd, shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        iostatInfo = subp.stdout.read()
        if subp.poll() == 0:
            iostatInfo = iostatInfo.split('\n')
        else:
            iostatInfo= []
        self.iostatInfo = iostatInfo

    def detail(self):
        """
        0        1          2       3     4        5       6        7          8        9       10      11
        Device:  rrqm/s   wrqm/s   r/s   w/s     rsec/s   wsec/s    avgrq-sz avgqu-sz   await  svctm  %util
        sda      0.03     621.37  0.13  10.79    10.58    5057.28   463.95     0.53     48.36   2.99   3.27
        """
        iostatInfo = self.iostatInfo
        try:
            iostatInfo = iostatInfo[6::]
        except IndexError:
            iostatInfo = ''
        project = ['await','rsec','wsec','util','device']
        result ={}
        for info in iostatInfo:
            info = re.split('\s+',info)
            if len(info) != 12:
                continue
            key,rsec,wsec,await,util = info[0],info[5],info[6],info[9],info[11]
            info = dict(zip(project,(await,rsec,wsec,util,key)))
            try:
                if result[key]:
                    pass
            except KeyError:
                result[key] = info
        if result:
            return result
        else:
            return None

top = Top()
free = Free()
net = Netcard()
df = Df()
io = Iostat()

def main():
    """
    单元测试
    """
    mark1 = "=/" * 20
    mark2 = "~*" * 20
    project = ['uptime','process','CpuLoad','PhysicalMem','BuffersMem','SwapMem',
               'Network','DiskInfo','IoInfo']
    p2 = ['Network','DiskInfo','IoInfo']
    info =  [top.uptime(),top.processStatus(),top.cpuLoad(),free.physicalMem(),free.bufferslMem(),
             free.swapMem(),net.detail(),df.detail(),io.detail()]
    for num,pro in enumerate(project):
        print "%s%s%s" %(mark1,pro,mark1)
        dictInfo = info[num]
        if dictInfo is not None:
            for key in dictInfo.keys():
                if pro in p2:
                    print mark2
                    dictInfo2 = dictInfo[key]
                    for key2 in dictInfo2.keys():
                        print "\t%s:%s" %(key2,dictInfo2[key2])
                else:
                    print "%s:%s" %(key,dictInfo[key])
        else:
            print "obtain error"

if __name__ == '__main__':
    main()
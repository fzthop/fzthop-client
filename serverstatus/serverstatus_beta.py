#!/usr/bin/env python
# -*- coding: utf-8 -*-
#全部从proc取数据，暂时无法保证其计算方法的正确性

__authors__  = ['ARES_HHD <ARES.HHD@gmail.com>', ]
__version__  = "0.1.1"
__date__     = "2013-3-27"
__license__  = "GPL v2.0"

import json
import time
import os
import re

def load_process_stat():

    load_dict = {}
    process_dict = {}
    with open("/proc/loadavg") as f:
        line = f.readline().split()
        load_dict['1min'] = line[0]
        load_dict['5min'] = line[1]
        load_dict['10min'] = line[2]
        process_dict['total'] = line[3].split('/')[1]
        process_dict['running'] = line[3].split('/')[0]
    with open("/proc/uptime") as f:
        con = f.readline().split()
        load_dict['uptime'] = round(float(con[0])/86400,2)

    data_keys = {
        'loadstat': load_dict,
        'processstat': process_dict
        }
    #print data_keys
    return data_keys 

def get_io_dict():

    io_dict = {}
    with open("/proc/diskstats") as f:
        for line in f.readlines(): 
            con = line.strip().split()[2:]
            if not con[0].startswith(('sd', 'c0', 'hd')):continue
            io_dict[con[0]] = map(int, con[1:])
    return io_dict

def getuptime():

    with open("/proc/uptime") as f:
        l = f.readline()
    return float(l.split()[0])

def try_div(a):
    if len(a) == 2:
        try:
            return a[0] / a[1]
        except ZeroDivisionError:
            return 0
    else:
        try:
            return a[0] / a[1] /a[2]
        except ZeroDivisionError:
            return 0

def io_stat():
    """
    columns_disk = ['rio', 'rmerge', 'rsect', 'ruse', 'wio', 'wmerge',
                    'wsect', 'wuse', 'running', 'aveq','use']
    """

    io_dict = {}
    io_dicts = {}
    oldUt = getuptime()
    iodict1 = get_io_dict()
    time.sleep(1)
    newUt = getuptime()
    total_time = newUt - oldUt
    iodict2 = get_io_dict()
    for key,value in iodict1.items():
        io_dict[key] = [abs((t2-t1)) for t1, t2 in zip(value, iodict2[key])]
    for key,value in io_dict.items():
        io_dicts[key] = dict(
            zip(
                ( 'rrqm/s',
                  'wrqm/s',
                  'r/s',
                  'w/s',
                  'rsec',
                  'wsec',
                  'avgrq-sz',
                  'avgqu-sz',
                  'await',
                  'svctm',
                  'util' ),
                ( str("%.2f" % try_div([value[1], total_time])),
                  str("%.2f" % try_div([value[5], total_time])),
                  str("%.2f" % try_div([value[0], total_time])),
                  str("%.2f" % try_div([value[4], total_time])),
                  str("%.2f" % try_div([value[2], total_time])),
                  str("%.2f" % try_div([value[6], total_time])),
                  str("%.2f" % try_div([(value[2] + value[6]), (value[0] + value[4]), total_time])),
                  str("%.2f" % try_div([value[9], 1000, total_time])),
                  str("%.2f" % try_div([(value[3] + value[7]), (value[0] + value[4]), total_time])),
                  str("%.2f" % try_div([value[10], (value[0] + value[4]), total_time])),
                  str("%.2f" % try_div([value[10], 1000, total_time])), )
            )

        )

    #print io_dicts
    return {'iostat': io_dicts}
 
def get_cpu_list():

    with open("/proc/stat") as f:
        one_line = f.readline().replace("cpu", "").split()
    return map(int, one_line)

def cpu_stat():

    cpulist1 = get_cpu_list()
    time.sleep(0.1)
    cpulist2 = get_cpu_list()
    cpulist = [(t2-t1) for t1, t2 in zip(cpulist1, cpulist2)]
    total_time = sum(cpulist)
    cpu_disk = dict( 
        zip(
            ( 'us', 
              'sy',
              'id',
              'ni',
              'wa',
              'hi',
              'si',
              'st'),
            ( str("%.2f%%" % ((cpulist[0] + cpulist[1]) * 100.0 / total_time)),
              str("%.2f%%" % ((cpulist[2] + cpulist[5] +cpulist[6]) * 100.0 / total_time)),
              str("%.2f%%" % (cpulist[3] * 100.0 / total_time)),
              str("%.2f%%" % (cpulist[1] * 100.0 / total_time)),
              str("%.2f%%" % (cpulist[4] * 100.0 / total_time)),
              str("%.2f%%" % (cpulist[5] * 100.0 / total_time)),
              str("%.2f%%" % (cpulist[6] * 100.0 / total_time)),
              str("%.2f%%" % (cpulist[7] * 100.0 / total_time)), ) 
         ) 
    )
#    print cpu_disk 
    return {'cpustat': cpu_disk} 

def mem_stat():
    mem_total = {}
    mem_need = {}
    with open("/proc/meminfo") as f:
        for line in f.readlines():
            if len(line) < 2: continue
            name = line.split(':')[0]
            var = line.split(':')[1].split()[0]
            #mem[name] = long(var) * 1024.0
            mem_total[name] = int(var)
    mem_need['MemTotal'] = mem_total['MemTotal']
    mem_need['MemFree'] = mem_total['MemFree']
    mem_need['MemUsed'] = mem_total['MemTotal'] - mem_total['MemFree']
    mem_need['Buffers'] = mem_total['Buffers']
    mem_need['Cached'] = mem_total['Cached']
    mem_need['BuffCacheUsed'] = mem_need['MemUsed'] - mem_need['Buffers'] - mem_need['Cached']
    mem_need['BuffCacheFree'] = mem_need['MemFree'] + mem_need['Buffers'] + mem_need['Cached']
    mem_need['SwapTotal'] = mem_total['SwapTotal']
    mem_need['SwapUsed'] = mem_total['SwapCached']
    mem_need['SwapFree'] = mem_total['SwapFree']

#    print mem_need
    return {'memstat': mem_need}

def disk_stat():
    
    filesys = []
    disk_dict = {}
    with open("/proc/filesystems") as f:
        for line in f.readlines():
            if not line.startswith("nodev"):
                filesys.append(line.strip())

    retlist = []
    with open("/proc/mounts") as f:
        for line in f.readlines():
            if line.startswith('none'):continue
            fields = line.split()
            mountpoint = fields[1]
            fstype = fields[2]
            if fstype not in filesys:continue
            retlist.append(mountpoint)
    for path in retlist:
        st = os.statvfs(path)
        size = (st.f_blocks * st.f_frsize) / 1024
        avail = (st.f_bavail * st.f_frsize) / 1024
        used = ((st.f_blocks - st.f_bfree) * st.f_frsize) / 1024
        percent = used * 100.0 / size
        iused = (st.f_files - st.f_ffree) * 100.0 / st.f_files

        disk_dict[path] = dict(
            zip(
                ( 'Size',
                  'Used',
                  'Avail',
                  'Use%',
                  'IUsed' ),
                (
                  size,
                  used,
                  avail,
                  str("%.2f%%" % percent),
                  str("%.2f%%" % iused ), )
            )        
        )

   # print disk_dict
    return {'diskstat': disk_dict} 


def net_stat(): 
    ''' pretreatment of netstat from /proc/net/dev
    return:
data_keys = {
        'netstat': {}
        }
    '''

    data_keys = {}
    net_dict = {} 
    with open("/proc/net/dev") as f:
        for line in f.readlines()[2:]: 
            if not line.strip().startswith(('eth', 'bond')):continue 
            con = re.split('[ :]+',line.strip()) 
            net_dict[con[0]] = dict( 
                zip(
                    ( 'ReceiveBytes', 'ReceivePackets', 'ReceiveErrs',
                      'ReceiveDrop', 'ReceiveFifo', 'ReceiveFrames',
                      'ReceiveCompressed', 'ReceiveMulticast', 'TransmitBytes',
                      'TransmitPackets', 'TransmitErrs', 'TransmitDrop', 
                      'TransmitFifo', 'TransmitFrames', 'TransmitCompressed',
                      'TransmitMulticast' ),
                    ( con[1], con[2], con[3],
                      con[4], con[5], con[6],
                      con[7], con[8], con[9],
                      con[10], con[11], con[12],
                      con[13], con[14], con[15],
                      con[16], ) 
                 ) 
            )

    #print net_dict 
    return {'netstat': net_dict} 

def server_stat():
    '''server status
    '''

    serverstat = {}
    serverstat = cpu_stat()
    serverstat.update(load_process_stat())
    serverstat.update(io_stat())
    serverstat.update(mem_stat())
    serverstat.update(disk_stat())
    serverstat.update(net_stat())
    info = json.dumps(serverstat)

    print info
    #return info

if __name__ == "__main__":
    server_stat()
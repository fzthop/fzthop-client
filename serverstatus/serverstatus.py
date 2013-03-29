#!/usr/bin/env python
# -*- coding: utf-8 -*-
#获取服务器资源使用情况 

__authors__  = ['ARES-HHD <ARES.HHD@gmail.com>', ]
__version__  = "0.2"
__date__     = "2013-3-28"
__license__  = "GPL v2.0"

import subprocess
import json
import os
import re

class SubProcess(object):
    """docstring for SubProcess"""
    def __init__(self, cmd, arg):
        self.cmd = cmd
        self.arg = arg
    def popen(self):
        output = subprocess.Popen(self.cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        output_list = output.stdout.read().split(self.arg)
        return output_list

def cpu_process_load_mem_stat():
    """ cpu、进程、负载、内存状态

    """

    cmd = "/usr/bin/top -bi -n 2 -d 0.02"
    arg = "\n\n\n"
    data_keys = {}
    output = SubProcess(cmd, arg)
    output_list = output.popen()[1].split('\n')

    #cpustat
    cpu_dict = {}
    cpu_messages = output_list[2]
    message_list = re.split('[:,%]',cpu_messages)
    for i in range(len(message_list[1::2])):
        cpu_dict[message_list[2::2][i]] = message_list[1::2][i].strip()

    #processstat
    process_dict = {}
    process_messages = output_list[1]
    process_list = re.split('[ ,]+',process_messages)
    for i in range(len(process_list[1::2])):
        process_dict[process_list[2::2][i]] = process_list[1::2][i].strip()

    #loadstat
    load_dict = {}
    load_messages = output_list[0].split(',')
    load_dict['uptime'] = load_messages[0].split(' ',4)[-1] + load_messages[1]
    load_dict['users'] = load_messages[2].strip()
    load_dict['1min'] = load_messages[3].split(':')[-1].strip()
    load_dict['5min'] = load_messages[4].strip()
    load_dict['10min'] = load_messages[5].strip()

    #memstat
    mem_dict = {}
    mem_messages = output_list[3] + ' ' + output_list[4]
    mem_list = re.split('[ :,]+',mem_messages)
    mem_dict['MemTotal'] = mem_list[1].strip('k')
    mem_dict['MemFree'] = mem_list[5].strip('k')
    mem_dict['MemUsed'] = mem_list[3].strip('k')
    mem_dict['Buffers'] = mem_list[7].strip('k')
    mem_dict['Cached'] = mem_list[16].strip('k')
    mem_dict['BuffCacheUsed'] = str( int(mem_dict['MemUsed']) - int(mem_dict['Buffers']) - int(mem_dict['Cached']) )
    mem_dict['BuffCacheFree'] = str( int(mem_dict['MemFree']) + int(mem_dict['Buffers']) + int(mem_dict['Cached']) )
    mem_dict['SwapTotal'] = mem_list[10].strip('k')
    mem_dict['SwapUsed'] = mem_list[12].strip('k')
    mem_dict['SwapFree'] = mem_list[14].strip('k')

    data_keys = {
        'cpustat': cpu_dict,
        'processstat': process_dict,
        'loadstat': load_dict,
        'memstat': mem_dict
        }
    return data_keys
    #print {'cpustat': cpu_dict,'processstat': process_dict,'loadstat': load_dict,'memstat': mem_dict}


def disk_stat():
    """ 磁盘状态，单位k
    """
    
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
    """ 网卡流量  
    """

    net_disk = {}
    with open("/proc/net/dev") as f:
        for line in f.readlines()[2:]:
            if not line.strip().startswith(('eth', 'bond')):continue
            con = re.split('[ :]+',line.strip())
            net_disk[con[0]] = dict(
                zip(
                    ( 'ReceiveBytes', 'ReceivePackets', 'ReceiveErrs',
                      'ReceiveDrop', 'ReceiveFifo', 'ReceiveFrames',
                      'ReceiveCompressed', 'ReceiveMulticast', 'TransmitBytes',
                      'TransmitPackets', 'TransmitErrs', 'TransmitDrop',
                      'TransmitFifo', 'TransmitFrames', 'TransmitCompressed',
                      'TransmitMulticast' ),
                      con[1:17]
                )
            )

    #print net_disk
    return {'netstat': net_disk}

def io_stat():
    """ 磁盘IO
    """

    cmd = "/usr/bin/iostat -x"
    arg = "\n\n"
    io_dict = {}
    output = SubProcess(cmd, arg)
    output_list = output.popen()[2].split('\n')[1:]

    for line in output_list:
        con = line.split()
        io_dict[con[0]] = dict(
                zip(
                    ( 'rrqm/s', 'wrqm/s', 'r/s',
                      'w/s', 'rsec/s', 'wsec/s',
                      'avgrq-sz', 'avgqu-sz', 'await',
                      'svctm', '%util' ),
                      con[1:12]
                    )
                )

    #print io_dict
    return {'iostat': io_dict}

def server_stat():
    """server status
    """

    serverstat = {}
    serverstat = cpu_process_load_mem_stat()
    serverstat.update(disk_stat())
    serverstat.update(net_stat())
    serverstat.update(io_stat())
    info = json.dumps(serverstat)

    print info
    #return info

if __name__ == "__main__":
    server_stat()

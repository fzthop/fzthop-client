# coding=utf-8
"""
计算最大的公网IP
"""
import socket
import struct


def ipDecimal(ip):
    return socket.ntohl(struct.unpack("I",socket.inet_aton(ip))[0])
def ipString(ip):
    return  socket.inet_ntoa(struct.pack('I',socket.htonl(ip)))

class Ipaddress():
    """

    """
    def maxInetip(self,ipaddress):
        """
        A类： 10.0.0.0    ~ 10.255.255.255
        B类： 172.16.0.0  ~ 172.31.255.255
        C类： 192.168.0.0 ~ 192.168.255.55
        """
        aMin = ipDecimal('10.0.0.0')
        aMax = ipDecimal('10.255.255.255')
        bMin = ipDecimal('172.16.0.0')
        bMax = ipDecimal('172.31.255.255')
        cMin = ipDecimal('192.168.0.0')
        cMax = ipDecimal('192.168.255.255')
        ipInet = []
        all    = []
        ipList = ipaddress
        ipList = ','.join(ipList)
        ipList = ipList.split(',')
        for ip in ipList:
            ip = ipDecimal(ip)
            all.append(ip)
            if   aMin < ip < aMax:
                pass
            elif bMin < ip < aMax:
                pass
            elif cMin < ip < cMax:
                pass
            else:
                ipInet.append(ip)
        if ipInet:
            ipInet.reverse()
            ip = ipInet[0]
            return ipString(ip)
        else:
            all.reverse()
            ip = all[0]
            return ipString(ip)

ipaddress = Ipaddress()
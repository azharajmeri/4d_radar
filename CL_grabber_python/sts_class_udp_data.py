# -*- coding: utf-8 -*-
"""
Created on Tue May 16 09:08:07 2017

@author: Apu
"""
import socket
import numpy as np

class get_data_udp:

    def __init__(self,UDP_IP_ADDRESS,UDP_PORT_NO):

        self.UDP_IP_ADDRESS= UDP_IP_ADDRESS
        self.UDP_PORT_NO = UDP_PORT_NO     # Arbitrary non-privileged port
        #self.s= socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        #self.s.settimeout(5.0)

        return


    def write_server_command(self,strx):

        d= strx.encode('ASCII')
        self.s.sendto(d, (self.UDP_IP_ADDRESS, self.UDP_PORT_NO))
        data, server = self.s.recvfrom(1024)
        statusx= data.decode().strip().split()[1]

        return statusx


    def write_server_command_beta(self,strx,timeout=1):

        d= strx.encode('ASCII')
        flag = False

        self.s= socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.s.settimeout(timeout)

        for i in range(60):
            try:
                self.s.sendto(d, (self.UDP_IP_ADDRESS, self.UDP_PORT_NO))
                while 1:
                    data, a = self.s.recvfrom(1024)         # For READ JSON API maximum byte size is 12k Bytes.
                    statusx = data.decode().strip()

                    resp = statusx.split(':')[1].split(' ')
                    if ('SUCCESS' in resp) or ('FAILURE' in resp):
                        flag = True
                        break
            except socket.timeout:
                print('[{}] Socket timedout'.format(i))
                continue
            except:
                break

            if flag:
                break

        #self.s.sendto(d, (self.UDP_IP_ADDRESS, self.UDP_PORT_NO))
        #data, server = self.s.recvfrom(1024)
        #statusx= data.decode().strip()

        self.s.close()

        return statusx


    def create_iterlist(self,txlist,freqlist):

        iterlist=[]
        for tx in txlist:
            for freq in freqlist:
                iterlist.append([tx,freq])

        N= len(freqlist)*len(txlist)

        return iterlist,N


    def create_iterlist_beta(self,iclist,txlist,freqlist):

        iterlist=[]

        for ic in iclist:
            for tx in txlist:
                for freq in freqlist:
                    iterlist.append([ic,tx,freq])

        N= len(iclist)*len(freqlist)*len(txlist)

        return iterlist,N


    def write_txcw_commands(self,case):

#        strx= case[0][0:2]+'CW '+str(2**(int(case[0])))+ ' ' + case[1]+' '+str(2**(int(case[0][2:])))
        strx= case[1][0:2]+'CW '+str(int(case[0])+1)+ ' '+case[2]+' '+str(2**(int(case[1][2:])))  # TXCW icno freq txport
        udptry=0
        while(udptry<10):
            udptry=udptry+1
            try:
                d= strx.encode('ASCII')
                self.s.sendto(d, (self.UDP_IP_ADDRESS, self.UDP_PORT_NO))
                data, server = self.s.recvfrom(1024)
                print("Response from UDP",data)
                break
            except self.s.timeout:
                print("Write timeout on socket",udptry)
                continue

        statusx= data.decode().strip().split()[1]

        return statusx,strx

    # RX/TX CW method for single chip board
    def write_rxcw_commands(self,case):

#        strx= case[0][0:2]+'CW '+str(2**(int(case[0])))+ ' ' + case[1]+' '+str(2**(int(case[0][2:])))
        if case[0][0:2] == 'RX':
            strx= case[0][0:2]+'CW '+str(int(case[0][2:])+1)+ ' '+case[1] + " \r" # RXCW ChID Frq  RX
        elif case[0][0:2] == 'TX':
            strx= case[0][0:2]+'CW '+case[1]+ ' '+str(int(case[0][2:])+1) # RXCW Frq ChID  TX
        else:
            print("Error")
        d= strx.encode('ASCII')
        self.s.sendto(d, (self.UDP_IP_ADDRESS, self.UDP_PORT_NO))

        data, server = self.s.recvfrom(1024)
        statusx= data.decode().strip().split()[1]

        return statusx,strx

    def get_sweep_dict(self):

        ramp_dict= {}

        ramp_dict['chipId']= 2
        ramp_dict['sweepBWMHz']= 500
        ramp_dict['startFreqGHz']= 79.400
        ramp_dict['upTimeUs']= 29.5
        ramp_dict['upHoldTimeUs']= 0
        ramp_dict['downTimeUs']= 2.25
        ramp_dict['downholdTimeUs']= 0
        ramp_dict['IdleTimeUs']= 10
        ramp_dict['numSamples']= 513

        return ramp_dict


    def create_sweep_command(self,startFreqList,ramp_dict):

        N= len(startFreqList)

        command_list=[]
        for i in range(N):
            ramp_dict['startFreqGHz']= startFreqList[i]
            strx='RAMPCONFIG'
            for keyx in ramp_dict.keys():
                strx= strx+' '+str(ramp_dict[keyx])

            command_list.append(strx+'\n')

        return command_list


    def initiate_new_connection(self):
        '''Initiates a new connection'''

        # try:
        #     self.s.close()
        # except:
        #     print()
        #     print('No connection exists to close')
        #     print()

        #self.UDP_IP_ADDRESS= UDP_IP_ADDRESS
        #self.UDP_PORT_NO = UDP_PORT_NO     # Arbitrary non-privileged port
        self.s= socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.s.settimeout(10.0)

        return

    def close_connection(self):

        self.s.close()

        return

    def write_server_command(self,strx):
        '''sends a single command to UDP and reads back the status'''

        d= strx.encode('ASCII')
        self.s.sendto(d, (self.UDP_IP_ADDRESS, self.UDP_PORT_NO))
        data, server = self.s.recvfrom(1024)
        #statusx= data.decode().strip().split()[1]

        return data.decode().strip()


    def write_bunch_of_commands(self,commandString):
        '''sends a bunch of commands and each attempt with new UDP connection'''

        statusArr = []

        N= len(commandString)

        for k in range(N):
            self.initiate_new_connection()
            statusx= self.write_server_command(commandString[k])

            #print('RESP is {}'.format(statusx))

            resp = statusx.split(':')[1].split(' ')
            if ('SUCCESS' in resp):
                print('Executed '+str(k+1)+'\'th UDP Command: '+commandString[k])
            else:
                print('Error in '+str(k+1)+'\'th UDP Command: '+commandString[k])

            statusArr.append(statusx)

            self.close_connection()

        return statusArr
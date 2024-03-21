# @file cl_grabber.py
# @file cl_grabber.py
#
# *****************************************************************************
# VERSION HISTORY
# ---------------------------------------------------------------------------
# Version  Author    Date       Comments
# ---------------------------------------------------------------------------
# 1.0      Steradian 04Jul2022  Initial version
# 1.1      Steradian 04Aug2022  Updated with storing data into csv files
# ****************************************************************************
#
# ------------------------------------------------------------------------------
# IMPORTS
# ------------------------------------------------------------------------------
import os
import datetime
import sys
from CL_grabber_python.tools import tools
from CL_grabber_python.sts_class_udp_data import get_data_udp
from csv import writer
from CL_grabber_python.servers import servers
import threading

from radar.models import Radar


class CL_Grabber():
    """
    CL_Grabber class to receive, parse and print Cluster and Trigger 
    data on console or into file
    """

    def __init__(self, radarIp, hostIp, pcPort=9001, clPort=9002,
                 trPort=9003):
        """
        This init takes radar configuration data.

        Parameters
        ----------
        radarIp : String
            Radar IP address.
        hostIp : String
            Host IP address.
        pcPort : Int, optional
            PC port number. The default is 9001.
        clPort : Int, optional
            CL port number. The default is 9002.
        trPort : Int, optional
            Trigger port number. The default is 9003.

        Returns
        -------
        None.

        """

        """ Variable initializations """
        self.myudp = ""
        self.radarIP = radarIp
        self.hostIP = hostIp
        self.pcPort = pcPort
        self.clPort = clPort
        self.trPort = trPort
        self.dataOptions = None
        self.cmdList = []
        self.logPath = ""
        self.tool = tools()
        self.headerPrint = 0
        self.saveTriggerHeader = 0
        self.jsonPath = os.getcwd() + "/config.json"
        self.trackObjCallback = None
        self.triggerCallback = None
        self.errorCallback = None
        self.radar_thread = threading.Thread(target=lambda:
        self.receiveData())

        """ Create UDP server """
        self.myudp = ""
        self.server = ""

    def configRadar(self):
        """
        This method validate user input and configure radar to 
        send cluster/trigger data to host

        Returns
        -------
        None.

        """
        """ Print input arguments """
        self.tool.consoleMessage("[INFO] Configuration:")
        self.tool.consoleMessage("\tRadar IP : " + self.radarIP)
        self.tool.consoleMessage("\tHost IP  : " + self.hostIP)
        self.tool.consoleMessage("\tPC Port  : " + str(self.pcPort))
        self.tool.consoleMessage("\tCL Port  : " + str(self.clPort))
        self.tool.consoleMessage("\tTrigger Port  : " + str(self.trPort))
        self.tool.consoleMessage("\tdataOptions  : " + str(self.dataOptions))

        self.cmdList.append("EXT_IP " + self.hostIP)
        self.cmdList.append("EXT_PCPORT  " + str(self.pcPort))
        self.cmdList.append("EXT_CLPORT  " + str(self.clPort))
        self.cmdList.append("EXT_TRIGGER_PORT   " + str(self.trPort))
        # self.cmdList.append("EXTTCP_CONNECT " + str(self.dataOptions))

        """ Send UDP commands to radar """
        self.myudp = get_data_udp(self.radarIP, 8888)
        retVal = self.sendUdp()
        if retVal < 0:
            return retVal

        """ Initializer servers module """
        sever = servers(self.hostIP, self.radarIP, self.pcPort,
                        self.clPort, self.trPort, self.dataOptions,
                        self.tool)
        self.server = sever

        return 0

    def tcpConnect(self):
        """
        This method send tcp connect value to radar

        Returns
        -------
        None.

        """
        self.cmdList.clear()
        self.cmdList.append("EXTTCP_CONNECT " + str(self.dataOptions))
        retVal = self.sendUdp()
        if retVal < 0:
            return retVal
        else:
            return 0

    def sendUdp(self):
        """
        This method sends UDP commands to radar

        Returns
        -------
        None.

        """
        statusArr = []
        try:
            statusArr = self.myudp.write_bunch_of_commands(self.cmdList)
        except Exception as e:
            print()
            print(e)
            self.tool.consoleError("Error while executing UDP")
            return -3

        for log in statusArr:
            self.tool.consoleMessage(log)

        return 0

    def createLogFolder(self):
        """
        This method creates log folder structure

        Returns
        -------
        None.

        """
        ct = str(datetime.datetime.now())
        ct = ct[:-7].replace(":", ".")
        logRoot = os.getcwd() + "/Log"
        if not os.path.exists(logRoot):
            os.mkdir(logRoot)

        self.logPath = logRoot + "/log_" + str(ct)
        os.mkdir(self.logPath)
        os.mkdir(self.logPath + "/PC")
        os.mkdir(self.logPath + "/CL")

    def displayData(self, rcvPkt):
        """
        This method display received data on console

        Parameters
        ----------
        rcvPkt : Data packet
            Received data packet from radar

        Returns
        -------
        None.

        """
        dataDict = rcvPkt

        if (dataDict["dataType"] == "CL"):
            curTime = self.tool.convertUnixToLocalTime(dataDict["timeStamp"][0], dataDict["timeStamp"][1])
            numClusters = len(dataDict["data"])
            frameNum = dataDict["frameNum"]

            self.tool.consoleMessage("")
            self.tool.consoleMessage(
                "Frame num: {}, no.of clusters: {}, time: {}".format(frameNum, numClusters, curTime))
            self.tool.consoleMessage(
                "==========================================================================================================================================");
            self.tool.consoleMessage(
                "    #   Id  lane  region       X(m)       Y(m)       Z(m)      Vx(km/h)      Vy(km/h)      Vz(km/h)     L(m)       W(m)       H(m)   Class")

            for i in range(0, numClusters):
                clPkt = dataDict["data"][i]

                """ Object type """
                objType = ""
                if (clPkt["obj_type"] == 2):
                    objType = "2w"
                elif (clPkt["obj_type"] == 4):
                    objType = "s4w"
                elif (clPkt["obj_type"] == 6):
                    objType = "b4w"
                else:
                    objType = "undef"

                self.tool.consoleMessage(
                    "{:5d}{:5d}{:6d}{:8d}{:11.2f}{:11.2f}{:11.2f}{:14.2f}{:14.2f}{:14.2f}{:9.2f}{:11.2f}{:11.2f}{:>8s}"
                    .format(i + 1, clPkt["objId"], clPkt["laneNum"], clPkt["regionNumber"],
                            clPkt["x"], clPkt["y"], clPkt["z"], (3.6 * clPkt["vel_x"]),
                            (3.6 * clPkt["vel_y"]), (3.6 * clPkt["vel_z"]),
                            clPkt["length"], clPkt["width"], clPkt["height"], objType));

            self.headerPrint = 0

        elif (dataDict["dataType"] == "TRIGGER"):
            if self.headerPrint == 0:
                self.tool.consoleMessage("")
                self.tool.consoleMessage(
                    "================================================================================================================");
                self.tool.consoleMessage(
                    "TimeStamp                       TrackID   Trigger    X(m)    Y(m)    Vx(km/h)    Vy(km/h)  Lane  objType    L(m)");

            trPkt = dataDict["data"]
            triggertype = ""
            curTime = self.tool.convertUnixToLocalTime(trPkt["timeSeconds"],
                                                       trPkt["timeMicroSeconds"])

            if (trPkt["triggerType"] == 1):
                triggertype = "[Range]"
            if (trPkt["triggerType"] == 2):
                triggertype = "[Speed]"
            if (trPkt["triggerType"] == 3):
                triggertype = "[Class]"

            objType = ""
            if (trPkt["obj_type"] == 2):
                objType = "2w"
            elif (trPkt["obj_type"] == 4):
                objType = "s4w"
            elif (trPkt["obj_type"] == 6):
                objType = "b4w"
            else:
                objType = "undef"

            self.tool.consoleMessage("[{:s}]\t{:5d}{:>10s}{:8.2f}{:8.2f}{:12.2f}{:12.2f}{:6d}{:>8s}{:9.2f}"
                                     .format(curTime, trPkt["trackId"], triggertype, trPkt["x"] / 10, trPkt["y"] / 10,
                                             (trPkt["vel_x"] * 3.6) / 10,
                                             (trPkt["vel_y"] * 3.6) / 10, trPkt["laneNumber"], objType,
                                             (trPkt["length"] / 10)))

            self.headerPrint = 1

        else:
            pass

    def saveData(self, rcvPkt):

        """
        This method save received CL and TRIGGER data into CSV file

        Parameters
        ----------
        rcvPkt : Data packet
            Receied data packet from radar

        Returns
        -------
        None.

        """
        dataDict = rcvPkt

        if (dataDict["dataType"] == "CL"):
            curTime = self.tool.convertUnixToLocalTime(dataDict["timeStamp"][0],
                                                       dataDict["timeStamp"][1])
            numClusters = len(dataDict["data"])
            frameNum = dataDict["frameNum"]

            """ Save cluster data into file """
            try:
                with open(self.logPath + '/CL/CL_{}.csv'.format(frameNum), 'w', newline='') as f_object:
                    writer_object = writer(f_object)
                    writer_object.writerow(self.server.clPktParams)
                    for i in range(0, numClusters):
                        clPkt = dataDict["data"][i]

                        csvWrite = []
                        for i in self.server.clPktParams:
                            csvWrite.append("{:.3f}".format(clPkt[i]))
                        writer_object.writerow(csvWrite)

                    f_object.close()
            except Exception as e:
                print()
                print(e)
                self.tool.consoleWarning("Unable to write into CSV file")

        elif (dataDict["dataType"] == "TRIGGER"):

            trPkt = dataDict["data"]
            curTime = self.tool.convertUnixToLocalTime(trPkt["timeSeconds"],
                                                       trPkt["timeMicroSeconds"])

            """ Save trigger data into file """
            try:
                with open(self.logPath + '/TR.csv', 'a', newline='') as f_object:
                    writer_object = writer(f_object)
                    if self.saveTriggerHeader == 0:
                        writer_object.writerow(
                            ["time", "numErr", "TrackID", "Trigger", "X(m)", "Y(m)", "Vx(km/h)", "Vy(km/h)", "Lane",
                             "objType", "L(m)"])
                        self.saveTriggerHeader = 1

                    trPkt = dataDict["data"]
                    csvWrite = []

                    trType = ""
                    if trPkt['triggerType'] == 1:
                        trType = "[Range]"
                    elif trPkt['triggerType'] == 2:
                        trType = "[Speed]"
                    elif trType['triggerType'] == 3:
                        trType = "[Class]"

                    objType = ""
                    if (trPkt['obj_type'] == 2):
                        objType = "2w"
                    elif (trPkt['obj_type'] == 4):
                        objType = "s4w"
                    elif (trPkt['obj_type'] == 6):
                        objType = "b4w"
                    else:
                        objType = "undef"

                    csvWrite.append(curTime)
                    csvWrite.append(self.server.trigCheckumErrCnt)
                    csvWrite.append(trPkt['trackId'])
                    csvWrite.append(trType)

                    """ X, Y, Vx, Vy """
                    for i in self.server.trPktParams[7:11]:
                        csvWrite.append("{:.3f}".format(trPkt[i]))

                    csvWrite.append(trPkt['laneNumber'])
                    csvWrite.append(objType)
                    csvWrite.append("{:.3f}".format(trPkt['length']))

                    writer_object.writerow(csvWrite)
                    f_object.close()
            except Exception as e:
                print()
                print(e)
                self.tool.consoleWarning("Unable to write into CSV file")

        else:
            pass

    def registerCallBack(self, errorCallback, trackObjCallBack=None, triggerCallback=None):
        """
        This method register user callbacks

        Parameters
        ----------
        errorCallback : Method
            Error data call back.
        trackObjCallBack : Method, optional
            Cluster data callback. The default is None.
        triggerCallback : Method, optional
            Trigger data callback. The default is None.
        
        Returns
        -------
        None.

        """
        self.trackObjCallback = trackObjCallBack
        self.triggerCallback = triggerCallback
        self.errorCallback = errorCallback

        if self.trackObjCallback != None and self.triggerCallback != None:
            self.dataOptions = 5
        elif self.trackObjCallback != None and self.triggerCallback == None:
            self.dataOptions = 2
        elif self.trackObjCallback == None and self.triggerCallback != None:
            self.dataOptions = 7
        else:
            self.dataOptions = 0

    def receiveData(self):
        """
        This method creates servers and read data from radar.

        Returns
        -------
        None.

        """
        radarConfigExecuted = False
        while True:
            try:
                self.createLogFolder()
                if self.configRadar() < 0:
                    self.errorCallback("[ERROR] UDP execution error")
                else:
                    radarConfigExecuted = True

                while True:
                    """ Create servers """
                    radar = Radar.objects.first()
                    if radar:
                        print("-"*40)
                        print(radar.ip, radar.host_ip)
                        print("-"*40)
                        self.server.radarIP = radar.ip
                        self.server.hostIP = radar.host_ip

                    self.server.createServers()

                    """ Execute TCP connect when UDP commands executed """
                    if radarConfigExecuted == True:
                        if self.tcpConnect() < 0:
                            self.errorCallback("[ERROR] UDP execution error")
                        # radarConfigExecuted = False

                    """ Start receivng data """
                    dataDict = self.server.receivePkt()
                    if dataDict == -2:
                        self.errorCallback("[ERROR] socket timeout")

                    if (dataDict["dataType"] == "CL"):
                        if self.trackObjCallback != None:
                            self.trackObjCallback(dataDict)

                    elif (dataDict["dataType"] == "TRIGGER"):
                        if self.triggerCallback != None:
                            self.triggerCallback(dataDict)

                    """ Save received data """
                    self.saveData(dataDict)

                    """ Close all connections """
                    self.server.closeAllConnections()

            except KeyboardInterrupt:
                self.tool.consoleError("===== KEY BOARD INTERRUPT =====")
                sys.exit(1)
            except Exception as e:
                print()
                print(e)
                self.tool.consoleError("Connection Failure")
                self.tool.consoleMessage("Reconnecting...")

    def receiveDataNonBlocking(self):

        """
        This method starts non-blocking radar data reception

        Returns
        -------
        None.

        """
        self.radar_thread.start()

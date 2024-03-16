 # @file servers.py
 #
 #*****************************************************************************
 # VERSION HISTORY
 # ---------------------------------------------------------------------------
 # Version  Author    Date       Comments
 # ---------------------------------------------------------------------------
 # 1.0      Steradian 16Mar2023  Initial version
 # 1.1      Steradian 23May2023  Added code to re-use ports if connection is
 #                               already exist. 
 # 1.2      Steradian 29May2023  Added checksum validation
 #****************************************************************************
 #
 
#------------------------------------------------------------------------------
# IMPORTS
#------------------------------------------------------------------------------
import socket
import select
import time
import struct

class servers():
    """
    This Class provies supportive methods for automation
    """
    def __init__(self, hostIp, radarIp, pcPort, clPort, trPort, dataFlag, 
                 tool):
        """
        Initialize port numbers

        Parameters
        ----------
        hostIp : String
            Host IP address.
        radarIp : String
            Radar IP address.
        pcPort : Int
            Point Cloud data port number.
        clPort : Int
            Cluster data port number.
        trigPort : Int
            Trigger data port number.

        Returns
        -------
        None.

        """
        self.server1             = ""
        self.server2             = ""
        self.server3             = ""
        self.connections         = []
        self.connectionsOut      = []
        self.hostIP              = hostIp
        self.radarIP             = radarIp
        self.pcPort              = pcPort
        self.clPort              = int(clPort)
        self.trPort              = int(trPort)
        self.dataFlag            = int(dataFlag)
        self.tool                = tool
        self.clHeaderStructStr   = 'i3I4HbBH2I4H2I4Hf3H62B'
        self.clStructStr         = 'h2b15f4b3f4b'
        self.trStructStr         = '3Bb3I4h2BbB2I2hI4H4B'
        self.clPktParams         = ["objId", "laneNum", "regionNumber", 
                                    "length", "width", "height", "x", "y", "z", 
                                    "yaw_ang", "yaw_rate", "vel_x", "vel_y", 
                                    "vel_z", "acc_x", "acc_y", "acc_z", 
                                    "rcs", "obj_type", "reserved1_0",
                                    "reserved1_1", "reserved1_2",
                                    "closestPoint", "maxSnr", "meanSnr", 
                                    "numPts", "reserved2_0", "reserved2_1",
                                    "reserved2_2"]
        self.trPktParams         = ["numBytes" ,  "checksum", "triggerType", 
                                    "cpu_temp", "frameNumber", "timeSeconds", 
                                    "timeMicroSeconds" , "x" , "y",              
                                    "vel_x", "vel_y", "obj_type",           
                                    "laneNumber", "regionNumber", "trackId",            
                                    "boardSerial_0", "boardSerial_1",     
                                    "imu_pitch", "imu_yaw", "errorInfoGeneral",  
                                    "errorInfoIC_0", "errorInfoIC_1",     
                                    "errorInfoIC_2", "errorInfoIC_3",     
                                    "length", "reserved0", 
                                    "reserved1", "reserved2" ]
        
        self.dataTypePC          = "PC"
        self.dataTypeCL          = "CL"
        self.dataTypeTR          = "TRIGGER"        
        self.trigCheckumErrCnt   = 0
        self.timeoutVal          = 1
        
    def createServers(self):
        """
        Create servers to receive data from radar

        Returns
        -------
        None.

        """
        if self.dataFlag == 2:
            """ Create server for CL data """
            self.server1 = self.connectServer(self.hostIP, self.clPort, "CL")
            self.connections.append(self.server1)
        elif self.dataFlag == 7:
            """ Create server for TRIG data """
            self.server2 = self.connectServer(self.hostIP, self.trPort, "TRIGGER")
            self.connections.append(self.server2)
            self.outputs2 = []
        elif self.dataFlag == 5:
            """ Create server for CL & TRIG data """
            self.server1 = self.connectServer(self.hostIP, self.clPort, "CL")
            self.connections.append(self.server1)
            
            self.server2 = self.connectServer(self.hostIP, self.trPort, "TRIGGER")
            self.server2.listen(5)
            self.connections.append(self.server2)
        elif self.dataFlag == 1:
            """ Create server for CL & PC data """
            self.server1 = self.connectServer(self.hostIP, self.clPort, "CL")
            self.connections.append(self.server1)
            
            self.server3 = self.connectServer(self.hostIP, self.pcPort, "PC")
            self.connections.append(self.server3)
        elif self.dataFlag == 3:
            """ Create server for PC data """            
            self.server3 = self.connectServer(self.hostIP, self.pcPort, "PC")
            self.connections.append(self.server3)
            
    def connectServer(self, hostIP, portNum, portType):
        
        retryCnt = 15
        while retryCnt > 0:
            try :
                server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                server.settimeout(self.timeoutVal)
                server.setblocking(1)
                server.bind((hostIP, portNum))
                self.tool.consoleMessage("Waiting for {} Connection".format(portType))
                server.listen(5)
                return server
            
            except socket.error as e:
                self.tool.consoleError("Socket error:", str(e))
                self.tool.consoleMessage("Reconnecting...")
                continue
            
            except socket.timeout:
                self.tool.consoleMessage("Connection timed out, reconnecting...")
                retryCnt = retryCnt - 1
                continue
        
        return None
        
    def closeAllConnections(self):
        """
        This method close all connections

        Returns
        -------
        None.

        """
        
        for s in self.connections:
            s.close()

        self.connections.clear()
        
    def receivePkt(self):
        """
        This method read sockets untill data received

        Returns
        -------
        data : dict
            Received data in dictionry format

        """
        while True:
            data = self.receiveSockData()
            if data == None:
                continue
            else:
                return data

    def receiveSockData(self):
        """
        This method poll sockets and receive data

        Returns
        -------
        dataRcvd : dict/None
            Received data in dictionry format
            None in case of no data received

        """
        try:
            ready = select.select(self.connections, self.connectionsOut, 
                              self.connections, 0.010)   
        except socket.error as e:
            print(e)
            return
        except Exception as e:
            print()
            print(e)
            return

        for s in ready[0]:
            if s is self.server1:
                connection, client_address = s.accept()
                connection.setblocking(False)
                self.connections.append(connection)
                return None
            elif s is self.server2:
                connection, client_address = s.accept()
                connection.setblocking(False)
                self.connections.append(connection)
                return None
            elif s is self.server3:
                connection, client_address = s.accept()
                connection.setblocking(False)
                self.connections.append(connection)
                return None
            else:
                                
                """ Receive first 8 bytes of data from socket and check for 
                    HEADER string 
                """
                data = self.recvSockData(s, 8)
                if data == -2:
                    return -2
                if((data[0] == 83) and (data[1] == 84) and (data[2] == 83) and
                   (data[3] == 84) and (data[4] == 82) and (data[5] == 65) and
                   (data[6] == 67) and (data[7] == 82)):
                    """ It's CL packet """
                    return (self.recvClData(s, data))
                
                elif((data[0] == 83) and (data[1] == 84) and (data[2] == 83) and
                     (data[3] == 84) and (data[4] == 82) and (data[5] == 73) and
                     (data[6] == 71) and (data[7] == 71)):
                     """ It's TRIGG packet """
                     return (self.recvTriggdata(s, data))
               
                elif((data[0] == 83) and (data[1] == 84) and (data[2] == 83) and
                     (data[3] == 82) and (data[4] == 65) and (data[5] == 68) and
                     (data[6] == 65) and (data[7] == 82)):
                     """ It's PC packet """
                     return (self.recvPcData(s, data))

    def recvSockData(self, s, dataSize):
        """
        This method receive given length data from given socket

        Parameters
        ----------
        s : sock
            Socket to receive data.
        dataSize : Int
            Data size in bytes to read.

        Returns
        -------
        data : Binary
            Received data.

        """
        totalRecvdSize = 0
        recvdSize = 0
        remSize   = dataSize
        retryCnt  = 0
 
        """ Receive data in loop till given number of bytes received """
        data = s.recv(dataSize)
        remSize = dataSize - len(data)
        
        while (remSize > 0):
            l = ""
            try:
                l = s.recv(remSize)
                data = data + l
                retryCnt = 0
        
            except socket.error as e: 
                retryCnt += 1
                time.sleep(0.01)
                if retryCnt > 500:
                    return -2
            except Exception as e:
                print()
                print(e)
                return -2
  
            recvdSize = len(l)
            totalRecvdSize += recvdSize
            remSize = dataSize - totalRecvdSize
 
        return data
            
    def recvClData(self, s, headString):
        """
        This method receive cluster data from given socket

        Parameters
        ----------
        s : sock
            Socket to receive data.
        
        headString: SockData
            First 8 bytes received data
            
        Returns
        -------
        dataRcvd : dict
            Received data in dictionry format

        """
        cl_data_size    = 84
        """ 8 bytes of header received already, 132 bytes of remainig header """
        remHeadPktSize  = 132
        rcvdBinData     = headString
        
        """ Receive rest of the header  """
        data = self.recvSockData(s, remHeadPktSize)   
        rcvdBinData = rcvdBinData + data
        if data == -2:
            return -2
        
        """ Parse header """
        headerData   = struct.unpack(self.clHeaderStructStr,data[0:132]) # 'i3I4HbBH2I4H2I4Hf3H62B'
        numClusters  = headerData[0] 
        rcvdFrameNum = headerData[3]
        checksum     = headerData[47]
                 
        clDataList = []
        dataRcvd = {}
        dataRcvd["dataType"]  = self.dataTypeCL
        dataRcvd["frameNum"]  = rcvdFrameNum
        dataRcvd["timeStamp"] = [headerData[1], headerData[2]]
        
        #print("Received checksum : {} {} {} {} {}".format(headerData[45], headerData[46], headerData[47], headerData[48], headerData[49]))
        
        if numClusters != 0:
                        
            data = self.recvSockData(s, cl_data_size * numClusters)
            rcvdBinData = rcvdBinData + data    
            if data == -2:
                return -2
            for i in range(0, numClusters):
                start = i * cl_data_size
                end   = (i + 1) * cl_data_size
                """ Unpack individual cluster data """
                cl_data = struct.unpack(self.clStructStr, data[start:end])
                
                """ Convert data into dict format """                
                clDataDict = self.tool.createDictFromListData(self.clPktParams, cl_data)
                
                """ Convert velocity from m/s ro km/h """
                clDataDict["vel_x"] = clDataDict["vel_x"] * 3.6
                clDataDict["vel_y"] = clDataDict["vel_y"] * 3.6
                clDataDict["vel_z"] = clDataDict["vel_z"] * 3.6
                
                clDataList.append(clDataDict)
                            
            dataRcvd["data"] = clDataList
            calChecksum      = self.calculateChecksum(rcvdBinData)
            return dataRcvd
    
    def recvTriggdata(self, s, headString):
        """
        This method receive trigger data from given socket

        Parameters
        ----------
        s : sock
            Socket to receive data.
            
        headString: SockData
            First 8 bytes received data

        Returns
        -------
        dataRcvd : dict
            Received data in dictionry format

        """
        
        """ 8 bytes of trigger packet received already, 56 bytes of trigger 
            data left 
        """
        remTrigPktSize  = 56      
        rcvdBinData     = headString       
        trData = self.recvSockData(s, remTrigPktSize)
        rcvdBinData = rcvdBinData + trData  
        if trData == -2:
            return -2
        
        """ Unpck data """
        trigger_data = struct.unpack(self.trStructStr, trData[0:56]) # '3Bb3I4h2BbB2I2hI4H4B'
        
        """ Convert data into dict format """
        dataRcvd = {}
        dataRcvd["dataType"] = self.dataTypeTR
        
        trDataDict = self.tool.createDictFromListData(self.trPktParams, trigger_data)
        dataRcvd["data"] = trDataDict
        
        """ Convert 0.1 meter to meter and m/s to km/h """
        dataRcvd["data"]["x"] = dataRcvd["data"]["x"]/10
        dataRcvd["data"]["y"] = dataRcvd["data"]["y"]/10
        dataRcvd["data"]["vel_x"] = (dataRcvd["data"]["vel_x"]/10) * 3.6
        dataRcvd["data"]["vel_y"] = (dataRcvd["data"]["vel_y"]/10) * 3.6
        
        calChecksum = self.calculateChecksum(rcvdBinData)
        if calChecksum == trDataDict["checksum"]:
            return dataRcvd
        else:
            self.trigCheckumErrCnt = self.trigCheckumErrCnt + 1
            self.tool.consoleMessage("TRIGG data checksum error")
            return None

    def recvPcData(self, s, headString):
        """
        This method reads PC data from given socket and store into .bin file

        Parameters
        ----------
        s : sock
            Socket to receive data.
            
        headString: SockData
            First 8 bytes received data

        Returns
        -------
        None

        """
                
        data = self.recvSockData(s, 4)   
        if data == -2:
            return -2
        up_data = struct.unpack('i',data[0:4])
        numPoints = up_data[0]
        
        data = self.recvSockData(s, 128 + 84*numPoints)
        if data == -2:
            return -2
        up_data = struct.unpack('i',data[8:12])
        frame_num = up_data[0]
              
        # TODO: log_path is not defined
        file_name = self.log_path + "//pointCloud//PC_" + str(frame_num) + ".bin"
        binary_file = open(file_name, "wb")
        binary_file.write(data)
        binary_file.close()
        
    def calculateChecksum(self, data):
        """
        This method calcualtes checksum for given data

        Parameters
        ----------
        data : Bin
            Socket data

        Returns
        -------
        checksum : Hex
            Calculated checksum of the data

        """
        checkSumCalculated = 0
        for i in range(0, len(data)):
            if i == 9:
                continue
            """ Add all bytes except checksum byte """
            checkSumCalculated = checkSumCalculated + int(data[i])
                                      
        return (checkSumCalculated) & 0xFF
        
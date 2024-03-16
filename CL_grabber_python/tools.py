 # @file tools.py
 #
 #*****************************************************************************
 # VERSION HISTORY
 # ---------------------------------------------------------------------------
 # Version  Author    Date       Comments
 # ---------------------------------------------------------------------------
 # 1.0      Steradian 16Mar2023  Initial version
 #****************************************************************************
 #
 
#------------------------------------------------------------------------------
# IMPORTS
#------------------------------------------------------------------------------
import time
import datetime
from colorama import Fore, Style
import os
import json

class tools():
    """
    This Class provies supportive methods for automation
    """
    def __init__(self):
        pass
        "No code to execute"
                
    def getCutTime(self):
        """
        This method gets current data in below format
        yyyy-mm-dd Hr:Min:Sec.mSec

        Returns
        -------
        None.

        """
        ct = datetime.datetime.now()
        ct = str(ct)[0 : len(str(ct)) - 7]
        return ct
                           
    def consoleMessage(self, string, *args):
        """
        This method prints message with time stamp on console with given
        string and arguments

        Parameters
        ----------
        string : String
            DESCRIPTION.
        *args : String/Int/Float/etc..
            Arguments to print

        Returns
        -------
        None.

        """
        ct = self.getCutTime()
        print(ct + " [INFO]  : " + string % args)
                    
    def consoleWarning(self, string, *args):
        """
        This method prints warning with time stamp on console with given
        string and arguments

        Parameters
        ----------
        string : String
            DESCRIPTION.
        *args : String/Int/Float/etc..
            Arguments to print

        Returns
        -------
        None.

        """
        ct = self.getCutTime()
        print(ct + " [WARN]  : " + string % args)
                
    def consoleError(self, string, *args):
        """
        This method prints error with time stamp on console with given
        string and arguments

        Parameters
        ----------
        string : String
            DESCRIPTION.
        *args : String/Int/Float/etc..
            Arguments to print

        Returns
        -------
        None.

        """
        ct = self.getCutTime()
        print(Fore.RED + ct + " [ERROR] : " + string % args)
        print(Style.RESET_ALL)
                        
    def delay(self, time_sec):
        """
        This method wait for given number of seconds

        Parameters
        ----------
        time_sec : Int/Float
            Number of seconds to wait/sleep.

        Returns
        -------
        None.

        """
        time.sleep(time_sec)
        
    def createDictFromListData(self, List, data):
        """
        This method creates dictionary with given list keys and data

        Parameters
        ----------
        List : list
            List of keys.
        data : data
            Data to fill dictionary.

        Returns
        -------
        dictFormat : dict
            Data in dictionary format

        """
        dictFormat = dict.fromkeys(List)
        
        for i in range(0, len(data)):
            dictFormat[List[i]] = data[i]
            
        return dictFormat
    
    def convertUnixToLocalTime(self,timeSec, timeMilliSec):
        """
        Convert UNIX EPOCH time to local time

        Parameters
        ----------
        data : List
            UNIX EPOCH time.

        Returns
        -------
        loc_time : TYPE
            DESCRIPTION.

        """
        time1 = timeSec
        time2 = timeMilliSec
        loc_time = time.ctime(time1 + time2/1000000)
        return loc_time
    
    def readJsonData(self, jsonFile):
        """
        This method returns json data
    
        Parameters
        ----------
        jsonFile : String
            Json file along with path
    
        Returns
        -------
        data: Dictionary/-1
            Json data if json file available
            -1 if json file not available
    
        """
        if not os.path.exists(jsonFile):
            self.consoleError("Json file not exist: [{}]".format(jsonFile))
            return -1
        
        else:
            """ Open Json in read mode if file exists """
            with open(jsonFile) as f:
                jsonData = json.load(f)
                return jsonData
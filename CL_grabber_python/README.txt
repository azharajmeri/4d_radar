
CL_grabber application reads Trigger and Cluster data from radar through ethernet cable.

Usage: 
------
1. Open example_radar_app.py file.

2. Initialize CL_grabber constructor with radarIP and hostIP
   Usage: G = grabber.CL_Grabber(<radar IP>, <host IP>)
   E.g  : G = grabber.CL_Grabber("192.168.1.97", "192.168.56.13")
   
   Refer to Arguments section for more information.

3. Register callbacks based on the type of data to be recieved.
   E.g. :
   a. To receive Trigger + Cluster data
      G.registerCallBack( errorCallback    = onErrorCallback, 
                          trackObjCallBack = onTrackedObjCallback, 
                          triggerCallback  = onTriggerCallback)

   b. To receive only Trigger data
      G.registerCallBack( errorCallback    = onErrorCallback, 
                          trackObjCallBack = None, 
                          triggerCallback  = onTriggerCallback)

   c. To receive Cluster
      G.registerCallBack( errorCallback    = onErrorCallback, 
                          trackObjCallBack = onTrackedObjCallback, 
                          triggerCallback  = None)

4. Run example_radar_app.py file.

5. onTrackedObjCallback and onTriggerCallback methods print cluster and trigger data 
   respectively.


Arguments:
----------
radarIp  : Radar IP address
hostIp   : Host IP address
pcPort   : External PC port number, default = 9001
clPort   : External CL port number, default = 9002, 
trPort   : External CL port number, default = 9003, 
saveData : Flag to save received data or not, default = False
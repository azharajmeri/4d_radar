import threading

from django.apps import AppConfig


class RadarConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'radar'

    def ready(self):
        # Start the background task when Django starts up
        # broadcast_thread = threading.Thread(target=self.broadcast_message)
        # # broadcast_thread.daemon = True
        # broadcast_thread.start()
        self.broadcast_message()

    def broadcast_message(self):
        import CL_grabber_python.cl_grabber as grabber
        from CL_grabber_python.radar_app import onErrorCallback, onTriggerCallback

        G = grabber.CL_Grabber("192.168.40.217", "192.168.40.216")
        print("????????????????????????????????????")
        G.registerCallBack(errorCallback=onErrorCallback,
                           trackObjCallBack=None,
                           triggerCallback=onTriggerCallback)
        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>")

        G.receiveData()
        print("LLLLLLLLLLLLLLLLLLLLLLLLLLLLL")
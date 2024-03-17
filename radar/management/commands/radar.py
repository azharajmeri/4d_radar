import random
import time

import requests
from django.core.management.base import BaseCommand

import CL_grabber_python.cl_grabber as grabber
from CL_grabber_python.radar_app import onErrorCallback, onTriggerCallback


class Command(BaseCommand):
    help = "Connect Radar"

    def handle(self, *args, **options):
        G = grabber.CL_Grabber("192.168.40.217", "192.168.40.216")
        G.registerCallBack(errorCallback=onErrorCallback,
                           trackObjCallBack=None,
                           triggerCallback=onTriggerCallback)
        G.receiveData()
        # while True:
        #     try:
        #         requests.post("http://127.0.0.1:8000/radar-update/", json={"instance_id": random.randint(1, 40)})
        #     except Exception as e:
        #         print(e)
        #         print("Make sure the server is running!")
        #     time.sleep(5)

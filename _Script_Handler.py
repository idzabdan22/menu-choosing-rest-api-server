import json
import subprocess
import psutil
import serial
import time

class _Script_Handler:
    def __init__(self,): # parse object menu.json
        self.arduino_serial = serial.Serial ('/dev/ttyACM0',9600,timeout=0.1)
        _mapping = {}
        try:
            with open("config/menu.json") as json_file:
                json_data = json.load(json_file)
                for menu in json_data["menu"]:
                    _mapping[menu["id"]] = {
                        "name": menu["name"],
                        "command": menu["command"]
                    }
                self.menus = _mapping
        except Exception as e:
            print(e)

    def runner(self, id):
        try:
            cmd = self.menus[id]["command"]
            subprocess.Popen(cmd, shell=True, executable='/bin/bash')
        except Exception as e:
            print("CANNOT RUN SCRIPT", e)

    def deactiver(self,):
        try:
            runningProcess = ""
            while not runningProcess:
                result = subprocess.run(["ps -aux | grep python | grep menu.py"], shell=True, capture_output=True, text=True)
                runningProcess = result.stdout.split("\n")[0].split()[1]
                print(result.stdout.split("\n")[0].split()[1])
            cmd = f"kill -9 {runningProcess}"
            subprocess.call(cmd, shell=True, executable='/bin/bash')
            for _ in range(0,5):
                print("STOPPING ARDUINO")
                self.arduino_serial.write(bytes("1", 'utf-8'))
                time.sleep(0.1)
            print("SUCCESSFULLY STOPPED SCRIPT")
        except Exception as e:
            print("CANNOT RUN SCRIPT")
    
    def receiveCommand(self, command):
        if command != 0:
            self.runner(command)
        else:
            self.deactiver()



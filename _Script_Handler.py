import json
import os
import subprocess
import psutil
import time
import threading

class _Script_Handler:
    def __init__(self,): # parse object menu.json
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
                result = subprocess.run(["ps -aux | grep python | grep opencv.py"], shell=True, capture_output=True, text=True)
                runningProcess = result.stdout.split("\n")[0].split()[1]
                print(result.stdout.split("\n")[0].split()[1])
            cmd = f"kill SIGTERM {runningProcess}"
            subprocess.call(cmd, shell=True, executable='/bin/bash')
            # with open("output/runningPid.json", "r") as jsonFile:
            #     data = json.load(jsonFile)
            #     pid = data["running_pid"]
            print("SUCCESSFULLY STOPPED SCRIPT")
        except Exception as e:
            print("CANNOT RUN SCRIPT")
    
    def runningChecker(self,):
        while True:
            if psutil.pid_exists(self.runningId+1):
                print("SUCCESSFULLY RUNNING SCRIPT")
                break
            else:
                print("INIT")
    
    def receiveCommand(self, command):
        # runnerThread = threading.Thread(target=self.runner, args=(id,))
        # deactiverThread = threading.Thread(target=self.deactiver, args=())
        # runnerThread.start()
        # deactiverThread.start()
        # runnerThread.join()
        if command != 0:
            self.runner(command)
        else:
            self.deactiver()



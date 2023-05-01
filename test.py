import os
import psutil



import subprocess

result = subprocess.run(["ps -aux | grep python | grep loop.py"], shell=True, capture_output=True, text=True)

print(result.stdout.split("\n")[0].split()[1])

# Iterate over all running process
# for proc in psutil.process_iter():
#     try:
#         # Get process name & pid from process object. 
#         # print(proc)
#         processName = proc.name()
#         processID = proc.pid
#         print(processName , ' ::: ', processID)
#     except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
#         pass

# import psutil

# listOfProcessNames = list()
# # Iterate over all running processes
# for proc in psutil.process_iter():
#    # Get process detail as dictionary
#    pInfoDict = proc.as_dict(attrs=['pid', 'name', 'cpu_percent'])
#    # Append dict of process detail in list
#    listOfProcessNames.append(pInfoDict)
# print(os.getpid())
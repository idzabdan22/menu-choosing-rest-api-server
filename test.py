# import subprocess
# import multiprocessing
# import time

# import subprocess
# cmd = 'conda init bash  && . /home/abdan2345/miniconda3/bin/activate abdan2 && cd /home/abdan2345/Development/menu_app_v1/backend && python3 opencv.py'
# pid = subprocess.Popen(cmd, shell=False, executable='/bin/bash')
# print("ALL PROCESS SHOULD BE DONE", pid)
# # cmd = 'conda init bash  && . /home/abdan2345/miniconda3/bin/activate abdan2 && cd /home/abdan2345/Development/menu_app_v1/backend && python3 test_copy.py'
# # pid = subprocess.Popen(cmd, shell=True, executable='/bin/bash')

# # while True:
# #     children = multiprocessing.active_children()
# #     print(children)
# #     time.sleep(5)
# #     pass

# import pyaudio

import pyaudio

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
SHORT_NORMALIZE = (1.0/32768.0)
TIMEOUTSIGNAL = ((RATE / CHUNK * 1)+2)
TEMPORARY_WAVE_FILENAME = "audio/temp.wav"
SWIDTH = 2
Threshold = 60

p = pyaudio.PyAudio()
info = p.get_host_api_info_by_index(0)

# p.open(input_host_api_specific_stream_info=)
numdevices = info.get('deviceCount')

for i in range(0, numdevices):
    if (p.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
        print("Input Device id ", i, " - ", p.get_device_info_by_host_api_device_index(0, i).get('name'))


# p.open(
#             format=FORMAT, 
#             channels=CHANNELS,
#             rate=RATE, 
#             input=True,
#             frames_per_buffer=CHUNK,
#             # input_device_index=7,
#         )

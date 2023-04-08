import pyaudio
import wave
import os
import math
import warnings
import time
import struct
import threading
from pynput import keyboard

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
warnings.filterwarnings('ignore')

SHORT_NORMALIZE = (1.0 / 32768.0)
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
swidth = 2
CHUNK = 1024
TimeoutSignal = ((RATE / CHUNK * 1) + 2)
Threshold = 55
audio = pyaudio.PyAudio()

def on_release(key):
    if key == keyboard.Key.enter:
        # Stop listener
        return False
    else:
        return True

def rms(frame):
    count = len(frame) / swidth
    format = "%dh" % (count)
    # short is 16 bit int
    shorts = struct.unpack(format, frame)
    sum_squares = 0.0
    for sample in shorts:
        n = sample * SHORT_NORMALIZE
        sum_squares += n * n
    # compute the rms
    rms = math.pow(sum_squares / count, 0.5)
    return rms * 1000


def recording(lastblock, stream, wav_name, wav_n, wav_num):
    global FORMAT, CHUNK, CHANNELS, RATE
    try:
        arr = []
        arr.append(lastblock)
        print("recording...")
        for i in range(0, int(TimeoutSignal)):
            data = stream.read(CHUNK)
            arr.append(data)

        print("Finish recording " + wav_n + ". Count: " + wav_num)

        waveFile = wave.open(wav_name, 'wb')
        waveFile.setnchannels(CHANNELS)
        waveFile.setsampwidth(audio.get_sample_size(FORMAT))
        waveFile.setframerate(RATE)
        waveFile.writeframes(b''.join(arr))
        waveFile.close()
        del stream
    except Exception as e:
        print(e)
        raise


def listen():
    global silence, STOPPING

    wav_id = "AFIFU"

    stream = audio.open(format=FORMAT, rate=RATE, channels=CHANNELS, frames_per_buffer=CHUNK, input=True)
    
    print("Welcome! id: " + wav_id)

    wav_path = [
        "/home/abdan2345/Dataset_Skripsi/Coba/",
        "/home/abdan2345/Dataset_Skripsi/Berhenti/",
        "/home/abdan2345/Dataset_Skripsi/Kanan/",
        "/home/abdan2345/Dataset_Skripsi/Kiri/",
        "/home/abdan2345/Dataset_Skripsi/Maju/",
        "/home/abdan2345/Dataset_Skripsi/Mundur/",
        "/home/abdan2345/Dataset_Skripsi/Satu/",
        "/home/abdan2345/Dataset_Skripsi/Dua/",
        "/home/abdan2345/Dataset_Skripsi/Tiga/",
        "/home/abdan2345/Dataset_Skripsi/Empat/",
        "/home/abdan2345/Dataset_Skripsi/Lima/",
        "/home/abdan2345/Dataset_Skripsi/Enam/",
        "/home/abdan2345/Dataset_Skripsi/Mati/",
        "/home/abdan2345/Dataset_Skripsi/Nyala/",
        "/home/abdan2345/Dataset_Skripsi/Info/",
        "/home/abdan2345/Dataset_Skripsi/Next/",
        "/home/abdan2345/Dataset_Skripsi/Back/",
        "/home/abdan2345/Dataset_Skripsi/Iya/",
        "/home/abdan2345/Dataset_Skripsi/Tidak/",
        "/home/abdan2345/Dataset_Skripsi/Keluar/",
        "/home/abdan2345/Dataset_Skripsi/Oke/",
    ]
    wav_name = [
        "Coba", "Berhenti", "Kanan", "Kiri", "Maju", 
        "Mundur", "Satu", "Dua", "Tiga", "Empat", 
        "Lima", "Enam", "Mati", "Nyala", "Info", 
        "Next", "Back", "Iya", "Tidak", "Keluar", 
        "Oke"]
    
    wav_num = 1
    wav_index = 0
    
    print("Your word is " + wav_name[wav_index])
    print("Your first instruction is: Read the word " + wav_name[wav_index] + " as NEUTRALLY as possible! Please press Enter to start recording!")
    
    with keyboard.Listener(on_release=on_release) as listener:
        listener.join()
        print("Start recording: " + wav_name[wav_index])

    while True:
        try:
            input = stream.read(CHUNK)
        except Exception as ex:
            print(ex)
            continue
        rms_value = rms(input)
        # print(rms_value)
        if rms_value > Threshold:
            silence = False
            LastBlock = input
            recording(LastBlock, stream, (wav_path[wav_index] + wav_id + "_" + wav_name[wav_index] + "_" + str(wav_num) + ".wav"), wav_name[wav_index], str(wav_num))
            wav_num += 1
            if wav_num == 11:
                wav_index += 1
                wav_num = 1

                # for i in range(3):
                #     print("wait for ", 3-i)
                #     time.sleep(1)

                print(wav_name[wav_index - 1] + " is done!")
                if wav_index == len(wav_name):
                    print("Thank You!")
                    exit()
                else:
                    print("Your next word is " + wav_name[wav_index])
                    print("Your first instruction is: Read the word " + wav_name[wav_index] + " as NEUTRALLY as possible! Please press Enter to start recording!")
                    with keyboard.Listener(
                            on_release=on_release) as listener:
                        listener.join()
                    print("Start recording: " + wav_name[wav_index])

            if wav_num == 6:
                print("First instruction is done!")
                print("Your next instruction is: Read the word " + wav_name[wav_index] + " as UNIQUELY as possible! Please press Enter to continue!")
                with keyboard.Listener(
                        on_release=on_release) as listener:
                    listener.join()
                print("Resume recording: " + wav_name[wav_index])


t1 = threading.Thread(target=listen, args=())

t1.start()

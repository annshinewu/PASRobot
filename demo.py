import IdentificationServiceHttpClientHelper
import sys
from CreateProfile import *
from EnrollProfile import *
from PrintAllProfiles import *
from IdentifyFile import *
from appJar import gui

def recordAudio():
    import pyaudio
    import wave
    
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 16000
    RECORD_SECONDS = 5
    WAVE_OUTPUT_FILENAME = "output.wav"
    
    p = pyaudio.PyAudio()
    
    stream = p.open(format=FORMAT,channels=CHANNELS,rate=RATE,input=True, frames_per_buffer=CHUNK)
    
    print("* recording")
    
    frames = []
    
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)
    
    print("* done recording")
    
    stream.stop_stream()
    stream.close()
    p.terminate()
    
    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

def enrollAudio():
    import pyaudio
    import wave
    
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 16000
    RECORD_SECONDS = 30
    WAVE_OUTPUT_FILENAME = "output.wav"
    
    p = pyaudio.PyAudio()
    
    stream = p.open(format=FORMAT,channels=CHANNELS,rate=RATE,input=True, frames_per_buffer=CHUNK)
    
    print("* recording")
    
    frames = []
    
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)
    
    print("* done recording")
    
    stream.stop_stream()
    stream.close()
    p.terminate()
    
    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

def press(btn):
    subscription_key = "1a6cfea9099a48f498c6cd2b0c01731d"
    if btn == "Enroll Voice":
        print("Please speak for 30 seconds continously")
        enrollAudio()
        newProfileId = create_profile(subscription_key,"en-US")
        enroll_profile(subscription_key, newProfileId, "/Users/annshinewu/Desktop/Cognitive-SpeakerRecognition-Python-master/Identification/output.wav", "true")
        print (newProfileId)
        app.stop()
    elif btn == "Identify Voice":
        print("Please speak for 5 seconds continously")
        recordAudio()
        profileList = print_all_profiles(subscription_key)
        getProfileId = 00000000-0000-0000-0000-000000000000
        count = 0
        while count < len(profileList):
            tempProfileId = identify_file(subscription_key,"/Users/annshinewu/Desktop/Cognitive-SpeakerRecognition-Python-master/Identification/output.wav", "true",{profileList[count]})
            if(tempProfileId != "00000000-0000-0000-0000-000000000000"):
                getProfileId = tempProfileId
            count = count + 1
        if getProfileId != "00000000-0000-0000-0000-000000000000":
            print (getProfileId)
        else:
            print("Please speak for 30 seconds continously")
            enrollAudio()
            newProfileId = create_profile(subscription_key,"en-US")
            enroll_profile(subscription_key, newProfileId, "/Users/annshinewu/Desktop/Cognitive-SpeakerRecognition-Python-master/Identification/output.wav", "true")
            print (newProfileId)
        app.stop()
    else:
        app.stop()

app = gui()

app.addLabel("title", "Voice Recognition Demo")
app.addButtons(["Enroll Voice", "Identify Voice"], press, 0, 0, 2)

app.go()

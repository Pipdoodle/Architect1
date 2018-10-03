import pygame
import pyaudio
import wave
from array import array
from struct import pack
import time
import speech_recognition as sr
import pyaudio
import wave
import time
import sys
import mainSubGameClass 
#taken from pyaudio documentation
def playSound(file):
    if len(file) < 2:
        print("Plays a wave file.\n\nUsage: %s filename.wav" % sys.argv[0])
        sys.exit(-1)
    
    wf = wave.open(file, 'rb')
    
    # instantiate PyAudio (1)
    p = pyaudio.PyAudio()
    
    # define callback (2)
    def callback(in_data, frame_count, time_info, status):
        data = wf.readframes(frame_count)
        return (data, pyaudio.paContinue)
    
    # open stream using callback (3)
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True,
                    stream_callback=callback)
    
    # start the stream (4)
    stream.start_stream()
    return stream
    
def endSound(stream):
    # wait for stream to finish (5)
    while stream.is_active():
        time.sleep(0.1)    
    # stop stream (6)
    stream.stop_stream()
    stream.close()
    wf.close()
    
    # close PyAudio (7)
    p.terminate()
import time

import speech_recognition as sr

#from speech recognizer documentation
# this is called from the background thread
def callback(recognizer, audio):
    # received audio data, now we'll recognize it using Google Speech Recognition
    try:
        # for testing purposes, we're just using the default API key
        # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
        # instead of `r.recognize_google(audio)`
        
        print("Google Speech Recognition thinks you said " + recognizer.recognize_google(audio))
        parse(recognizer.recognize_google(audio))
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
#speech recognizer documentation
def micRecord1():
    print("running")
    r = sr.Recognizer()
    m = sr.Microphone()
    with m as source:
        r.adjust_for_ambient_noise(source)  # we only need to calibrate once, before we start listening
    
    # start listening in the background (note that we don't have to do this inside a `with` statement)
    stop_listening = r.listen_in_background(m, callback)
    # `stop_listening` is now a function that, when called, stops background listening
    
    # do some other computation for 5 seconds, then stop listening and keep doing other computations
    for _ in range(50): time.sleep(0.1)  # we're still listening even though the main thread is doing other things
    stop_listening()  # calling this function requests that the background listener stop listening
    while True: time.sleep(0.1)

def parse(stuff):
    print("in")
    dict={"bad":-5,"horrible":-5,"unhappy":-5,"okay":5,"here":5,"happy":5,"hello":5}
    stuff=stuff.split()
    
    for item in stuff: 
    
        mainSubGameClass.SubGameClass.value+=dict.get(item,0)
   
#speech recognizer documentation
def micRecord():
    r=sr.Recognizer()
    with sr.Microphone() as source:
        print("Say something!")
        audio = r.listen(source)
    # try:
    #     print("Sphinx thinks you said " + r.recognize_sphinx(audio))
    # except sr.UnknownValueError:
    #     print("Sphinx could not understand audio")
    # except sr.RequestError as e:
    #     print("Sphinx error; {0}".format(e))
                
    try:
        # for testing purposes, we're just using the default API key
        # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
        # instead of `r.recognize_google(audio)`
        stuff=r.recognize_google(audio)
        parse(stuff)
        print("Google Speech Recognition thinks you said " + r.recognize_google(audio))
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))

import aubio

# #modified from https://github.com/aubio/aubio/blob/master/python/demos/demo_pitch.py
#         
# Code taken from https://github.com/aubio/aubio/issues/6
#modified for parsing
from aubio import pitch
import numpy as np
import audioop
def record(outputFile):
    
    CHUNK = 1024
    FORMAT = pyaudio.paFloat32
    CHANNELS = 1
    RATE = 44100
    RECORD_SECONDS = 60
    WAVE_OUTPUT_FILENAME = "output.wav"
    
    p = pyaudio.PyAudio()
    
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)
    
    print("* recording")
    
    frames = []
    
    # Pitch
    tolerance = 0.8
    downsample = 1
    win_s = 4096 // downsample # fft size
    hop_s = 1024  // downsample # hop size
    pitch_o = aubio.pitch("yin", win_s, hop_s, RATE)
    pitch_o.set_unit("midi")
    pitch_o.set_tolerance(tolerance)
    pitches = []
    confidences = []
    
    
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        buffer = stream.read(CHUNK)
        frames.append(buffer)
        something=audioop.rms(buffer,2)
        #1400
        if something>10:
            signal = np.fromstring(buffer, dtype=np.float32)
        
            pitch = pitch_o(signal)[0]
            confidence = pitch_o.get_confidence()
            if confidence>=0.8:
                pitches.append(pitch)
                confidences.append(confidence)
            else:
                mainSubGameClass.SubGameClass.value=0
            if len(pitches)>1:
                if abs(pitches[-1]-pitches[-2])>20 or pitch<10:
                    if mainSubGameClass.SubGameClass.value>2:
                        mainSubGameClass.SubGameClass.value-=2
                else:
                    mainSubGameClass.SubGameClass.value+=1
            print("{} / {}".format(pitch,confidence))
        else:
            mainSubGameClass.SubGameClass.value=0
    
    
    print("* done recording")
    
    #stream.stop_stream()
    #stream.close()
    #p.terminate()
    
   
            

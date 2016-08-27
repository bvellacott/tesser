#!/usr/bin/python
import pyaudio
import wave
import sys
import time, threading
import numpy
import math
import struct

formatDataType = {
    pyaudio.paFloat32: numpy.float32,
    pyaudio.paInt32: numpy.int32,
    # pyaudio.paInt24: numpy.int24,
    pyaudio.paInt16: numpy.int16,
    pyaudio.paInt8: numpy.int8,
    pyaudio.paUInt8: numpy.uint8
}

class Tesser:
    def __init__(self):
        global formatDataType

        self.chunkSize = 80

        self.informat = pyaudio.paFloat32
        self.inchannels = 1
        self.inrate = 48000
        
        self.outformat = pyaudio.paFloat32
        self.outchannels = 1
        self.outrate = 48000

        self.signalHandlers = []


    def chunkHandler(self, in_data, frame_count, time_info, status):
        raw = numpy.fromstring(in_data, dtype=formatDataType.get(self.informat))
        output = raw.copy()
        for i in xrange(len(raw)):
            for handler in self.signalHandlers:
                handler(sampleIndex=self.sampleIndex, chunkSampleIndex=i, raw=raw, output=output)
            self.sampleIndex += 1
        self.outStream.write(output.tostring())
        return (None, pyaudio.paContinue)

    def start(self):
        self.pAudio = pyaudio.PyAudio()

        self.outStream = self.pAudio.open(format=self.outformat,
                        channels=self.outchannels,
                        rate=self.outrate,
                        output=True,
                        # output_device_index=2,
                        frames_per_buffer=self.chunkSize)

        self.sampleIndex = long(0)

        self.inStream = self.pAudio.open(format=self.informat,
                        channels=self.inchannels,
                        rate=self.inrate,
                        input=True,
                        frames_per_buffer=self.chunkSize,
                        # input_device_index=2,
                        stream_callback=self.chunkHandler)

    def stop(self):
        self.inStream.stop_stream()
        self.inStream.close()
        self.outStream.stop_stream()
        self.outStream.close()
        self.pAudio.terminate()

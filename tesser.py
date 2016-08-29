import pyaudio
import numpy
import math

formatDataType = {
    pyaudio.paFloat32: numpy.float32,
    pyaudio.paInt32: numpy.int32,
    # pyaudio.paInt24: numpy.int24,
    pyaudio.paInt16: numpy.int16,
    pyaudio.paInt8: numpy.int8,
    pyaudio.paUInt8: numpy.uint8
}



class Tesser:
    def __init__(self, bufferLength=300, inrate=48000, outrate=48000):
        global formatDataType

        self.chunkSize = 80
        self.bufferLength = bufferLength
        self.bufferSize = inrate*bufferLength
        self.rawBuffer = None
        self.outputBuffer = None

        self.informat = pyaudio.paFloat32
        self.inchannels = 1
        self.inrate = inrate
        
        self.outformat = pyaudio.paFloat32
        self.outchannels = 1
        self.outrate = outrate

        self.signalHandlers = []

        self.silence = chr(0)*self.chunkSize*self.inchannels*2 


    def addToBuffer(self, raw, output):
        if self.rawBuffer is None:
            self.rawBuffer = raw
            self.outputBuffer = output
            return
        overflow = len(self.rawBuffer) - self.bufferSize
        if overflow > 0:
            self.rawBuffer = self.rawBuffer[overflow:]
            self.outputBuffer = self.outputBuffer[overflow:]
        self.rawBuffer = numpy.append(self.rawBuffer, raw)
        self.outputBuffer = numpy.append(self.outputBuffer, output)

    def chunkHandler(self, in_data, frame_count, time_info, status):
        if in_data == '':
            in_data = self.silence
        raw = numpy.fromstring(in_data, dtype=formatDataType.get(self.informat))
        output = raw.copy()
        self.addToBuffer(raw, output)
        for i in xrange(len(raw)):
            for handler in self.signalHandlers:
                handler(
                    sampleIndex= self.sampleIndex, 
                    bufferIndex=len(self.outputBuffer) - (len(raw) - i),
                    chunkIndex= i, 
                    raw= raw, 
                    output=output,
                    tesser=self)
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
        self.rawBuffer = self.outputBuffer = None
        self.inStream.stop_stream()
        self.inStream.close()
        self.outStream.stop_stream()
        self.outStream.close()
        self.pAudio.terminate()

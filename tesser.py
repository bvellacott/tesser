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

        self.chunkSize = 256
        self.bufferLength = bufferLength
        self.bufferSize = inrate*bufferLength/self.chunkSize
        self.rawBuffer = []
        self.outputBuffer = []

        self.informat = pyaudio.paFloat32
        self.inchannels = 1
        self.inrate = inrate

        self.outformat = pyaudio.paFloat32
        self.outchannels = 1
        self.outrate = outrate

        self.signalHandlers = []

        self.silence = chr(0)*self.chunkSize*self.inchannels*2


    def addToBuffer(self, raw, output):
        self.rawBuffer.append(raw)
        self.outputBuffer.append(output)
        if len(self.rawBuffer) > self.bufferSize:
            del self.rawBuffer[0]
            del self.outputBuffer[0]

    def getBufferSample(self, buffer, index):
        chunkIndex = int(index/self.chunkSize)
        sampleIndex = int(index%self.chunkSize)
        return buffer[chunkIndex][sampleIndex]

    def getRawBufferSample(self, index):
        return self.getBufferSample(self.rawBuffer, index)

    def getOutputBufferSample(self, index):
        return self.getBufferSample(self.outputBuffer, index)

    def getBufferLength(self):
        return len(self.outputBuffer)*self.chunkSize

    def chunkHandler(self, in_data, frame_count, time_info, status):
        if in_data == '':
            in_data = self.silence
        raw = numpy.fromstring(in_data, dtype=formatDataType.get(self.informat))
        output = raw.copy()
        self.addToBuffer(raw, output)
        for handler in self.signalHandlers:
            bufferIndex = self.getBufferLength() - self.chunkSize
	    sampleIndex = self.sampleIndex 
            for i in xrange(len(raw)):
                handler(
                    sampleIndex= self.sampleIndex,
                    bufferIndex= bufferIndex + 1,
                    chunkIndex= i,
                    raw= raw,
                    output=output,
                    tesser=self)
		sampleIndex += 1
	self.sampleIndex += self.chunkSize
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

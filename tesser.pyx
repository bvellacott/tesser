import threading
import pyaudio
import numpy
import math




class Tesser:
  formatDataType = {
    pyaudio.paFloat32: numpy.float32,
    pyaudio.paInt32: numpy.int32,
    # pyaudio.paInt24: numpy.int24,
    pyaudio.paInt16: numpy.int16,
    pyaudio.paInt8: numpy.int8,
    pyaudio.paUInt8: numpy.uint8
  }

  def __init__(self, bufferLength=300, rate=16000, chunkSize=160):
    self.chunkSize = 160
    self.bufferLength = bufferLength
    self.bufferSize = rate*bufferLength/self.chunkSize
    self.outputBuffer = []

    self.width = 2
    self.channels = 1
    self.rate = rate

    self.signalHandlers = []

    self.silence = chr(0)*self.chunkSize*self.channels*2
    self.lastUnread = self.silence
    self.completedChunks = [self.silence, self.silence]


  def addToBuffer(self, output):
    self.outputBuffer.append(output)
    if len(self.outputBuffer) > self.bufferSize:
      del self.outputBuffer[0]

  def getBufferSample(self, buffer, index):
    chunkIndex = int(index/self.chunkSize)
    sampleIndex = int(index%self.chunkSize)
    return buffer[chunkIndex][sampleIndex]

  def getBufferChunk(self, buffer, index):
    if index < 0 or index >= len(buffer):
      return None
    return buffer[index]

  def getPreviousChunk(self):
    return self.getBufferChunk(self.outputBuffer, len(self.outputBuffer)-2)

  def getOutputBufferSample(self, index):
    return self.getBufferSample(self.outputBuffer, index)

  def getBufferLength(self):
    return len(self.outputBuffer)*self.chunkSize

  def addCompletedChunk(self, chunk):
    self.completedChunks.append(chunk)

  def getUnreadChunk(self):
    if len(self.completedChunks) > 0:
      self.lastUnread = self.completedChunks.pop(0)
    return self.lastUnread

  def inHandler(self, in_data, frame_count=None, time_info=None, status=None):
    def chunkHandler():
      output = numpy.fromstring(in_data, dtype=self.formatDataType.get(self.format))
      self.addToBuffer(output)
      for handler in self.signalHandlers:
        bufferIndex = self.getBufferLength() - self.chunkSize
        sampleIndex = self.sampleIndex
        for i in xrange(self.chunkSize):
          handler(sampleIndex=sampleIndex,
                  bufferIndex=bufferIndex,
                  chunkIndex=i,
                  output=output,
                  tesser=self)
          sampleIndex += 1
          bufferIndex += 1
      self.sampleIndex += self.chunkSize
      self.addCompletedChunk(output.tostring())
      return
    threading.Thread(target=chunkHandler).start()
    return (self.getUnreadChunk(), pyaudio.paContinue)

  def outHandler(self, in_data, frame_count=None, time_info=None, status=None):
    if self.completedChunk is None:
      return (self.silence, pyaudio.paContinue)
    chunk = self.completedChunk
    self.completedChunk = None
    return (chunk.tostring(), pyaudio.paContinue)

  def start(self):
    self.pAudio = pyaudio.PyAudio()
    self.format = self.pAudio.get_format_from_width(self.width)
    self.sampleMax = numpy.iinfo(self.formatDataType.get(self.format)).max

    self.sampleIndex = long(0)

    self.inStream = self.pAudio.open(format=self.format,
                        channels=self.channels,
                        rate=self.rate,
                        input=True,
                        output=True,
                        frames_per_buffer=self.chunkSize,#)
                        # input_device_index=2,
                        stream_callback=self.inHandler)

#        self.inStream.start_stream()
#        self.outStream.start_stream()

#	while True:
#	    data = self.inStream.read(self.chunkSize)
#	    self.chunkHandler(data)

  def stop(self):
    #self.outputBuffer = None
    self.inStream.stop_stream()
    self.inStream.close()
    self.outStream.stop_stream()
    self.outStream.close()
    self.pAudio.terminate()


#import pyaudio
#import time

#WIDTH = 2
#CHANNELS = 2
#RATE = 44100

#p = pyaudio.PyAudio()

#def cb(in_data, frame_count, time_info, status):
#  return (in_data, pyaudio.paContinue)

#stream = p.open(format=p.get_format_from_width(WIDTH),
#                channels=CHANNELS,
#                rate=RATE,
#                input=True,
#                output=True,
#                stream_callback=cb)

#stream.start_stream()

#while stream.is_active():
#  time.sleep(0.1)

#stream.stop_stream()
#stream.close()

#p.terminate()

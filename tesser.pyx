import threading
import pyaudio
import numpy
import math

lock = threading.Lock()

class Tesser:
  formatDataType = {
    pyaudio.paFloat32: numpy.float32,
    pyaudio.paInt32: numpy.int32,
    # pyaudio.paInt24: numpy.int24,
    pyaudio.paInt16: numpy.int16,
    pyaudio.paInt8: numpy.int8,
    pyaudio.paUInt8: numpy.uint8
  }

  def __init__(self, bufferLength=300, rate=16000, chunkSize=160, inputDevice=None, outputDevice=None):
    self.inputDevice = inputDevice
    self.outputDevice = outputDevice

    self.chunkSize = chunkSize
    self.bufferLength = bufferLength
    self.bufferSize = rate*bufferLength/self.chunkSize
    self.outputBuffer = []

    self.width = 2
    self.channels = 1
    self.rate = rate

    self.signalHandlers = []
    self.chunkHandlers = []

    self.silence = chr(0)*self.chunkSize*self.channels*2
    self.lastUnread = self.silence
    self.completedChunks = []


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
    lock.acquire()
    self.completedChunks.append(chunk)
    lock.release()

  def getUnreadChunk(self):
    lock.acquire()
    if len(self.completedChunks) > 0:
      self.lastUnread = self.completedChunks.pop(0)
    lock.release()
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
      for handler in self.chunkHandlers:
        for i in xrange(self.chunkSize):
          handler(firstSampleIndex=self.sampleIndex,
                  output=output,
                  tesser=self)
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
                        input_device_index=self.inputDevice,
                        output_device_index=self.outputDevice,
                        stream_callback=self.inHandler)

    self.inStream.write(chr(0)*self.inStream.get_write_available()*self.channels*2)

  def stop(self):
    self.inStream.stop_stream()
    self.inStream.close()
    self.pAudio.terminate()

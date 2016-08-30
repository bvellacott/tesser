#!/usr/bin/python
import math

def create(delay, volume):
  def do(sampleIndex, chunkIndex, bufferIndex, output, tesser):
    echoSampleIndex = bufferIndex - delay*tesser.rate
    if echoSampleIndex < 0 or echoSampleIndex >= tesser.getBufferLength():
      return False
    sample = output[chunkIndex]
    output[chunkIndex] = output[chunkIndex] + tesser.getOutputBufferSample(echoSampleIndex) * volume
  return do

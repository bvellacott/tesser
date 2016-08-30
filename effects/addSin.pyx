#!/usr/bin/python
import math

# hZ stands for wavelength or oscillations per second -> 1 hZ will do on oscillation in one second
# volume: 0 for silent and 1 for maximum volume - anything above that won't sound like a sine wave
def create(hZ, volume):
  def do(sampleIndex, chunkIndex, bufferIndex, output, tesser):
    output[chunkIndex] += tesser.sampleMax * math.sin(math.pi*sampleIndex/(tesser.rate/(2*hZ))) * volume
  return do

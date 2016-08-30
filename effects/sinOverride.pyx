#!/usr/bin/python
import math

# hZ stands for wavelength or oscillations per second -> 1 hZ will do on oscillation in one second
def create(hZ):
  def do(sampleIndex, chunkIndex, bufferIndex, output, tesser):
    output[chunkIndex] *= math.sin(math.pi*sampleIndex/(tesser.rate/(2*hZ)))
  return do

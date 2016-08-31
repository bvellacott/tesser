#!/usr/bin/python
import math

# hZ stands for wavelength or oscillations per second -> 1 hZ will do on oscillation in one second
def create(hZ, rate):
  scalar = math.pi/(rate/(2*hZ))
  def do(sampleIndex, chunkIndex, bufferIndex, output, tesser):
    output[chunkIndex] *= math.sin(sampleIndex*scalar)
  return do

#!/usr/bin/python
import math

def create(handlers):
  def do(sampleIndex, chunkIndex, bufferIndex, output, tesser):
    for h in handlers:
      h(sampleIndex, chunkIndex, bufferIndex, output, tesser)
  return do

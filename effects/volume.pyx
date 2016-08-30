#!/usr/bin/python
import math

def create(volume):
	def do(sampleIndex, chunkIndex, bufferIndex, output, tesser):
		output[chunkIndex] *= volume
	return do

#!/usr/bin/python
import math

def create(count, delay, coefficient):
	def do(sampleIndex, chunkIndex, bufferIndex, raw, output, tesser):
		def doOne(echoIndex):
			echoSampleIndex = bufferIndex - echoIndex*delay*tesser.inrate
			# print 'echoSampleIndex : ' + str(echoSampleIndex)
			# print 'bufferIndex : ' + str(bufferIndex)
			# print 'len(tesser.outputBuffer) : ' + str(len(tesser.outputBuffer))
			# print len(tesser.outputBuffer)
			if echoSampleIndex < 0 or echoSampleIndex >= len(tesser.outputBuffer):
				return False
			sample = output[chunkIndex]
			output[chunkIndex] = output[chunkIndex] + tesser.outputBuffer[echoSampleIndex] * math.pow(coefficient, echoIndex)
			return True
		for i in range(1, count+1):
			if doOne(i) == False:
				break
	return do



#!/usr/bin/python
import sys
import numpy
import math

import tesser

sys.path.append('effects')
import echo

tesser = tesser.Tesser(300, 8000, 8	000)

# def effect(sampleIndex, chunkIndex, bufferIndex, raw, output, tesser):
#     output[chunkIndex] = output[chunkIndex] * math.cos(2*math.pi*400*sampleIndex/tesser.inrate)

# tesser.signalHandlers.append(effect)
tesser.signalHandlers.append(echo.create(5, 0.1, .5))
tesser.start()

raw_input('Press any key to exit!')

tesser.stop()

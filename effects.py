#!/usr/bin/python
import sys
import numpy
import math

import tesser

sys.path.append('effects')
import volume
import echo
import addSin
import sinOverride

tesser = tesser.Tesser(300, 8000, 80)

def effect(sampleIndex, chunkIndex, bufferIndex, output, tesser):
  output[chunkIndex] += tesser.sampleMax * math.sin(math.pi*sampleIndex/(tesser.rate/(2*200.0))) / 4

tesser.signalHandlers.append(volume.create(0.5))
tesser.signalHandlers.append(echo.create(0.2, 0.4))
tesser.signalHandlers.append(addSin.create(100, 0.5))
tesser.signalHandlers.append(sinOverride.create(400))
# tesser.signalHandlers.append(effect)
tesser.start()

raw_input('Press any key to exit!')

tesser.stop()

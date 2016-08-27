#!/usr/bin/python
import numpy
import math

#!/usr/bin/python
import tesser
import math

tesser = tesser.Tesser()

def effect(sampleIndex, chunkSampleIndex, raw, output):
    output[chunkSampleIndex] = output[chunkSampleIndex] * math.cos(2*math.pi*400*sampleIndex/tesser.inrate)

tesser.signalHandlers.append(effect)
tesser.start()

raw_input('Press any key to exit!')

tesser.stop()

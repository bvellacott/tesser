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
import aggregate

# if you are experiencing buffer underrun problems, lower the rate and/or increase the chunkSize
# decreases the rate decreases the quality and increasing the chunkSize increases the latency
rate = 16000
chunkSize = 320

tesser = tesser.Tesser(bufferLength=300, rate=rate, chunkSize=chunkSize)

tesser.signalHandlers.append(aggregate.create([
    # volume.create(0.25),
    echo.create(0.2, 0.4),
    # addSin.create(40, 0.01, rate),
    sinOverride.create(400, rate)
    ]))
tesser.start()

raw_input('Press any key to exit!')

tesser.stop()

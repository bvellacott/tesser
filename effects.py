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

tesser = tesser.Tesser(300, 8000, 800)

tesser.signalHandlers.append(aggregate.create([
    # volume.create(0.25),
    echo.create(0.2, 0.4),
    # addSin.create(20, 0.1),
    sinOverride.create(400)
    ]))
tesser.start()

raw_input('Press any key to exit!')

tesser.stop()

# tesser
A simple realtime audio effects thingy done using pyaudio

Compiled using Cython

Run: 

./effects.py 

to test the effects. Currently has a simple echo, a sine wave override and a sine wave add effect. Have a look at the .pyx files in the effects directories to see how to implement an effect and look at the effects.py file to see how to put an effect into use. Currently everything relevant (tesser.pyx and the effects) has been compiled using Cython for performance. If you have Cython installed, you can compile for example tesser.pyx like so:

./cyt tesser.pyx build_ext --inplace

if you want to compile an effect like say the echo, which resides in the effects directory, you can do it like so:

cd effects
../cyt tesser.pyx build_ext --inplace

have fun!

# musicolor
A console-based tool to analyse photo albums and summarise their atmosphere by extracting colors and music out of it.

## Features
 - creates a banded 1:5 image, where each band represents the median color of the respective image
 - generates a piano music file (.wav) based on the occuring colors and constrasts in the album
   - the higher the overall color differences, the faster will the music's pace be
   - every image's median color results in a tone
   - the brighter the image, the higher the tone's octave
   - if more than two tones are evaluated consecutively, only the first two are considered in order to avoid repitition
   
## Dependencies
This program requires the python imaging library (_PIL_), _numpy_ as well as _pysynth_b_.

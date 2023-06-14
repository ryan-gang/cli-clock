# A simple CLI clock.
Written in pure python, no external dependencies. Tested on windows only.
Script also uses `[msvcrt](https://docs.python.org/3/library/msvcrt.html)` module, so might not work properly on unix systems. 

## Usage.
Repeat timer for 5 minutes, 10 times with sound
`py -m clock -r 10 300 1`
Timer for 10 seconds with sound
`py -m clock -t 10 1`
Stopwatch
`py -m clock -s`
Stopwatch can be paused (p), unpaused (p), and quit (q).
Alarm clock for 3:40 PM with sound
`py -m clock -a 15 40 1`

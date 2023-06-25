# A simple CLI clock.
## Intro.
A CLI clock packahe, written in pure python, with no external dependencies. Depends on [msvcrt](https://docs.python.org/3/library/msvcrt.html) module, (so might not work properly on unix systems.)  
Useful to work following the `Rational Breaks` methodology.  
Re : https://www.lesswrong.com/posts/RWu8eZqbwgB9zaerh/

The clock, keeps track of total work and break times (`s`), keeps track of accumulated breaks (`b`). Long breaks can be taken, which don't count towards the ratio (`B`). It can also keep a track of what task was done in which `session` (`i`). 
## Usage.
Help  
`py -m clock -h`  
Repeat timer for 300 seconds, 5 times with an alarm at the end.  
`py -m clock -r 5 300 1`  
Timer for 10 seconds with an alarm at the end.  
`py -m clock -t 10 1`  
Alarm clock for 3:40 PM with an alarm at the end.  
`py -m clock -a 15 40 1`  
Stopwatch  
`py -m clock -s`  

Stopwatch flags :   
- `p` : Pause and unpause, between sessions.  
- `s` : Get total cumulative stats.  
- `i` : Enter task details.  
Task details expected in `session_id -> task_details` format. Multiple key-value pairs can be passed seperated by a comma. 
- `t` : Show task details.  
- `b` : Get accumulated break time.  
- `B` : Start long break.  
Doesn't count towards total break time.
- `q` : Stop watch.  

Note : These flags are not passed while starting the stopwatch. These are passed while it is running.
## Installation.
### Clone and install. 
1. Git clone the repo.
2. Create a venv, and activate it.
3. `pip install .` in the parent directory.

### Directly install from repo.  
`py -m pip install git+https://github.com/ryan-gang/cli-clock.git`
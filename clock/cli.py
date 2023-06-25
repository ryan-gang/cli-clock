import argparse
import sys

from clock import Clock
from stopwatch import Stopwatch

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Simple CLI Clock")
    parser.add_argument(
        "--timer",
        "-t",
        metavar=("SECONDS", "SOUND_BOOL"),
        nargs=2,
        type=int,
        help="Set a timer for a specified number of seconds, and play an alarm at the end.",
    )
    parser.add_argument(
        "--repeat",
        "-r",
        metavar=("REPEATS", "SECONDS", "SOUND_BOOL"),
        nargs=3,
        type=int,
        help=(
            "Set a timer for 'SECONDS' number of seconds, that repeats 'REPEATS' times, and plays"
            " an alarm at the end. If 'REPEATS' is negative, it would repeat infinitely."
        ),
    )

    parser.add_argument(
        "--stopwatch",
        "-s",
        action="store_true",
        help=(
            "Start a stopwatch. The stopwatch supports pause (p), unpause (p) and quit (q)"
            " commands."
        ),
    )
    parser.add_argument(
        "--alarm",
        "-a",
        metavar=("HOUR", "MINUTE", "SOUND_BOOL"),
        nargs=3,
        type=int,
        help="Set an alarm for a specific time (24-hour format).",
    )
    args = parser.parse_args()

    clock = Clock()
    stopwatch = Stopwatch()
    if args.timer:
        clock.start_timer(args.timer[0], args.timer[1])
    elif args.stopwatch:
        stopwatch.start_stopwatch()
    elif args.alarm:
        clock.alarm(args.alarm[0], args.alarm[1], args.alarm[2])
    elif args.repeat:
        clock.repeat_timer(args.repeat[0], args.repeat[1], args.repeat[2])
    else:
        sys.exit()

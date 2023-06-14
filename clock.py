import argparse
import msvcrt
import threading
import time
import winsound
import sys


class ThreadedAlarm(threading.Thread):
    def __init__(self, hours: int, minutes: int, sound: bool):
        self.alarm_time: tuple[int, int] = (hours, minutes)
        self.sound = sound
        self.notification_tone: str = r"assets/subtle_beeps.wav"

    def alarm(self):
        while True:
            # Check if it's time for the alarm
            now = time.localtime()
            if now.tm_hour == self.alarm_time[0] and now.tm_min == self.alarm_time[1]:
                print("Alarm!")
                if self.sound:
                    winsound.PlaySound(self.notification_tone, winsound.SND_ALIAS)
                return

            # Wait for one second
            time.sleep(1)


class Clock:
    """
    Simple clock class, implementing alarms, stopwatch and a timer.
    """

    def __init__(self):
        self.timer_on: bool = False
        self.stopwatch_on: bool = False
        self.notification_tone: str = r"assets/subtle_beeps.wav"

    def repeat_timer(self, times: int, duration: int, sound: bool):
        ran = 0
        try:
            while times:
                self.start_timer(duration, sound)
                times -= 1
                ran += 1
        except (KeyboardInterrupt, Exception):
            print(f"Timer for {duration} seconds, ran for {ran} times.")

    def start_timer(self, duration: int, sound: bool):
        # duration in seconds.
        self.timer_on = True
        start_time = time.time()
        end_time = start_time + duration
        while time.time() <= end_time:
            remaining_time = end_time - time.time()
            print(f"Remaining time: {remaining_time:.2f} seconds\r", end="")
            time.sleep(0.1)
        self.timer_on = False
        print("\rTimer complete.                                          ")
        if sound:
            winsound.PlaySound(self.notification_tone, winsound.SND_FILENAME)

    def start_stopwatch(self):
        self.stopwatch_on, paused, paused_at = True, False, 0
        start_time = time.time()
        while self.stopwatch_on:
            while not msvcrt.kbhit() and not paused:
                elapsed_time = time.time() - start_time
                print("Elapsed time:", self.generate_time_string(elapsed_time), end="")

            cmd = msvcrt.getch().decode("utf-8")
            if cmd == "p":  # Pause
                paused ^= True  # Toggle Pause
                if paused:
                    paused_at = time.time()
                    print("\nPaused.\t", end="")
                else:
                    elapsed = time.time() - paused_at
                    print(f"Resumed after {self.generate_time_string(elapsed).strip()}.")
            elif cmd == "q":  # Quit
                self.stop_stopwatch()
                print("\n")
                break
            else:
                continue
            time.sleep(0.1)

    def generate_time_string(self, elapsed_time: float) -> str:
        if elapsed_time < 60:
            string = f"{elapsed_time:.2f} seconds\r"
        elif elapsed_time < 60 * 60:
            string = f"{elapsed_time//60:.2f} minutes {elapsed_time%60:.2f} seconds\r"
        else:
            string = (
                f"{elapsed_time // (60*60):.2f} hours"
                f" {elapsed_time % (60 * 60) // 60:.2f} minutes"
                f" {elapsed_time % (60 * 60) % 60:.2f} seconds\r"
            )
        return string

    def stop_stopwatch(self):
        self.stopwatch_on = False

    def alarm(self, hours: int, minutes: int, sound: bool):
        try:
            t = ThreadedAlarm(hours=hours, minutes=minutes, sound=sound)
            t.start()
        except (KeyboardInterrupt, Exception):
            print(f"Alarm is still on for {hours}:{minutes}.")


if __name__ == "__main__":
    """
    Usage :
    Repeat timer for 5 minutes, 10 times with sound : py -m clock -r 10 300 1
    Timer for 10 seconds with sound : py -m clock -t 10 1
    Stopwatch : py -m clock -s
    Stopwatch can be paused (p), unpaused (p), and quit (q).
    Alarm clock for 3:40 PM with sound : py -m clock -a 15 40 1
    """
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

    if args.timer:
        clock.start_timer(args.timer[0], args.timer[1])
    elif args.stopwatch:
        clock.start_stopwatch()
    elif args.alarm:
        clock.alarm(args.alarm[0], args.alarm[1], args.alarm[2])
    elif args.repeat:
        clock.repeat_timer(args.repeat[0], args.repeat[1], args.repeat[2])
    else:
        sys.exit()

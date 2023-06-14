import argparse
import threading
import time
import winsound


class ThreadedAlarm(threading.Thread):
    def __init__(self, hours: int, minutes: int, sound: bool):
        super().__init__()
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
        except KeyboardInterrupt or Exception:
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
        self.stopwatch_on = True
        start_time = time.time()
        flag = 1
        try:
            while self.stopwatch_on:
                elapsed_time = time.time() - start_time
                if elapsed_time < 60:
                    string = f"Elapsed time: {elapsed_time:.2f} seconds\r"
                    print(string, end="")
                elif elapsed_time < 60 * 60:
                    flag = 2
                    string = (
                        f"Elapsed time: {elapsed_time//60:.2f} minutes"
                        f" {elapsed_time%60:.2f} seconds\r"
                    )
                    print(string, end="")
                else:
                    flag = 3
                    string = (
                        f"Elapsed time: {elapsed_time // (60*60):.2f} hours"
                        f" {elapsed_time % (60 * 60) // 60:.2f} minutes"
                        f" {elapsed_time % (60 * 60) % 60:.2f} seconds\r"
                    )
                    print(string, end="")
                time.sleep(0.1)
        except KeyboardInterrupt or Exception:
            self.stop_stopwatch()
            print(string)

    def stop_stopwatch(self):
        self.stopwatch_on = False

    def alarm(self, hours: int, minutes: int, sound: bool):
        try:
            t = ThreadedAlarm(hours=hours, minutes=minutes, sound=sound)
            t.start()
        except KeyboardInterrupt or Exception:
            print(f"Alarm is still on for {hours}:{minutes}.")


if __name__ == "__main__":
    """
    Usage :
    Repeat timer for 5 minutes, 10 times with sound : py -m clock -r 10 300 1
    Timer for 10 seconds with sound : py -m clock -t 10 1
    Stopwatch : py -m clock -s
    Alarm clock for 3:40 PM with sound : py -m clock -a 15 40 1
    """
    parser = argparse.ArgumentParser(description="CLI Clock")
    parser.add_argument(
        "--timer",
        "-t",
        metavar=("SECONDS", "SOUND_BOOL"),
        nargs=2,
        type=int,
        help="Set a timer for a specified number of seconds",
    )
    parser.add_argument(
        "--repeat",
        "-r",
        metavar=("REPEATS", "SECONDS", "SOUND_BOOL"),
        nargs=3,
        type=int,
        help=(
            "Set a timer for a specified number of seconds, that repeats after the seconds are over"
        ),
    )

    parser.add_argument("--stopwatch", "-s", action="store_true", help="Use stopwatch mode")
    parser.add_argument(
        "--alarm",
        "-a",
        metavar=("HOUR", "MINUTE", "SOUND_BOOL"),
        nargs=3,
        type=int,
        help="Set an alarm for a specific time (24-hour format)",
    )
    args = parser.parse_args()

    clock = Clock()

    if args.timer:
        clock.start_timer(args.timer[0], args.timer[1])

    if args.stopwatch:
        clock.start_stopwatch()
        clock.stop_stopwatch()

    if args.alarm:
        clock.alarm(args.alarm[0], args.alarm[1], args.alarm[2])

    if args.repeat:
        clock.repeat_timer(args.repeat[0], args.repeat[1], args.repeat[2])

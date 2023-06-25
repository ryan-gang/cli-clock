import threading
import time
import winsound

TOLERANCE = 1  # seconds


class Alarm:
    def __init__(self, hours: int, minutes: int, sound: bool):
        self.alarm_time: tuple[int, int] = (hours, minutes)
        self.sound = sound
        self.notification_tone: str = r"assets/subtle_beeps.wav"

    def alarm(self):
        while True:
            # Check if it's time for the alarm
            print("Waiting ... \r", end="")
            now = time.localtime()
            if now.tm_hour == self.alarm_time[0] and now.tm_min == self.alarm_time[1]:
                print("\nAlarm!")
                if self.sound:
                    for _ in range(3):
                        winsound.PlaySound(self.notification_tone, winsound.SND_ALIAS)
                return

            # Wait for one second
            time.sleep(TOLERANCE)


class Clock:
    """
    Simple clock class, implementing alarms and a timer.
    """

    def __init__(self):
        self.timer_on: bool = False
        self.stopwatch_on: bool = False
        self.notification_tone: str = r"assets/subtle_beeps.wav"

    def alarm(self, hours: int, minutes: int, sound: bool):
        a = Alarm(hours, minutes, sound)
        x = threading.Thread(target=a.alarm(), daemon=True)
        x.start()

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
            time.sleep(TOLERANCE)
        self.timer_on = False
        print("\rTimer complete.                                          ")
        if sound:
            winsound.PlaySound(self.notification_tone, winsound.SND_FILENAME)

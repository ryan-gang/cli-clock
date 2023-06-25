import msvcrt
import time
from collections import defaultdict
from commons import Commons

TOLERANCE = 1  # seconds


class Stopwatch:
    """
    Options :
    p : Pause and unpause, between sessions.
    s : Get total cumulative stats.
    b : Get accumulated break time.
    B : Start long break.
    q : Stop watch.
    """

    def __init__(self):
        self.stopwatch_on: bool = False
        self.c = Commons()
        self.d: dict[int, list[str]] = defaultdict(list)
        self.ratio = 3  # Rational breaks ratio : 1/ 3

    def start_stopwatch(self):
        self.stopwatch_on, self.paused, paused_at = True, False, 0.0
        start_time = time.time()
        elapsed_time = self.total_work = self.total_break = 0
        print("STOPWATCH MODE.")
        print(f"Started at : {self.c.get_timestamp()}")
        while self.stopwatch_on:
            while not msvcrt.kbhit() and not self.paused:
                elapsed_time = time.time() - start_time
                print(f"Work Session : {self.c.generate_time_string(elapsed_time)}", end="")
                # print("Elapsed time:", self.c.generate_time_string(elapsed_time), end="")
                time.sleep(TOLERANCE)

            cmd = msvcrt.getch().decode("utf-8")
            if cmd == "p" or cmd == "B":  # Pause or Long Break
                # Long Breaks will not count toward break quota.
                self.paused ^= True  # Toggle Pause
                if self.paused:
                    paused_at = time.time()
                    work_duration = paused_at - start_time
                    if cmd == "p":
                        print(
                            f"Paused at : {self.c.get_timestamp()}, Work :"
                            f" {self.c.generate_time_string(work_duration).strip()}."
                        )
                    elif cmd == "B":
                        print(
                            f"LONG BREAK STARTED : {self.c.get_timestamp()}, Work :"
                            f" {self.c.generate_time_string(work_duration).strip()}."
                        )
                    self.total_work += work_duration
                    start_time += work_duration
                else:
                    break_duration = time.time() - paused_at
                    start_time += break_duration
                    if cmd == "p":
                        self.total_break += break_duration
                        # Or else stopwatch would count the entire time, including
                        # the time it was paused for.
                        print(
                            f"Restarted at : {self.c.get_timestamp()}, Break :"
                            f" {self.c.generate_time_string(break_duration).strip()}."
                        )
                    elif cmd == "B":
                        print(
                            "Long break duration :"
                            f" {self.c.generate_time_string(break_duration).strip()}"
                        )
                        print(f"Restarted at : {self.c.get_timestamp()}.")
            elif cmd == "q":  # Quit
                print(f"Stopped at : {self.c.get_timestamp()}")
                print(self.get_stats(elapsed_time, paused_at))
                self.stop_stopwatch()
                print("\n")
                break
            elif cmd == "s":  # Stats
                self.print_clean(self.get_stats(elapsed_time, paused_at), end="\r")
            elif cmd == "b":  # Break status
                self.print_clean(self.get_break_status(elapsed_time, paused_at), end="\r")
            elif cmd == "i":
                _ = input("Enter data : ")
                self.remove_input_data_and_line()
            else:
                continue

    def stop_stopwatch(self):
        self.stopwatch_on = False

    def get_stats(self, current_elapsed: float, paused_at: float) -> str:
        tw, tb = self.total_work, self.total_break
        if current_elapsed:
            tw += current_elapsed
        if self.paused:
            tb += time.time() - paused_at
        return (
            f"STATS : Total work : {self.c.generate_time_string(tw).strip()}, Total"
            f" break : {self.c.generate_time_string(tb).strip()}"
        )

    def get_break_status(self, current_elapsed: float, paused_at: float) -> str:
        tw, tb = self.total_work, self.total_break
        if current_elapsed:
            tw += current_elapsed
        if self.paused:
            tb += time.time() - paused_at
        tb = self.total_break
        ab = tw // self.ratio
        ab -= tb
        if ab <= 0:
            return "No break time left."
        return f"Acc Break time : {self.c.generate_time_string(ab)}"

    def wait_and_flush(self) -> None:
        time.sleep(TOLERANCE * 5)
        print(" " * 100, end="\r")

    def print_clean(self, *args: str, end: str = "\n"):
        print(*args, end=end)
        self.wait_and_flush()

    def remove_input_data_and_line(self):
        # The \033 is the escape character. The [1A says go up one line and the
        # [K says erase to the end of this line.
        print("\033[1A" + "\033[K", end="\r")

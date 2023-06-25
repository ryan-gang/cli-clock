import time
from datetime import datetime

TOLERANCE = 1  # seconds


class Commons:
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

    def get_timestamp(self) -> str:
        ts = time.time()
        return datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M:%S")

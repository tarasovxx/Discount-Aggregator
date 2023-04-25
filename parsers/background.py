import time
from threading import Thread
import schedule


def task_runner(function):
    schedule.every().day.do(function)
    while True:
        schedule.run_pending()
        time.sleep(60)

def start_schedule():
    t = Thread(target=task_runner)
    t.start()
import math
import time
import datetime as dt
import pyttsx3

ENGINE = pyttsx3.init()
NOTIFICATIONS = []


def alert_user(task):
    """ Prints out task. Adds finished tasks sto notifications. Runs pyttsx3 for text to speech and says 'task'. """
    print('Finished task: ' + task)
    NOTIFICATIONS.append(task)
    print('List of finished tasks: ')
    print(NOTIFICATIONS)
    try:
        ENGINE.say(task)
        ENGINE.runAndWait()
        ENGINE.endLoop()
    except Exception:
        pass


def date_diff_in_seconds(date_two, date_one):
    """ Calculate the amount of seconds between two dates. """
    timedelta = date_two - date_one
    return timedelta.days * 24 * 60 * 60 + timedelta.seconds


def add_alarm(s, date, hhmmss, task):
    """ Adds alarm to the scheduler. Also calculates the delay in seconds needed between specific dates and passes
    that to the scheduler. """
    try:
        date1 = dt.datetime.strptime(date + ' ' + hhmmss, '%Y-%m-%d %H:%M:%S')
        date2 = dt.datetime.now()
        delay_in_seconds = date_diff_in_seconds(date1, date2)
        s.enter(delay_in_seconds, 1, alert_user, (task,))
    except IndexError:
        pass


def remove_alarm(sch, date, hhmmss):
    """  Compares the time part of events in scheduler and cancels the chosen event according to time. """
    date_time = dt.datetime(int(date[:4]), int(date[-5:7]), int(date[-2:]), int(hhmmss[:2]), int(hhmmss[-5:5]))
    date_time_in_sec = int(time.mktime(date_time.timetuple()))
    # print(date_time_in_sec)
    for event in sch.queue:
        if math.ceil(event.time) == date_time_in_sec:
            try:
                # print(math.ceil(event.time))
                sch.cancel(event)
            except ValueError:
                print('Error')


# ---TESTING FOR add_alarm() and remove_alarm()---
# scheduler = sched.scheduler(time.time, time.sleep)
# add_alarm(scheduler, '2019-11-18', '23:09:00', 'Eat stuff')
# add_alarm(scheduler, '2019-11-18', '23:10:00', 'Eat cabbage')
# print(LIST_OF_ALARMS)
# remove_alarm(scheduler, '2019-11-18', '23:09:00')
# print(LIST_OF_ALARMS)

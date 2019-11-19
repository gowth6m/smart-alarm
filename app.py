import sched
import time
import alarm
from flask import Flask, render_template, request
from threading import Thread


scheduler = sched.scheduler(time.time, time.sleep)

app = Flask(__name__)

list_of_alarms = []
list_of_tasks = []


@app.route('/')
def home():
    """ Gets data from URL in browser and uses add_alarm() to pass date, time & task to the scheduler. Also passes
    back list of alarms and list of tasks back to the browser. """
    date_time = request.args.get('date_time')
    task = request.args.get('task')
    try:
        date_time = date_time.replace('T', ' ')
        set_date = date_time[:10]
        set_time = date_time[-5:] + ':00'
        list_of_alarms.append(date_time)
        list_of_tasks.append(task)
        # print(list_of_alarms)
        # print(list_of_tasks)
        alarm.add_alarm(scheduler, set_date, set_time, task)
    except AttributeError:
        pass
    return render_template('index.html', date_time_info=list_of_alarms, task_info=list_of_tasks)


def run_sch_thread(sch):
    """ Checks for scheduler queue every 1 second and runs it. """
    while True:
        if len(sch.queue) == 0:
            time.sleep(1)
        else:
            sch.run()


if __name__ == '__main__':
    t = Thread(target=run_sch_thread, args=(scheduler,))
    t.start()
    app.run()

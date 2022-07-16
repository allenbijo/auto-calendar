import csv
import pickle
from datetime import date as dt
from datetime import timedelta as td


def fmin(t):
    h = int(t[:2])
    m = int(t[3:])
    return int((h * 60 + m) / 5)


def scheduler(m):
    with open("Times.csv") as t:
        cv = csv.reader(t)
        time = [i for i in cv if i not in [[], ['', '']]]

    with open("daySchedule.csv") as f:
        cv = csv.reader(f)
        sched = [i for i in cv if i not in [[], ['', '']]]

    day = dt.weekday(dt.today() + td(days=m))

    try:
        with open("preferences.dat", 'rb') as k:
            tasks = pickle.load(k)
    except:
        print('Please add preferences')

    tasks.sort(key=lambda tasks: tasks[5], reverse = True)

    start = {}
    todaytask = []

    for task in tasks:
        if task[4][day] == '1':
            todaytask.append(task)
            for i in range(fmin(task[1]), fmin(task[2])):
                for j in range(i, i + fmin(task[3])):
                    if sched[j][1] != 'None':
                        break
                else:
                    start[task[0]] = i
                    for j in range(fmin(task[3])):
                        time[start[task[0]] + j][1] = task[0]
                        sched[start[task[0]] + j][1] = task[0]
                    break
    with open('updayschedule.csv', 'w') as up:
        cs = csv.writer(up)
        cs.writerows(time)

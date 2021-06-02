import random
import pylab
import math

"""edf"""


class Task:
    def __init__(self, time, la):
        self.time_to_solve = MX
        self.deadline = random.randint(2, MAX_K) * self.time_to_solve
        self.appearing_time = time - 1 / la * math.log(random.random())


def get_new_task(t):
    ret = 0

    for i in range(len(queue)):
        if getattr(queue[i], "deadline") < getattr(queue[ret], "deadline") and t > getattr(queue[i], "appearing_time"):
            ret = i
    return queue.pop(ret)


def last_appeared_element(t):
    return getattr(queue[-1], "appearing_time") if len(queue) != 0 and getattr(queue[-1], "appearing_time") > t else t


response_to_lambda = []
LAMBDA_COUNT = 100
MAX_K = 5
task_made_by_025 = []
sleep_to_lambda = []
MX = 3
lambda_list_x_for_plot = []
MODEL_TIME = 10000
tasks_in_time = []

for lam_scale in range(1, LAMBDA_COUNT + 1, 1):
    lam = 0.01 * lam_scale

    T = 0
    queue = []
    response_time = []
    sleep = 0

    task = Task(0, lam)
    task.appearing_time = 0.0
    while T < MODEL_TIME:
        if T < getattr(task, "appearing_time"):
            sleep += getattr(task, "appearing_time") - T
            T = getattr(task, "appearing_time")

        if T < getattr(task, "appearing_time") + getattr(task, "deadline"):
            if T + getattr(task, "time_to_solve") < getattr(task, "appearing_time") + getattr(task, "deadline"):
                response_time.append(T - getattr(task, "appearing_time"))
                if lam == 0.25:
                    task_made_by_025.append(T - task.appearing_time)
                T += getattr(task, "time_to_solve")
            else:
                T += getattr(task, "appearing_time") + getattr(task, "deadline") - T

        while T > last_appeared_element(getattr(task, "appearing_time")):
            queue.append(Task(last_appeared_element(getattr(task, "appearing_time")), lam))
            if lam == 0.25:
                tasks_in_time.append(getattr(queue[-1], "appearing_time"))
        task = get_new_task(T)

    lambda_list_x_for_plot.append(lam)
    response_to_lambda.append(sum([i for i in response_time]) / len(response_time))
    sleep_to_lambda.append(sleep)

    print('\r{}%'.format(lam_scale), end='')
    if lam_scale == LAMBDA_COUNT:
        print()
pylab.plot(lambda_list_x_for_plot, response_to_lambda)
pylab.xlabel('lambda')
pylab.ylabel('average response time')
pylab.show()
pylab.plot(lambda_list_x_for_plot, sleep_to_lambda)
pylab.xlabel('lambda')
pylab.ylabel('sleep time')
pylab.show()

GROUP = 100
bar_x = [0]
for i in range(len(tasks_in_time)):
    if tasks_in_time[i] < GROUP * (len(bar_x)):
        bar_x[-1] += 1
    else:
        bar_x.append(1)

pylab.plt.bar(tasks_in_time, [1 for i in range(len(tasks_in_time))], align='center', alpha=1)
pylab.plt.show()

pylab.plt.bar([i for i in range(len(bar_x))], bar_x, align='center', alpha=1)
pylab.plt.show()

task_made_by_025.sort()
tmp = [0]
for i in range(len(task_made_by_025)):
    if task_made_by_025[i] < len(tmp):
        tmp[-1] += 1
    else:
        tmp.append(0)

pylab.plot([i for i in range(len(tmp))], tmp)
pylab.xlabel('response time')
pylab.ylabel('tasks')
pylab.show()

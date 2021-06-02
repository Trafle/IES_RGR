
import math
import random
import pylab
"""RM"""


class Task:
    def __init__(self, time, lampd):
        self.time_to_solve = MX
        self.appearing_time = time - 1 / lampd * math.log(random.random())
        self.deadline = random.randint(2, MAX_K) * self.time_to_solve
        self.priority = random.choice([1, 2, 3])
        self.reaction = None
        self.time_after_break = self.appearing_time

    def get_appeartime(self):
        return self.appearing_time

    def get_solvetime(self):
        return self.time_to_solve

    def get_deadline(self):
        return self.deadline

    def get_priority(self):
        return self.priority

    def get_break_time(self):
        return self.time_after_break


def find_last_appeared_time(t):
    return queue[-1].get_appeartime() if len(queue) != 0 and queue[-1].get_appeartime() > t else t


def get_new_task(t):
    ret = 0
    for i in range(len(queue)):
        if queue[i].get_deadline() < queue[ret].get_deadline() and t > queue[i].get_appeartime():
            ret = i
    return queue.pop(ret)


def choose_next_task():
    ret = 0
    if len(queue) == 1:
        pass
    else:
        min_deadline = queue[0].get_deadline()
        for i in range(len(queue)):
            if queue[i].get_deadline() < min_deadline:
                min_deadline = queue[i].get_deadline()
                ret = i
    return ret


def check_if_break():
    if task.get_deadline() > queue[-1].get_deadline():
        return True
    else:
        return False


def break_curr_task():
    task.time_to_solve /= 2



MAX_K = 3
MX = 3
MODEL_TIME = 10000
AMOUNT_OF_LAMBDA = 100
lambda_list_x_for_plot = []
response_to_lambda = []
sleep_to_lambda = []
tasks_in_time = []
task_made_by_025 = []

for scale_lambda in range(1, AMOUNT_OF_LAMBDA+1, 1):
    lampda = 0.01 * scale_lambda

    T = 0
    queue = [Task(0, lampda)]
    response_time = []
    sleep = 0

    queue[0].appearing_time = 0.0
    while T < MODEL_TIME:
        task = queue.pop(choose_next_task())
        if T < task.get_appeartime():  # простой процесора
            sleep += task.get_appeartime() - T
            T = task.get_appeartime()

        if task.reaction is None:  # формирование след задачи
            task.reaction = T - task.get_appeartime()
            next_task = task.get_appeartime() - 1 / lampda * math.log(random.random())
            queue.append(Task(task.get_appeartime(), lampda))
            if check_if_break():
                break_curr_task()
                queue.append(task)
                continue
            if lampda == 0.25:
                tasks_in_time.append(queue[-1].get_appeartime())

        if task.get_solvetime() > task.get_deadline() or task.get_break_time() > task.get_appeartime():  # задача прерывеается
            task.time_to_solve = task.get_solvetime() - task.get_break_time()
            task.time_after_break = T + task.get_break_time()

            if task.reaction is None:  # время реакции
                task.reaction = T - task.get_appeartime()

            T += task.get_deadline()
            queue.append(task)
            if check_if_break():
                break_curr_task()
                queue.append(task)
                continue

        elif task.get_solvetime() <= task.get_deadline() and T - task.get_appeartime() + task.get_solvetime() < task.get_deadline():  # задача выполнится
            if lampda == 0.25:
                task_made_by_025.append(T - task.appearing_time)
            T += task.get_solvetime()
            response_time.append(task.reaction)

        elif T - task.get_break_time() < task.get_deadline():  # потеряное время из за наступления дедлайга
            T += task.get_deadline() - (T - task.get_break_time())

    lambda_list_x_for_plot.append(lampda)
    #print(len(response_time))
    #print(response_time)
    if len(response_time) != 0:
        response_to_lambda.append(sum([i for i in response_time]) / len(response_time))
    else:
        response_to_lambda.append(0)
    sleep_to_lambda.append(sleep)

    print('\r{}%'.format(scale_lambda), end='')
    if scale_lambda == AMOUNT_OF_LAMBDA:
        print()


pylab.plot(lambda_list_x_for_plot, response_to_lambda)
pylab.xlabel('lambda')
pylab.ylabel('average response time')
pylab.show()
pylab.plot(lambda_list_x_for_plot, sleep_to_lambda)
pylab.xlabel('lambda')
pylab.ylabel('sleep time')
pylab.show()

bar_x = [0]
GROUP = 100
for i in range(len(tasks_in_time)):
    if tasks_in_time[i] < GROUP*(len(bar_x)):
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


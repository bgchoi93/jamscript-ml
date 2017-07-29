import queue


class TaskQueue(queue.Queue):

    def __init__(self):
        super(TaskQueue, self).__init__()
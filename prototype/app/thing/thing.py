from prototype.app.thing.stream.destination.destination_stream import DestinationStream
from prototype.app.thing.stream.source.source_stream import SourceStream
from prototype.app.thing.storage.storage import Storage
from prototype.app.thing.taskqueue.task import Task
from prototype.app.thing.taskqueue.task_queue import TaskQueue
from prototype.app.thing.neuron.feed_forward_neuron import FeedForwardNeuron

import collections


class Thing:
    def __init__(self):
        self.__destination_stream = DestinationStream()
        self.__source_stream = SourceStream()
        self.__task_queue = TaskQueue()
        self.__storage = Storage("localhost", 6379, 0)

    #  replace this with REST call
    def assign_new_task(self, neuron_id, inputs):
        task = Task(neuron_id, inputs)
        self.__task_queue.put(task)

    #  TODO: replace this with RabbitMQ message queue
    def send_result(self, result):
        print("sending result: ")
        print(result["neuron_id"])
        print(result["output"])
        return self.__destination_stream.put(result)

    def compute_next_task(self):
        #  retrieve next task
        task = self.__task_queue.get()

        #  define neuron
        id = task.get_neuron_id()

        inputs = list(map(lambda x: float(x), task.get_inputs()))

        weights_dict = collections.OrderedDict(self.__storage.connection.hgetall("L1." + task.get_neuron_id()))
        del weights_dict["bias"]

        weights = []
        for key, value in weights_dict.items():
            weights.append(float(value))

        bias = float(self.__storage.connection.hget("L1." + task.get_neuron_id(), "bias"))

        neuron = FeedForwardNeuron(id, inputs, weights, bias)

        #  return computed result to destination stream
        return {"neuron_id": neuron.get_neuron_id(), "output": neuron.calculate()}


def main():
    thing = Thing()

    thing.assign_new_task("N0", ["0.3", "0.7", "0.4"])
    result = thing.compute_next_task()
    print(thing.send_result(result))

if __name__ == "__main__":
    main()
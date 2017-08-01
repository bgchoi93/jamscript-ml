from collections import OrderedDict

from prototype.app.thing.model.neuron.feed_forward_neuron import FeedForwardNeuron
from prototype.app.thing.model.storage.storage import Storage
from prototype.app.thing.model.taskqueue.task import Task
from prototype.app.thing.model.taskqueue.task_queue import TaskQueue

from prototype.app.thing.model.stream.destination.destination_stream import DestinationStream
from prototype.app.thing.model.stream.source.source_stream import SourceStream

class Thing:
    def __init__(self):
        self.__destination_stream = DestinationStream()
        self.__source_stream = SourceStream()
        self.__storage = Storage("localhost", 6379, 0)


    def get_destination_stream(self):
        return self.__destination_stream


    def get_source_stream(self):
        return self.__source_stream


    def get_storage(self):
        return self.__storage


    def assign_new_task(self, neuron_id, inputs):
        task = Task(neuron_id, inputs)
        self.__source_stream.put(task)


    def compute_next_task(self):
        if self.__source_stream.empty():
            return False
        else:
            #  retrieve next task
            task = self.__source_stream.get()

            #  define neuron
            id = task.get_neuron_id()

            inputs = list(map(lambda x: float(x), task.get_inputs()))

            weights_dict = OrderedDict(self.__storage.connection.hgetall("L1." + task.get_neuron_id()))
            del weights_dict["bias"]

            weights = []
            for key, value in weights_dict.items():
                weights.append(float(value))

            bias = float(self.__storage.connection.hget("L1." + task.get_neuron_id(), "bias"))

            neuron = FeedForwardNeuron(id, inputs, weights, bias)

            #  return computed result to destination stream
            self.__destination_stream.put({"neuron_id": neuron.get_neuron_id(), "output": neuron.calculate()})
            return True

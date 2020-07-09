from multiprocessing import Queue
from .Workers import Workers


class Communicator:

    def __init__(self):

        super().__init__()

        self._queues = [Queue() for _ in Workers]

    def broadcast(self, message):

        for q in self._queues[1:]:
            q.put(message)

    def send(self, target, message):

        if not isinstance(target, Workers):
            raise TypeError('target must be a member of Workers')

        self._queues[target].put(message)

    def receive(self, worker, block=True):

        if not isinstance(worker, Workers):
            raise TypeError('worker must be a member of Workers')

        return self._queues[worker].get(block)

    def iterate(self, worker):

        if not isinstance(worker, Workers):
            raise TypeError('worker must be a member of Workers')

        return iter(self._queues[worker].get, None)

    def empty(self, worker):

        if not isinstance(worker, Workers):
            raise TypeError('worker must be a member of Workers')

        return self._queues[worker].empty()


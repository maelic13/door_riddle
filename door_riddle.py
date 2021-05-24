from multiprocessing import cpu_count, Pool
from random import randrange
from time import time
from typing import Iterable


class Counter:
    def __init__(self) -> None:
        self.correct = 0
        self.incorrect = 0

    def add(self, success: bool) -> None:
        if success:
            self.correct += 1
        else:
            self.incorrect += 1

    def update(self, counter: 'Counter') -> 'Counter':
        self.correct += counter.correct
        self.incorrect += counter.incorrect
        return self

    def multiple_update(self, counters: Iterable['Counter']) -> 'Counter':
        for counter in counters:
            self.update(counter)
        return self

    @property
    def success_rate(self) -> float:
        return (self.correct / (self.correct + self.incorrect)) * 100


class DoorRiddle:
    doors = (False, True, False)

    @classmethod
    def evaluate(cls, choice: int, change: bool = False) -> bool:
        return change is not cls.doors[choice]

    @classmethod
    def random_play(cls, iterations: int, choice: bool = False, cpus: int = cpu_count()) -> Counter:
        args = [[int(iterations / cpus), choice] for _ in range(cpus)]
        args[0][0] += iterations % cpus
        with Pool() as pool:
            results = pool.starmap(cls.iterative_play, args)
            pool.close()
            pool.join()
        return Counter().multiple_update(results)

    @classmethod
    def iterative_play(cls, iterations: int, choice: bool) -> Counter:
        counter = Counter()
        start = time()
        log_number = 1000000
        for i in range(iterations):
            counter.add(cls.evaluate(randrange(0, 3), choice))
            # counter.add(cls.evaluate(i % 3, choice))
            if (i + 1) % log_number == 0:
                run_time = time() - start
                speed = (i + 1) / run_time
                estimate_time = (iterations - i) / speed
                print("{}M/{}M iterations in {} min {} sec. Estimated {} min {} sec left. "
                      "Speed: {} kiter/s."
                      .format((i + 1) / log_number, iterations / log_number,
                              int(run_time / 60), int(run_time % 60),
                              int(estimate_time / 60), int(estimate_time % 60),
                              round(speed) / 1000))
        return counter

    @staticmethod
    def print_result(change, percentage, cycles, run_time) -> None:
        print()
        print("Change = {}: Success rate = {} %.".format(change, percentage))
        print("Calculated cycles = {}, speed = {} kiter/s."
              .format(cycles, round(int(cycles / run_time / 1000))))
        print("Calculation took {} min {} sec.".format(int(run_time / 60), int(run_time % 60)))


if __name__ == "__main__":
    num_tries = 1000000000
    num_cpus = int(cpu_count() / 2)

    # switch doors
    start1 = time()
    result1 = DoorRiddle.random_play(num_tries, True, num_cpus)
    time1 = time() - start1

    # don't switch doors
    start2 = time()
    result2 = DoorRiddle.random_play(num_tries, False, num_cpus)
    time2 = time() - start2

    # print results
    DoorRiddle.print_result(True, result1.success_rate, num_tries, time1)
    DoorRiddle.print_result(False, result2.success_rate, num_tries, time2)

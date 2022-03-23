from collections import Counter
from multiprocessing import cpu_count, Pool
from random import randint
from time import time

import matplotlib.pyplot as plt
from psutil import virtual_memory


def randomize_throws_in_batches(batch, repetitions, dice=6, num_throws=3):
    counter = Counter()
    num_batches = int(repetitions / batch)
    batches = [batch for _ in range(num_batches)]
    batches.append(repetitions % batch)
    tic = time()

    for i in range(len(batches)):
        results = randomize_throws(batches[i], dice, num_throws)
        counter.update(Counter(results))
        results = dict()

        tac = time()
        iters_done = sum(batches[:(i + 1)])
        current_time = tac - tic
        time_left = (current_time / iters_done) * (sum(batches) - iters_done)
        print("{}M/{}M iterations in {} min {} sec. "
              "Estimated {} min {} sec left. Speed {} iters/s"
              .format(iters_done / 1000000, repetitions / 1000000,
                      int(current_time / 60), int(current_time % 60),
                      int(time_left / 60), int(time_left % 60),
                      int(iters_done / current_time)))
    return counter


def randomize_throws(repetitions, dice=6, num_throws=3):
    throws_result = list()
    for i in range(repetitions):
        throws_result.append(get_random_dice_sum(num_throws, dice))
    return throws_result


def get_random_dice_sum(num_throws=3, dice=6):
    return sum([throw_dice(dice) for _ in range(num_throws)])


def throw_dice(dice=6):
    return randint(1, dice)


if __name__ == '__main__':
    num_dice = 6
    num_attempts = 10
    iterations = 10000

    cpus = cpu_count()
    # cpus = 4
    batch_size = min(int(virtual_memory().available / 512), 1000000)

    start = time()
    args = [[batch_size, int(iterations / cpus), num_dice, num_attempts] for _ in range(cpus)]
    args[0][0] += iterations % cpus
    with Pool() as pool:
        counted_results = pool.starmap(randomize_throws_in_batches, args)
    end = time()

    print()
    print("{}M iterations completed.".format(iterations / 1000000))
    print("Calculation took {} min {} s.".format(int((end - start) / 60), int((end - start) % 60)))

    counted_final = Counter()
    for cnt in counted_results:
        counted_final.update(cnt)
    throws = dict(sorted(counted_final.items()))

    print(throws)
    plt.bar(range(len(throws)), list(throws.values()), align='center')
    plt.xticks(range(len(throws)), list(throws.keys()))
    plt.show()

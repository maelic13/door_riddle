from collections import namedtuple
from itertools import permutations
from typing import List, Sequence


Season = namedtuple("Season", "name adventures")
Result = namedtuple("Result", "base_season compared_season score")


def calculate_variation(default: Sequence[int], comparing: Sequence[int]) -> int:
    variation = 0
    for encounter in comparing:
        if encounter not in default:
            variation += 10
            continue
        variation += abs(comparing.index(encounter) - default.index(encounter))
    return variation


def find_max_variation(season: Sequence[int]) -> Sequence[int]:
    new_season = list(season[::-1])
    missing_indices = [x for x in range(1, 11) if x not in season]
    new_season[3] = missing_indices[0]
    new_season[4] = missing_indices[1]
    return tuple(new_season)


def result_permutations(seasons: List[Season]) -> List[Result]:
    results = list()
    for season1, season2 in permutations(seasons, 2):
        score = calculate_variation(season1.adventures, season2.adventures)
        results.append(Result(season1.name, season2.name, score))
    return results


def base_results(base: Season, compare: List[Season]) -> List[Result]:
    results = list()
    for compared_season in compare:
        score = calculate_variation(base.adventures, compared_season.adventures)
        results.append(Result(base.name, compared_season.name, score))
    return results


def print_results(results: List[Result]) -> None:
    for result in results:
        print(f"{result.base_season}-{result.compared_season} variation score is {result.score}.")


if __name__ == "__main__":
    # define seasons
    spring = Season("Spring", (2, 4, 10, 9, 3, 7, 1, 6))
    summer = Season("Summer", (4, 10, 5, 1, 3, 9, 8, 7))
    fall = Season("Fall", (1, 9, 6, 8, 7, 5, 2, 10))
    winter = Season("Winter", (10, 1, 5, 6, 3, 2, 7, 4))

    # calculate scores
    permutation_results = result_permutations([spring, summer, fall, winter])
    spring_scores = base_results(spring, [summer, fall, winter])

    # print results
    print_results(spring_scores)

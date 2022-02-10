from collections import namedtuple
from itertools import permutations
from typing import List, Sequence


Season = namedtuple("Season", "name adventures")
Result = namedtuple("Result", "base_season compared_season score")


def calculate_variation(default: Season, comparing: Season) -> int:
    variation = 0
    for encounter in comparing.adventures:
        if encounter not in default.adventures:
            variation += 10
            continue
        variation += abs(comparing.adventures.index(encounter) - default.adventures.index(encounter))
    return variation


def find_max_variation(season: Season) -> Season:
    new_season_adventures = list(season.adventures[::-1])
    missing_indices = [x for x in range(1, 11) if x not in season]
    new_season_adventures[3] = missing_indices[0]
    new_season_adventures[4] = missing_indices[1]
    return Season(season.name + "_opposite", tuple(new_season_adventures))


def result_permutations(seasons: List[Season]) -> List[Result]:
    return [Result(season1.name, season2.name, calculate_variation(season1, season2))
            for season1, season2 in permutations(seasons, 2)]


def base_results(base: Season, compare: List[Season]) -> List[Result]:
    return [Result(base.name, compared_season.name, calculate_variation(base, compared_season))
            for compared_season in compare]


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
    max_variation_spring = find_max_variation(spring)

    # print results
    print_results(spring_scores)
    print(max_variation_spring)

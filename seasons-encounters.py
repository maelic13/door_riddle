from typing import Sequence


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


if __name__ == "__main__":
    spring = (2, 4, 10, 9, 3, 7, 1, 6)
    summer = (4, 10, 5, 1, 3, 9, 8, 7)
    fall = (1, 9, 6, 8, 7, 5, 2, 10)
    winter = (10, 1, 5, 6, 3, 2, 7, 4)

    summer_var = calculate_variation(spring, summer)
    fall_var = calculate_variation(spring, fall)
    winter_var = calculate_variation(spring, winter)

    print(f"Variation in summer compared to spring is {summer_var}.")
    print(f"Variation in fall compared to spring is {fall_var}.")
    print(f"Variation in winter compared to spring is {winter_var}.")
    print()

    max_var_season = find_max_variation(spring)
    max_var = calculate_variation(spring, max_var_season)
    print(f"Maximum variation season to spring is {max_var_season}.")
    print(f"Maximum variation seasons value is {max_var}.")

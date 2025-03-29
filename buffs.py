#!/usr/bin/env python3
import math
from collections.abc import Callable
from functools import partial

from prettytable import PrettyTable

ALLIANCE_HELP_PERCENTAGE = 0.005  # 0.5 %


def seconds_to_string(seconds: int) -> str:
    (minutes, seconds) = divmod(seconds, 60)
    (hours, minutes) = divmod(minutes, 60)
    (days, hours) = divmod(hours, 24)

    result = ""
    if days:
        result += f"{days}d "
    return result + f"{hours}:{minutes:02}:{seconds:02}"


def time_to_seconds(days: int, hours: int, minutes: int, seconds: int) -> int:
    return ((days * 24 + hours) * 60 + minutes) * 60 + seconds


def format_percent(percentage: float) -> str:
    return f"{percentage * 100:.1f} %"


def effective_time(construction: int, alliance_help_max: int, allinace_help_minimum_time: int, time: int) -> int:
    time = max(0, time - construction)
    for _ in range(alliance_help_max):
        time -= max(0, allinace_help_minimum_time, math.floor(time * ALLIANCE_HELP_PERCENTAGE))
    return max(0, time)


def gen_row(title: str, time: int, make_effective: Callable[[int], int], relative: int | None) -> list[str]:
    effective_time = make_effective(time)
    if relative is None:
        return [title, seconds_to_string(time), "", "", seconds_to_string(effective_time), "", ""]

    effective_relative = make_effective(relative)
    saved = relative - time
    saved_effective = effective_relative - effective_time
    return [
        title,
        seconds_to_string(time),
        seconds_to_string(saved),
        format_percent(saved / relative),
        seconds_to_string(effective_time),
        seconds_to_string(saved_effective),
        format_percent(saved_effective / effective_relative),
    ]


def calc_duration(
    original_seconds: int,
    buffs: int,
    construction_buff: int = 0,
    alliance_help_max: int = 0,
    alliance_help_minimum_time: int = 60,  # 1 minute
) -> None:
    my_effective_time = partial(effective_time, construction_buff, alliance_help_max, alliance_help_minimum_time)
    table = PrettyTable(
        [
            "Type",
            "Time on Button",
            "Saved",
            "Saved %",
            "Effective time",
            "Saved effective",
            "Saved effective %",
        ]
    )
    table.add_row(gen_row("original time", original_seconds, my_effective_time, None))

    time = math.ceil(original_seconds / (1 + buffs / 100))
    table.add_row(gen_row("without additional buff", time, my_effective_time, original_seconds))
    table.add_row(
        gen_row("additional 25% buff", math.ceil(original_seconds / (1 + (buffs + 25) / 100)), my_effective_time, time)
    )
    table.add_row(
        gen_row("additional 50% buff", math.ceil(original_seconds / (1 + (buffs + 50) / 100)), my_effective_time, time)
    )
    print(table)


original_time = time_to_seconds(2, 15, 15, 52)
buffs_percentage = 88
construction_buff = time_to_seconds(0, 1, 28, 48)
alliance_help_max = 23
alliance_help_minimum_time = time_to_seconds(0, 0, 6, 30)

calc_duration(original_time, buffs_percentage, construction_buff, alliance_help_max, alliance_help_minimum_time)

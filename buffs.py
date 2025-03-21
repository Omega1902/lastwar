import math


def seconds_to_string(seconds: int) -> str:
    (minutes, seconds) = divmod(seconds, 60)
    (hours, minutes) = divmod(minutes, 60)
    (days, hours) = divmod(hours, 24)

    result = ""
    if days:
        result += f"{days}d "
    if days or hours:
        result += f"{hours}:"
    return result + f"{minutes:02}:{seconds:02}"


def time_to_seconds(days: int, hours: int, minutes: int, seconds: int) -> int:
    return ((days * 24 + hours) * 60 + minutes) * 60 + seconds


def format_percent(percentage: float) -> str:
    return f"{percentage * 100:.1f} %"


def calc_duration(original_seconds: int, buffs: int) -> None:
    print("Original time: " + seconds_to_string(original_seconds))
    time = math.ceil(original_seconds / (1 + buffs / 100))
    saved = original_seconds - time
    print(
        f"Time without additional buff:  {seconds_to_string(time)} - saved: {seconds_to_string(saved)} ({format_percent(saved / original_seconds)})"
    )
    time25 = math.ceil(original_seconds / (1 + (buffs + 25) / 100))
    saved25 = time - time25
    print(
        f"Time with additional 25% buff: {seconds_to_string(time25)} - additionally saved: {seconds_to_string(saved25)} ({format_percent(saved25 / time)})"
    )
    time50 = math.ceil(original_seconds / (1 + (buffs + 50) / 100))
    saved50 = time - time50
    print(
        f"Time with additional 50% buff: {seconds_to_string(time50)} - additionally saved: {seconds_to_string(saved50)} ({format_percent(saved50 / time)})"
    )


original_time = time_to_seconds(0, 15, 15, 52)
buffs_percentage = 78

calc_duration(original_time, buffs_percentage)

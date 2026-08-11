WALL_BIT = {"north": 0, "east": 1, "south": 2, "west": 3}


def calc_wall_sum(walls_dict: dict[str, bool]) -> int:
    result = 0
    for wall, is_close in walls_dict.items():
        if is_close:
            result += 1 << WALL_BIT[wall]
    return result


def convert_hex(num: int) -> str:
    return hex(num).replace("0x", "")

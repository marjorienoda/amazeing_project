from typing import TypedDict

#  python3.10のtypingにはNotRequiredがない→3.10以降に対応だから、3.10でも使えるようにしたい
#  →typing_extensions(typingより先行してNotRequiredが追加されている)に頼る
#  よって、外部パッケージ(typing_extensions)をpip installしないといけない
from typing_extensions import NotRequired

REQUIRED_KEYS = [
    "WIDTH",
    "HEIGHT",
    "ENTRY",
    "EXIT",
    "OUTPUT_FILE",
    "PERFECT"
]
# 必須キーを定数にした。


class MazeConfig(TypedDict):
    width: int
    height: int
    entry: tuple[int, int]
    exit: tuple[int, int]
    output_file: str
    perfect: bool
    seed: NotRequired[int]  # NotRequired　あってもなくてもいい扱いになる


class ConfigError(Exception):
    def __init__(self, message: str = "Error"):
        super().__init__(message)


def read_config(file: str) -> dict[str, str]:
    try:
        with open(file) as f:
            data = f.read()
    except OSError as e:
        raise ConfigError(f"Could not open config file: {e}")

    lines = data.splitlines()
    key_dict: dict[str, str] = {}
    for line in lines:
        line_data = line.strip()
        if line_data.startswith("#") or line_data == "":
            continue
        if "=" not in line_data:
            raise ConfigError(f"Invalid line in config file: '{line_data}'")

        key, value = line_data.split("=", 1)
        key_dict[key.strip()] = value.strip()
    return key_dict


def int_convert(value: str, key_name: str) -> int:
    try:
        result = int(value)
    except ValueError:
        raise ConfigError(
            f"Invalid type for the key '{key_name}': "
            f"expected an integer, got '{value}'"
        )
    return result


def coordinate_convert(value: str, key_name: str) -> tuple[int, int]:
    coordinate = value.split(",")
    if len(coordinate) != 2:
        raise ConfigError(f"Invalid input for the '{key_name}'")
    x, y = coordinate
    result_x = int_convert(x, key_name)
    result_y = int_convert(y, key_name)
    return (result_x, result_y)


def bool_convert(value: str, key_name: str) -> bool:
    if value == "True":
        result = True
    elif value == "False":
        result = False
    else:
        raise ConfigError(
            f"Invalid value for the key '{key_name}': "
            f"expected 'True' or 'False', got '{value}'"
        )
    return result


def build_maze_config(key_dict: dict[str, str]) -> MazeConfig:
    width = int_convert(key_dict["WIDTH"], "WIDTH")
    if width <= 0:
        raise ConfigError("Value for the key 'WIDTH' is <= 0")
    height = int_convert(key_dict["HEIGHT"], "HEIGHT")
    if height <= 0:
        raise ConfigError("Value for the key 'HEIGHT' is <= 0")

    entry = coordinate_convert(key_dict["ENTRY"], "ENTRY")
    exit = coordinate_convert(key_dict["EXIT"], "EXIT")
    perfect = bool_convert(key_dict["PERFECT"], "PERFECT")
    output_file = key_dict["OUTPUT_FILE"]

    config: MazeConfig = {
        "width": width,
        "height": height,
        "entry": entry,
        "exit": exit,
        "output_file": output_file,
        "perfect": perfect,
    }  # seedは必須ではない＝ないかもしれないのでここには含めない

    # ここでseedが存在するなら追加する処理を行う
    # 後から追加しても型チェックに怒られないのはNotRequiredのおかげ
    if "SEED" in key_dict:
        config["seed"] = int_convert(key_dict["SEED"], "SEED")

    return config


# convertでは必須キーが含まれていない場合のエラーがチェックされない。ex) "WIDTH"がそもそもない場合、何もチェックされないで通る ので作った
def check_required_keys(key_dict: dict[str, str]) -> None:
    """Check whether entered keys contain required keys.

    Args:
        key_dict: A dictionary of entered config data,
            e.g. {"WIDTH": "20", "HEIGHT": "30"}.

    Raises:
        ConfigError: If any required key is missing from `key_dict`.
    """
    input_keys = set(key_dict)
    required_keys = set(REQUIRED_KEYS)
    result = required_keys.difference(input_keys)
    # requiredの中にあって、inputの中にないものだけ検出する。　完全一致ならFalse(空集合)になる
    if result:
        raise ConfigError(f"Not enough keys: {','.join(result)}")


def validate_entry_exit(
    width: int, height: int, entry: tuple[int, int], exit: tuple[int, int]
) -> None:
    """Check whether the "entry" and "exit" values are valid.

    Check the following three items:
        - Are the entry coordinates within the maze's boundaries?
        - Are the exit coordinates within the maze's boundaries?
        - Are "entry" and "exit" different from each other?

    Args:
        width: Width of the maze.
        height: Height of the maze.
        entry: Starting coordinates (x, y) of the maze.
        exit: Ending coordinates (x, y) of the maze.

    Raises:
        ConfigError: If entry or exit is out of bounds, or if entry and exit
            are the same.
    """
    entry_x, entry_y = entry
    exit_x, exit_y = exit
    if not (0 <= entry_x < width and 0 <= entry_y < height):
        raise ConfigError(
            f"Entry {entry} is out of bounds "
            f"(width={width}, height={height})"
        )
    if not (0 <= exit_x < width and 0 <= exit_y < height):
        raise ConfigError(
            f"Exit {exit} is out of bounds "
            f"(width={width}, height={height})"
        )
    if entry == exit:
        raise ConfigError(f"Entry and exit must be different: {entry}")

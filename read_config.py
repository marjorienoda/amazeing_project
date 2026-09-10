"""Config file parsing and validation for the A-Maze-ing project.

Reads a `KEY=VALUE` style config file, validates that all required keys
are present and well-formed, and converts the raw string values into a
typed `MazeConfig` ready to be passed to `MazeGenerator`.
"""

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


class MazeConfig(TypedDict):
    """Typed representation of a validated maze configuration.

    All fields are required except `seed`, which is optional (a random
    seed is used if not provided).

    Attributes:
        width: Maze width, in cells.
        height: Maze height, in cells.
        entry: Starting coordinates `(x, y)`.
        exit: Ending coordinates `(x, y)`.
        perfect: Whether to generate a perfect maze (no loops).
        seed: Optional seed for reproducible generation.
    """
    width: int
    height: int
    entry: tuple[int, int]
    exit: tuple[int, int]
    perfect: bool
    seed: NotRequired[int]  # NotRequired　あってもなくてもいい扱いになる


class ConfigError(Exception):
    """Raised when the config file is missing, malformed, or invalid."""

    def __init__(self, message: str = "Error"):
        super().__init__(message)


def read_config(file: str) -> dict[str, str]:
    """Read and parse a `KEY=VALUE` style config file.

    Blank lines and lines starting with `#` are ignored. All other
    lines must contain exactly one `=`, splitting the line into a key
    and a value (both stripped of surrounding whitespace).

    Args:
        file: Path to the config file to read.

    Returns:
        A dictionary mapping each key to its raw string value, exactly
        as written in the file (no type conversion applied yet).

    Raises:
        ConfigError: If the file cannot be opened, or if a non-blank,
            non-comment line does not contain an `=`.
    """
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
    """Convert a raw string value to an integer.

    Args:
        value: The raw string value to convert.
        key_name: The config key this value belongs to, used only to
            produce a clear error message.

    Returns:
        The converted integer value.

    Raises:
        ConfigError: If `value` is not a valid integer.
    """
    try:
        result = int(value)
    except ValueError:
        raise ConfigError(
            f"Invalid type for the key '{key_name}': "
            f"expected an integer, got '{value}'"
        )
    return result


def coordinate_convert(value: str, key_name: str) -> tuple[int, int]:
    """Convert a raw `"x,y"` string value into a coordinate tuple.

    Args:
        value: The raw string value to convert, expected to contain
            exactly two comma-separated integers.
        key_name: The config key this value belongs to, used only to
            produce a clear error message.

    Returns:
        The converted `(x, y)` coordinate tuple.

    Raises:
        ConfigError: If `value` does not contain exactly two
            comma-separated parts, or if either part is not a valid
            integer.
    """
    coordinate = value.split(",")
    if len(coordinate) != 2:
        raise ConfigError(f"Invalid input for the '{key_name}'")
    x, y = coordinate
    result_x = int_convert(x, key_name)
    result_y = int_convert(y, key_name)
    return (result_x, result_y)


def bool_convert(value: str, key_name: str) -> bool:
    """Convert a raw `"True"`/`"False"` string value into a bool.

    Args:
        value: The raw string value to convert. Must be exactly
            `"True"` or `"False"`.
        key_name: The config key this value belongs to, used only to
            produce a clear error message.

    Returns:
        The converted boolean value.

    Raises:
        ConfigError: If `value` is neither `"True"` nor `"False"`.
    """
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


def build_maze_config(key_dict: dict[str, str]) -> tuple[MazeConfig, str]:
    """Convert raw config values into a typed `MazeConfig`.

    Validates and converts `WIDTH`, `HEIGHT`, `ENTRY`, `EXIT`, `PERFECT`,
    and the optional `SEED`. `OUTPUT_FILE` is returned separately, since
    it is not part of `MazeGenerator`'s reusable configuration.

    Args:
        key_dict: The raw config dictionary, as returned by
            `read_config`. Must already contain all keys in
            `REQUIRED_KEYS` (see `check_required_keys`).

    Returns:
        A tuple `(config, output_file)`, where `config` is ready to be
        passed to `MazeGenerator` via `MazeGenerator(**config)`, and
        `output_file` is the path to write the maze output file to.

    Raises:
        ConfigError: If `WIDTH` or `HEIGHT` is not a positive integer,
            or if any value fails its individual conversion (see
            `int_convert`, `coordinate_convert`, `bool_convert`).
    """
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
    if not output_file:
        raise ConfigError(
            f"Invalid value for the key 'OUTPUT_FILE': "
            f"expected a non-empty filename, got '{output_file}'"
        )

    config: MazeConfig = {
        "width": width,
        "height": height,
        "entry": entry,
        "exit": exit,
        "perfect": perfect,
    }  # seedは必須ではない＝ないかもしれないのでここには含めない

    # ここでseedが存在するなら追加する処理を行う
    # 後から追加しても型チェックに怒られないのはNotRequiredのおかげ
    if "SEED" in key_dict:
        config["seed"] = int_convert(key_dict["SEED"], "SEED")

    return config, output_file


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

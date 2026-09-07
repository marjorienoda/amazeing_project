REQUIRED_KEYS = [
    "WIDTH",
    "HEIGHT",
    "ENTRY",
    "EXIT",
    "OUTPUT_FILE",
    "PERFECT"
]
# 必須キーを定数にした。


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


# ↓convert_keysという名前だけど、ValueCheckもしてるから、名前を変えるべき？　or チェック部分を別関数に切り出す
def convert_keys(
            key_dict: dict[str, str],
        ) -> dict[str, int | tuple[int, int] | bool | str]:
    new_key_dict: dict[str, int | tuple[int, int] | bool | str] = {}
    for key, value in key_dict.items():
        if key in ("WIDTH", "HEIGHT", "SEED"):
            try:
                converted_int_value = int(value)
            except ValueError:
                raise ConfigError(
                    f"Invalid type for the key '{key}': "
                    f"expected an integer, got '{value}'"
                )
            if key in ("WIDTH", "HEIGHT") and converted_int_value <= 0:
                raise ConfigError(f"Value for the key '{key}' is <= 0")
            new_key_dict[key.lower()] = converted_int_value
        elif key in ("ENTRY", "EXIT"):
            coordinate: list[str] = value.split(",")
            if len(coordinate) != 2:
                raise ConfigError(f"Invalid input for the '{key}'")
            try:
                converted_tuple_value = (
                    int(coordinate[0]),
                    int(coordinate[1]),
                )
            except ValueError:
                raise ConfigError(
                    f"Invalid type for the key '{key}': expected an integer"
                )
            new_key_dict[key.lower()] = converted_tuple_value
        elif key == "PERFECT":
            if value == "True":
                converted_bool_value = True
            elif value == "False":
                converted_bool_value = False
            else:
                raise ConfigError(f"Invalid input for the key: '{key}'")
            new_key_dict[key.lower()] = converted_bool_value
        elif key == "OUTPUT_FILE":
            new_key_dict[key.lower()] = value
        else:
            raise ConfigError(f"Unknow argument in the config file: '{key}'")
    return new_key_dict


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

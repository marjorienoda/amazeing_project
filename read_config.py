<<<<<<< HEAD
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
=======
def read_config(file: str) -> dict[str, str] | None:
    try:
        with open(file) as f:
            data = f.read()
            lines = data.splitlines()
            key_dict: dict[str, str] = {}
            for line in lines:
                line_data = line.strip()
                if line_data.startswith("#") or line_data == "":
                    continue
                key, value = line_data.split("=")
                key_dict[key] = value

    except OSError as e:
        print(f"Could not open config file: {e}")
        return None
    except ValueError as e:
        print(f"Invalid line in config file: '{line}' ({e})")
        return None
>>>>>>> 8bb92a497afcae03f59e880e5cc09b07513a8699
    return key_dict


def convert_keys(
<<<<<<< HEAD
            key_dict: dict[str, str],
        ) -> dict[str, int | tuple[int, int] | bool | str] | None:
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
=======
    key_dict: dict[str, str],
) -> dict[str, int | tuple[int, int] | bool | str] | None:
    new_key_dict: dict[str, int | tuple[int, int] | bool | str] = {}
    for key, value in key_dict.items():
        if key in ("WIDTH", "HEIGHT", "SEED"):
            converted_int_value = int(value)
            new_key_dict[key.lower()] = converted_int_value
        elif key in ("ENTRY", "EXIT"):
            coordinate: list[str] = value.split(",")
            converted_tuple_value = (int(coordinate[0]), int(coordinate[1]))
>>>>>>> 8bb92a497afcae03f59e880e5cc09b07513a8699
            new_key_dict[key.lower()] = converted_tuple_value
        elif key == "PERFECT":
            if value == "True":
                converted_bool_value = True
            elif value == "False":
                converted_bool_value = False
            else:
<<<<<<< HEAD
                raise ConfigError(f"Invalid input for the key: '{key}'")
=======
                print("key: PERFECT is bool.")
                return None
>>>>>>> 8bb92a497afcae03f59e880e5cc09b07513a8699
            new_key_dict[key.lower()] = converted_bool_value
        elif key == "OUTPUT_FILE":
            new_key_dict[key.lower()] = value
        else:
<<<<<<< HEAD
            raise ConfigError(f"Unknow argument in the config file: '{key}'")
    return new_key_dict
=======
            print("Unknown Key")
            return None
    return new_key_dict


def main() -> None:
    key_dict = read_config("config.txt")
    if key_dict is None:
        return

    print("=== read_config ===")
    print(key_dict)

    keys = convert_keys(key_dict)
    if keys is None:
        return

    print("=== convert_keys ===")
    print(keys)
    # output_file_name = keys.pop("output_file")
    # maze = MazeGenerator(**keys)


if __name__ == "__main__":
    main()
>>>>>>> 8bb92a497afcae03f59e880e5cc09b07513a8699

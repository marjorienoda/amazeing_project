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


def convert_keys(
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

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
    return key_dict


def convert_keys(
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
            new_key_dict[key.lower()] = converted_tuple_value
        elif key == "PERFECT":
            if value == "True":
                converted_bool_value = True
            elif value == "False":
                converted_bool_value = False
            else:
                print("key: PERFECT is bool.")
                return None
            new_key_dict[key.lower()] = converted_bool_value
        elif key == "OUTPUT_FILE":
            new_key_dict[key.lower()] = value
        else:
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

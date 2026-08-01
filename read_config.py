from main import Cell, MazeGenerator

def read_config(file: str) -> dict | None:
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


def convert_keys(key_dict: dict) -> dict | None:
    new_key_dict = {}
    for key in key_dict:
        if key in ("WIDTH", "HEIGHT", "SEED"):
            converted_value = int(key_dict[key])
            new_key_dict[key.lower()] = converted_value
        elif key in ("ENTRY", "EXIT"):
            coordinate: list[str] = key_dict[key].split(",")
            converted_value = (int(coordinate[0]), int(coordinate[1]))
            new_key_dict[key.lower()] = converted_value
        elif key == "PERFECT":
            if key_dict[key] == "True":
                converted_value = True
            elif key_dict[key] == "False":
                converted_value = False
            else:
                print("key: PERFECT is bool.")
                return None
            new_key_dict[key.lower()] = converted_value
        elif key == "OUTPUT_FILE":
            new_key_dict[key.lower()] = key_dict[key]
        else:
            print("Unknown Key")
            return None
    return new_key_dict


def main():
    key_dict = read_config("config.txt")
    if key_dict is None:
        return
    keys = convert_keys(key_dict)
    if keys is None:
        return
    output_file_name = keys.pop("output_file")
    maze = MazeGenerator(**keys)


if __name__ == "__main__":
    main()

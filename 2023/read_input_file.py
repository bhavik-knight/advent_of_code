from pathlib import Path


def main():
    file_path = Path("3_1_sample_input.txt")
    lines = get_lines(file_path)
    print(lines)
    return None


def get_lines(file_path: str) -> [str]:
    with open(file_path, "r") as f:
        return f.readlines()


if __name__ == "__main__":
    main()

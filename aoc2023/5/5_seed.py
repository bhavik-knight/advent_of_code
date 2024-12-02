import re, sys
from typing import List
from pathlib import Path


def main():
    file_path = Path(__file__).parent.joinpath("5_1_sample.txt")
    # file_path = Path(__file__).parent.joinpath("5_1_input.txt")
    lines = get_all_maps(file_path)

    seeds = lines[0]
    locations:list = list()
    min_loc = sys.maxsize
    for seed in seeds:
        dst = get_location(seed, lines[1:])
        locations.append(dst)
        min_loc = min(dst, min_loc)
    print(locations)

    # puzzle 1
    print(f"puzzle 1: {min_loc}")

    # puzzle 2
    seed_range = []
    for i in range(1, len(seeds), 2):
        seed_range.append((seeds[i - 1], seeds[i - 1] + seeds[i]))

    min_location = sys.maxsize
    locations_new = list()
    for entry in seed_range:
        for seed in range(*entry):
            dst = get_location(seed, lines[1:])
            locations_new.append({seed: dst})
            min_location = min(dst, min_location)
    print(locations_new)
    print(f"puzzle 2: {min_location}")

    return None


def get_location(seed: int, maps: List[dict]) -> int:
    dst = seed
    for i, line in enumerate(maps):
        for (start, end), distance in line.items():
            if start <= dst <= end:
                dst += distance
                break
    return dst


def get_all_maps(file_name: str) -> List[str]:
    seeds = list()
    seed_to_soil = dict()
    soil_to_fert = dict()
    fert_to_water = dict()
    water_to_light = dict()
    light_to_temp = dict()
    temp_to_humidity = dict()
    humidity_to_location = dict()

    with open(file_name, "r") as f:
        lines = f.readlines()

    i, total = 0, len(lines)
    while i < total:
        line = str.strip(lines[i])
        if not line:
            i += 1
            continue

        elif line.startswith("seeds"):
            seeds = list(map(lambda x: int(x), re.findall(r"\d+\s*", line.strip())))
            i += 1

        elif line.startswith("seed-to-soil"):
            i += 1
            while True:
                data = str.strip(lines[i])
                if not data:
                    break
                dst, src, r = map(lambda x: int(x), data.split())
                seed_to_soil.update({(src, src + r - 1): dst - src})
                i += 1
            print(f"s-s: {seed_to_soil}")
            i += 1

        elif line.startswith("soil-to-fert"):
            j = i + 1
            while True:
                data = str.strip(lines[j])
                if not data:
                    break
                dst, src, r = map(lambda x: int(x), data.split())
                soil_to_fert.update({(src, src + r - 1): dst - src})
                j += 1
            print(f"s-f: {soil_to_fert}")
            i = j + 1

        elif line.startswith("fertilizer-to-water"):
            j = i + 1
            while True:
                data = str.strip(lines[j])
                if not data:
                    break
                dst, src, r = map(lambda x: int(x), data.split())
                fert_to_water.update({(src, src + r - 1): dst - src})
                j += 1
            print(f"f-w: {fert_to_water}")
            i = j + 1

        elif line.startswith("water-to-light"):
            j = i + 1
            while True:
                data = str.strip(lines[j])
                if not data:
                    break
                dst, src, r = map(lambda x: int(x), data.split())
                water_to_light.update({(src, src + r - 1): dst - src})
                j += 1
            print(f"w-l: {water_to_light}")
            i = j + 1

        elif line.startswith("light-to-temp"):
            j = i + 1
            while True:
                data = str.strip(lines[j])
                if not data:
                    break
                dst, src, r = map(lambda x: int(x), data.split())
                light_to_temp.update({(src, src + r - 1): dst - src})
                j += 1
            print(f"l-t: {light_to_temp}")
            i = j + 1

        elif line.startswith("temperature-to-humidity"):
            j = i + 1
            while True:
                data = str.strip(lines[j])
                if not data:
                    break
                dst, src, r = map(lambda x: int(x), data.split())
                temp_to_humidity.update({(src, src + r - 1): dst - src})
                j += 1
            print(f"t-h: {temp_to_humidity}")
            i = j + 1

        elif line.startswith("humidity-to-location"):
            j = i + 1
            while True and j < total:
                data = str.strip(lines[j])
                if not data:
                    break
                dst, src, r = map(lambda x: int(x), data.split())
                humidity_to_location.update({(src, src + r): dst - src})
                j += 1
            print(f"h-l: {humidity_to_location}")
            i = j + 1

    return [seeds, seed_to_soil, soil_to_fert, fert_to_water, water_to_light, light_to_temp, temp_to_humidity, humidity_to_location]


if __name__ == "__main__":
    main()

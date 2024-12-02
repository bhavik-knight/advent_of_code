import re
from pathlib import Path

def main():
    # file_path = Path(__file__).parent.joinpath("sample1.txt")
    # file_path = Path(__file__).parent.joinpath("sample2.txt")
    # file_path = Path(__file__).parent.joinpath("sample.txt")
    file_path = Path(__file__).parent.joinpath("input.txt")

    directions, nodes = get_directions_nodes(file_path)
    directions = directions.replace("R", "1")
    directions = directions.replace("L", "0")

    graph = generate_graph(nodes)

    # puzzle 1
    counter, traversed = traverse_graph(graph, "AAA", "ZZZ", directions)

    # puzzle 2
    counter_list, traversed_list = ghost_traverse(graph, directions)

    # print(f"tranversed: {traversed}")
    lcm = get_lcm_list(counter_list)
    print(f"Steps: {lcm}")
    return None


def get_gcd(a: int, b: int) -> int:
    while b != 0:
        a, b = b, a % b
    return a


def get_lcm(a:int, b: int) -> int:
    return a * b // get_gcd(a, b)


def get_lcm_list(l: list) -> int:
    lcm = l[0]
    for i in l[1:]:
        lcm = get_lcm(lcm, i)
    return lcm


def ghost_traverse(graph: dict, directions) -> [int, list]:
    length = len(directions)

    current_nodes = list(filter(lambda x: x.endswith("A"), graph))
    print(f"current_nodes: {current_nodes}")

    traversed_nodes_list = list()
    counter_list = list()

    for current in current_nodes:
        counter = 0
        traversed_nodes = list()
        while True:
            direction = int(directions[counter % length])
            current = graph[current][direction]
            traversed_nodes.append(current)
            # print(current_nodes)
            counter += 1

            if current in filter(lambda x: x.endswith("Z"), graph):
                counter_list.append(counter)
                traversed_nodes_list.append(traversed_nodes)
                break

        print(counter)
    return counter_list, traversed_nodes_list


def traverse_graph(graph: dict, start: str, end: str, directions: [str]) -> [int, list]:
    print(f"Graph: {graph}")
    counter = 0
    current = start
    traversed_nodes = list()
    length = len(directions)

    while True:
        direction = int(directions[counter % length])
        current = graph[current][direction]
        traversed_nodes.append(current)
        counter += 1

        if current == end:
            return counter, traversed_nodes
    return None


def get_directions_nodes(file_name: str) -> [list, dict]:
    lines = list()
    with open(file_name, "r") as f:
        lines = f.readlines()

    directions = lines[0].strip()
    nodes = dict()
    for line in lines[2:]:
        k, v = line.strip().split("=")
        nodes[k.strip()] = re.findall(r"[0-9A-Z]{3}", v.strip())
    return directions, nodes


def generate_graph(nodes: dict) -> dict:
    graph = dict()
    for k, v in nodes.items():
        graph[k] = v
    return graph


if __name__ == "__main__":
    main()

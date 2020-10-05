import fileinput
import sys
from queue import Queue


# We (sometimes)destroy input nka!!!


class VertexFrozenset(frozenset):
    def __repr__(self):
        return "{" + ", ".join([item.__repr__() for item in self]) + "}"


class GoodNKA:  # one letter transitions, no epsilons
    def __init__(self, vertexes_number, start_vertex, terminal_vertexes, edges, alphabet):
        # every vertex is a frozenset of trivial vertex
        self.start_vertex = start_vertex  # one start vertex
        self.terminal_vertexes = terminal_vertexes  # set of terminal vertexes
        self.edges = edges  # vertex -> letter -> set of trivial vertexes
        self.alphabet = alphabet  # list of letters
        self.vertexes_number = vertexes_number

    def pretty_print(self):
        print("********************")
        print(f"Total {self.vertexes_number} vertexes")
        print(f"Start vertex is - {self.start_vertex}")
        print("Terminal vertexes:", self.terminal_vertexes)
        print("Edges: format from -letter-> to1 | to2 ...")
        for vertex in self.edges:
            print("----------")
            for letter in self.edges[vertex]:
                print(vertex, f"-{letter}->", " | ".join(map(repr, self.edges[vertex][letter])))
        # print("----------")
        print("********************")


def minimizator(pdka):
    nonterminal_vertexes = VertexFrozenset({vertex for vertex in pdka.edges if vertex not in pdka.terminal_vertexes})
    v_class = [dict([(vertex, pdka.terminal_vertexes)
                     if vertex in pdka.terminal_vertexes
                     else (vertex, nonterminal_vertexes)
                     for vertex in pdka.edges])]  # vertex -> class on i-th iteration
    i = 1
    while True:
        match_destination = dict()
        for vertex in pdka.edges:
            destination_mask = []
            for letter in pdka.alphabet:
                destination_vertex = next(iter(pdka.edges[vertex][letter]))
                destination_mask.append(VertexFrozenset(v_class[i - 1][destination_vertex]))
            hashable_mask = tuple(destination_mask)
            if hashable_mask in match_destination:
                match_destination[hashable_mask].add(vertex)
            else:
                match_destination[hashable_mask] = {vertex}

        v_class.append(dict())
        for mask in match_destination:
            for vertex in match_destination[mask]:
                v_class[i][vertex] = match_destination[mask].intersection(v_class[i - 1][vertex])

        if v_class[i - 1] == v_class[i]:
            break

        i += 1

    result_division = v_class[-1]
    for vertex in result_division: # delete copies "from"
        if vertex != min(result_division[vertex]):
            pdka.terminal_vertexes.discard(vertex)
            del pdka.edges[vertex]

    for vertex in pdka.edges:
        for letter in pdka.edges[vertex]:
            destination_vertex = next(iter(pdka.edges[vertex][letter]))
            if destination_vertex != min(result_division[destination_vertex]):
                pdka.edges[vertex][letter] = {min(result_division[destination_vertex])}

    pdka.vertexes_number = len(pdka.edges)

    pdka.pretty_print()
    return pdka


def pdkator(dka):
    is_changed = False
    for vertex in dka.edges:
        for letter in dka.alphabet:
            if dka.edges[vertex][letter] == VertexFrozenset():
                is_changed = True
                dka.edges[vertex][letter] = VertexFrozenset({"dummy"})

    if is_changed:
        dka.vertexes_number += 1
        dka.edges["dummy"] = dict([(letter, VertexFrozenset({"dummy"})) for letter in dka.alphabet])
    dka.pretty_print()
    return dka


def dkator(good_nka):
    queue_v = Queue()
    queue_v.put(VertexFrozenset({good_nka.start_vertex}))
    dka_edges = dict()
    dka_terminal_vertexes = set()
    while not queue_v.empty():
        current_v = queue_v.get()
        dka_edges[current_v] = dict()
        for letter in good_nka.alphabet:
            destination_vertex = VertexFrozenset(set.union(*[good_nka.edges[vertex][letter] for vertex in current_v]))
            if destination_vertex == VertexFrozenset():
                dka_edges[current_v][letter] = VertexFrozenset()
                continue
            dka_edges[current_v][letter] = VertexFrozenset({destination_vertex})

            # print(destination_vertex, good_nka.terminal_vertexes)
            if destination_vertex.intersection(good_nka.terminal_vertexes) != VertexFrozenset():
                dka_terminal_vertexes.add(destination_vertex)

            if destination_vertex not in dka_edges:
                queue_v.put(destination_vertex)
    # print(dka_edges)
    # print(dka_terminal_vertexes)
    GoodNKA(len(dka_edges), VertexFrozenset({good_nka.start_vertex}), dka_terminal_vertexes, dka_edges,
            good_nka.edges).pretty_print()
    return GoodNKA(len(dka_edges), VertexFrozenset({good_nka.start_vertex}), dka_terminal_vertexes, dka_edges,
                   good_nka.alphabet)


def read(file=None):
    if file is not None:
        fd = open(file, 'r')
        fo = open('/dev/null', 'w')
        sys.stdin = fd
        sys.stdout = fo
    vertexes_number = int(input("Enter number of vertexes: "))
    edges_number = int(input("Enter number of edges: "))
    start_vertex = int(input("Enter start vertex: "))
    terminal_vertexes = VertexFrozenset(map(int, input("Enter terminal vertexes: ").split()))
    alphabet = list(input("Enter used alphabet: ").split())
    print("Now line by line enter edges in form: $from, $to, $letter")
    edges = {vertex + 1: {letter: set() for letter in alphabet} for vertex in range(vertexes_number)}
    for i in range(edges_number):
        from_v, to_v, letter_v = input(f"Enter edge number {i + 1}: ").split()
        from_v = int(from_v)
        to_v = int(to_v)
        edges[from_v][letter_v].add(to_v)

    if file is not None:
        sys.stdin.close()
        sys.stdout.close()
        sys.stdin = sys.__stdin__  # Reset the stdin to its default value
        sys.stdout = sys.__stdout__

    """print(start_vertex)
    print(terminal_vertexes)
    print(edges)
    print(alphabet)
    # print(frozenset([1, 2, 3, 4]))
    print(VertexFrozenset(set.union(*[{0, 1}, {1, 2}])))"""

    GoodNKA(vertexes_number, start_vertex, terminal_vertexes, edges, alphabet).pretty_print()

    # pdkator(GoodNKA(vertexes_number, start_vertex, terminal_vertexes, edges, alphabet)).pretty_print()

    return GoodNKA(vertexes_number, start_vertex, terminal_vertexes, edges,
                   alphabet)  # information about size we can get by len


if __name__ == "__main__":
    minimizator(pdkator(dkator(read("tests/expo_test.txt"))))

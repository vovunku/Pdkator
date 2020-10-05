import unittest
import pdkator


class FullTest2(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.automaton = pdkator.read("tests/test2.txt")
        cls.answers = []
        with open("tests/test2_ans.txt") as source:
            lines = source.readlines()
            cls.answers = [eval(line) for line in lines]

    def automaton_comparing(self, ans_automaton):
        self.assertEqual(self.automaton.vertexes_number, ans_automaton.vertexes_number)
        self.assertEqual(self.automaton.start_vertex, ans_automaton.start_vertex)
        self.assertEqual(self.automaton.terminal_vertexes, ans_automaton.terminal_vertexes)
        self.assertEqual(self.automaton.edges, ans_automaton.edges)
        self.assertEqual(self.automaton.alphabet, ans_automaton.alphabet)

    def test_all(self):
        self.automaton_comparing(self.answers[0])
        self.automaton = pdkator.dkator(self.automaton)
        self.automaton_comparing(self.answers[1])
        self.automaton = pdkator.pdkator(self.automaton)
        self.automaton_comparing(self.answers[2])
        self.automaton = pdkator.minimizator(self.automaton)
        self.automaton_comparing(self.answers[3])


if __name__ == "__main__":
    unittest.main()

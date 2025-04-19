from weightsplitter import support_functions as sf
from weightsplitter.errors import UnknownTerminal
import unittest


class FunctionsTest(unittest.TestCase):
    def test_stable_correct(self):
        weight_slice = [550, 550, 550, 550, 550]
        admitting_spikes = 50
        response = sf.check_weight_stable(weight_slice, admitting_spikes)
        self.assertTrue(response)

    def test_stable_incorrect(self):
        weight_slice = [101010, 1337, 1337, 1337, 1337]
        admitting_spikes = 50
        response = sf.check_weight_stable(weight_slice, admitting_spikes)
        self.assertTrue(not response)


if __name__ == '__main__':
    unittest.main()

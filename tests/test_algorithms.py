import unittest
from algorithms import merge_sort,bubble_sort,binary_search_amount,benchmark_sorts,synthetic_amounts

class AlgorithmTests(unittest.TestCase):
    def setUp(self): self.data=[{"amount":4},{"amount":2},{"amount":4},{"amount":1}]
    def test_sorts(self):
        self.assertEqual([x["amount"] for x in merge_sort(self.data)],[1,2,4,4])
        self.assertEqual([x["amount"] for x in bubble_sort(self.data,True)],[4,4,2,1])
        self.assertEqual([x["amount"] for x in self.data],[4,2,4,1])
    def test_binary_duplicates(self):
        self.assertEqual(len(binary_search_amount(merge_sort(self.data),4)),2)
        self.assertEqual(binary_search_amount(merge_sort(self.data),3),[])
    def test_benchmark(self):
        r=benchmark_sorts([4,1,3,2],3)
        self.assertEqual(r["input_size"],4); self.assertGreaterEqual(r["bubble_seconds"],0); self.assertGreaterEqual(r["merge_seconds"],0)
        self.assertEqual(synthetic_amounts(4),synthetic_amounts(4))

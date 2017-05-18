import unittest
from app import nodeset

class NodeSetTestCase(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_nodeset_basic_range(self):
        result = nodeset.expand('node[0-2]')
        expected = ['node0', 'node1', 'node2']
        self.assertEqual(result, expected)

    def test_nodeset_basic_range_with_spaces(self):
        result = nodeset.expand('node[0 - 2]')
        expected = ['node0', 'node1', 'node2']
        self.assertEqual(result, expected)

    def test_nodeset_two_basic_ranges(self):
        result = nodeset.expand('node[1-2]-[3-4]')
        expected = ['node1-3', 'node1-4', 'node2-3', 'node2-4']
        self.assertEqual(result, expected)

    def test_nodeset_compound_range(self):
        result = nodeset.expand('node[0-1,4,6]')
        expected = ['node0', 'node1', 'node4', 'node6']
        self.assertEqual(result, expected)

    def test_nodeset_compound_range_with_spaces(self):
        result = nodeset.expand('node[0-1, 4, 6]')
        expected = ['node0', 'node1', 'node4', 'node6']
        self.assertEqual(result, expected)

    def test_noderanges(self):
        result = nodeset.noderanges('node[13-14]-[1-4]')
        expected = [(4, 10), (12, 16)]
        self.assertEqual(result, expected)

    def test_expand_noderange(self):
        result = nodeset.expand_noderange('1-4')
        expected = ['1', '2', '3', '4']
        self.assertEqual(result, expected)

    def test_replace(self):
        result = nodeset.replace('c[13-14].local', 1, 7, 'XX')
        expected = 'cXX.local'
        self.assertEqual(result, expected)

    def test_product(self):
        result = nodeset.product([['c'], ['13', '14'], ['-'], ['1', '2']])
        expected = [('c', '13', '-', '1'), ('c', '13', '-', '2'),
                    ('c', '14', '-', '1'), ('c', '14', '-', '2')]
        self.assertEqual(result, expected)

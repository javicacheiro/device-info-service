import unittest
from .test_nodeset import NodeSetTestCase
from .test_endpoints import TestAPI

suite = unittest.TestSuite()
loader = unittest.TestLoader()
suite.addTests(loader.loadTestsFromTestCase(NodeSetTestCase))
suite.addTests(loader.loadTestsFromTestCase(TestAPI))

import unittest

class SimpleTest(unittest.TestCase):
    def test_import(self):
        import ezfiles
        self.assertIsNotNone(ezfiles)
        
    def test_true(self):
        self.assertTrue(True)

if __name__ == '__main__':
    unittest.main()

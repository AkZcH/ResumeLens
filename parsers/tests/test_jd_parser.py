import unittest
from ..jd_parser import JDParser

class TestJDParser(unittest.TestCase):
    def setUp(self):
        self.sample_jd = "Software Engineer position requiring Python and React experience"
        self.parser = JDParser(self.sample_jd)
    
    def test_requirements_extraction(self):
        # Test requirements extraction
        pass
    
    def test_skills_extraction(self):
        # Test skills extraction
        pass

if __name__ == '__main__':
    unittest.main()
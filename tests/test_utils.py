import unittest
from pypideps import _clean_requirements

class TestCleaner(unittest.TestCase):
    
    def test_strip_comments(self):
        reqs = ['#hello world']
        self.assertEqual(_clean_requirements(reqs), [])
        
    def test_trim_text(self):
        reqs = ['                      zope.app.intid']
        self.assertEqual(_clean_requirements(reqs), ['zope.app.intid'])
        
    def test_remove_reqs_string_part(self):
        reqs = ['SQLAlchemy>0.4']
        self.assertEqual(_clean_requirements(reqs), ['SQLAlchemy'])
        
    def test_no_blanks(self):
        reqs = ['SQLAlchemy>0.4', '']
        self.assertEqual(_clean_requirements(reqs), ['SQLAlchemy'])
        
    def test_garabage(self):
        reqs = ['(%s %s % (d', 'v and v or )).strip()', 'for d', 'v in requires.items()', '']
        self.assertEqual(_clean_requirements(reqs), [])
        
        reqs = ['line for line in open(requirements.txt)', '']
        self.assertEqual(_clean_requirements(reqs), [])